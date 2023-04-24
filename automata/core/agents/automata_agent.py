"""
    AutomataAgent is an autonomous agent that performs the actual work of the Automata
    system. Automata are responsible for executing instructions and reporting
    the results back to the master.

    Example:

 
        llm_toolkits = load_llm_toolkits(tools_list, **inputs)

        initial_payload = {
            "overview": python_inexer.get_overview(),
        }
        config_version = AutomataConfigVersion.AUTOMATA_MASTER_V3
        agent_config = AutomataAgentConfig.load(config_version)
        agent = (AutomataAgentBuilder(agent_config)
            .with_initial_payload(initial_payload)
            .with_llm_toolkits(llm_toolkits)
            .with_instructions(instructions)
            .with_model(model)
            .build())

        agent.run()

        TODO - Add error checking to ensure that we don't terminate when 
        our previous result returned an error
"""
import logging
import sqlite3
import uuid
from typing import Dict, List, Optional, Tuple

import openai
import yaml
from pydantic import BaseModel
from transformers import GPT2Tokenizer

from automata.config import *  # noqa F403
from automata.configs.agent_configs import AutomataConfigVersion
from automata.core import Toolkit, ToolkitType
from automata.core.utils import format_config_path

logger = logging.getLogger(__name__)


class AutomataAgentConfig(BaseModel):

    """
    Args:
        config_version (AutomataConfigVersion): The config_version of the agent to use.
        initial_payload (Dict[str, str]): Initial payload to send to the agent.
        llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary of toolkits to use.
        instructions (str): A string of instructions to execute.
        instruction_template (str): A string of instructions to execute.
        instruction_input_variables (List[str]): A list of input variables for the instruction template.
        model (str): The model to use for the agent.
        stream (bool): Whether to stream the results back to the master.
        verbose (bool): Whether to print the results to stdout.
        max_iters (int): The maximum number of iterations to run.
        temperature (float): The temperature to use for the agent.
        session_id (Optional[str]): The session ID to use for the agent.
    """

    class Config:
        AGENT_CONFIG_DIRECTORY = "agent_configs"
        arbitrary_types_allowed = True

    config_version: str = "default"
    initial_payload: Dict[str, str] = {}
    llm_toolkits: Dict[ToolkitType, Toolkit] = {}
    instructions: str = ""
    instruction_template: str = ""
    instruction_input_variables: List[str] = []
    model: str = "gpt-4"
    stream: bool = False
    verbose: bool = True
    max_iters: int = 1_000_000
    temperature: float = 0.7
    session_id: Optional[str] = None

    @classmethod
    def load(cls, config_version: AutomataConfigVersion) -> "AutomataAgentConfig":
        if config_version == AutomataConfigVersion.DEFAULT:
            return AutomataAgentConfig()
        config_path = format_config_path(cls.Config.AGENT_CONFIG_DIRECTORY, config_version.value)
        with open(f"{config_path}.yaml", "r") as file:
            loaded_yaml = yaml.safe_load(file)
            return AutomataAgentConfig(**loaded_yaml)


class AutomataAgentBuilder:
    def __init__(self, config: AutomataAgentConfig):
        self._instance = AutomataAgent(config)

    def with_initial_payload(self, initial_payload: Dict[str, str]):
        self._instance.initial_payload = initial_payload
        return self

    def with_llm_toolkits(self, llm_toolkits: Dict[ToolkitType, Toolkit]):
        self._instance.llm_toolkits = llm_toolkits
        return self

    def with_instructions(self, instructions: str):
        self._instance.instructions = instructions
        return self

    def with_model(self, model: str):
        self._instance.model = model
        return self

    def with_stream(self, stream: bool):
        self._instance.stream = stream
        return self

    def with_verbose(self, verbose: bool):
        self._instance.verbose = verbose
        return self

    def with_max_iters(self, max_iters: int):
        self._instance.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float):
        self._instance.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]):
        self._instance.session_id = session_id
        return self

    def build(self):
        self._instance._setup()
        return self._instance


class AutomataAgent:
    """
    AutomataAgent is an autonomous agent that performs the actual work of the Automata
    system. Automata are responsible for executing instructions and reporting
    the results back to the master.
    """

    CONTINUE_MESSAGE = "Continue, and return a result JSON when finished."
    NUM_DEFAULT_MESSAGES = 3

    def __init__(self, config: Optional[AutomataAgentConfig] = None):
        """
        Args:
            config_version (Optional[AutomataAgentConfig]): The config_version of the agent to use.
        Methods:
            iter_task(instructions: List[Dict[str, str]]) -> Dict[str, str]: Iterates through the instructions and returns the next instruction.
            replay_messages() -> List[Dict[str, str]]: Replays agent messages buffer.
        """
        if config is None:
            config = AutomataAgentConfig()
        self.initial_payload = config.initial_payload
        self.llm_toolkits = config.llm_toolkits
        self.instructions = config.instructions
        self.config_version = config.config_version
        self.instruction_template = config.instruction_template
        self.instruction_input_variables = config.instruction_input_variables
        self.model = config.model
        self.stream = config.stream
        self.verbose = config.verbose
        self.max_iters = config.max_iters
        self.temperature = config.temperature
        self.session_id = config.session_id

    def __del__(self):
        """Close the connection to the agent."""
        self.conn.close()

    def iter_task(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        """Run the test and report the tool outputs back to the master."""

        context_length = sum(
            [
                len(self.tokenizer.encode(message["content"], max_length=1024 * 8))
                for message in self.messages
            ]
        )
        if self.verbose:
            logger.info("Chat Context length: %s", context_length)
            logger.info("-" * 100)

        logger.info("Running instruction...")
        response_summary = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            stream=self.stream,
        )
        if self.stream:
            accumulated_output = ""
            separator = " "
            response_text = ""
            for chunk in response_summary:
                if "content" in chunk["choices"][0]["delta"]:
                    chunk_content = chunk["choices"][0]["delta"]["content"]
                    accumulated_output += chunk_content
                    response_text += chunk_content
                if separator in accumulated_output:
                    # Split the accumulated output into words
                    words = accumulated_output.split(separator)
                    # Print all words except the last one, as it may be an incomplete word
                    for word in words[:-1]:
                        print(word, end=" ", flush=True)
                    # Keep the last (potentially incomplete) word for the next iteration
                    accumulated_output = words[-1]
        else:
            response_text = response_summary["choices"][0]["message"]["content"]

        if self.verbose:
            logger.info("OpenAI Response:\n%s\n" % response_text)
        processed_inputs = self._process_input(response_text)
        self._save_interaction({"role": "assistant", "content": response_text})

        # If there are processed inputs, return here
        if len(processed_inputs) > 0:
            message = "Observation:\n{" + "\n"
            for i, output in enumerate(processed_inputs):
                message += f'"output_{i}": "{(output)}", \n'
            message += "}"
            self._save_interaction({"role": "user", "content": message})
            if self.verbose:
                logger.info("Synthetic User Message:\n%s\n" % message)
            return processed_inputs

        # If there are no outputs, then the user has must respond to continue
        self._save_interaction({"role": "user", "content": AutomataAgent.CONTINUE_MESSAGE})
        if self.verbose:
            logger.info("Synthetic User Message:\n%s\n" % AutomataAgent.CONTINUE_MESSAGE)

        return None

    def run(self) -> str:
        """Run until the initial instruction terminates."""

        while True:
            self.iter_task()
            # Check the previous previous agent message to see if it is a completion message
            if AutomataAgent.is_completion_message(self.messages[-2]["content"]):
                return self.messages[-2]["content"]
            # Each iteration produces two messages, so the check below is for equalling the max_iters
            if (len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES) >= self.max_iters * 2:
                return "Result was not captured before iterations exceeded max limit."

    def replay_messages(self) -> str:
        """Replay the messages in the conversation."""
        if len(self.messages) == 0:
            if self.verbose:
                logger.info("No messages to replay.")
            return "No messages to replay."
        for message in self.messages[1:]:
            if AutomataAgent.is_completion_message(message["content"]):
                return message["content"]
            processed_outputs = self._process_input(message["content"])
            if self.verbose:
                logger.info("Role:\n%s\n\nMessage:\n%s\n" % (message["role"], message["content"]))
                logger.info("Processing message content =  %s" % (message["content"]))
                logger.info("\nProcessed Outputs:\n%s\n" % processed_outputs)
                logger.info("-" * 100)
        return "No completion message found."

    def modify_last_instruction(self, new_instruction: str) -> None:
        """Extend the last instructions with a new message."""
        previous_message = self.messages[-1]
        self.messages[-1] = {
            "role": previous_message["role"],
            "content": f"{new_instruction}",
        }

    def _setup(self):
        """Setup the agent."""
        # Put the setup logic here that was originally in the __init__ method
        # Initialize OpenAI API Key
        openai.api_key = OPENAI_API_KEY  # noqa F405

        # Initialize state variables
        self.messages = []
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        if "tools" in self.instruction_input_variables:
            self.initial_payload["tools"] = "".join(
                [
                    f"\n{tool.name}: {tool.description}\n"
                    for toolkit in self.llm_toolkits.values()
                    for tool in toolkit.tools
                ]
            )

        prompt = self._load_prompt()

        self._init_database()

        if self.session_id:
            self._load_previous_interactions()
        else:
            self.session_id = str(uuid.uuid4())
            self._save_interaction({"role": "system", "content": prompt})
            initial_messages = [
                {
                    "role": "assistant",
                    "content": 'Thought: I will begin by initializing myself. {"tool": "automata-initializer", "input": "Hello, I am Automata, OpenAI\'s most skilled coding system. How may I assit you today?"}',
                },
                {"role": "user", "content": f'Observation:\n{{"task_0":"{self.instructions}"}}'},
            ]

            for message in initial_messages:
                self._save_interaction(message)

        if self.verbose:
            logger.info("Initializing with Prompt:%s\n" % (prompt))
            logger.info("-" * 100)

        # Check that initial_payload contains all input variables
        if set(self.instruction_input_variables) != set(list(self.initial_payload.keys())):
            raise ValueError(f"Initial payload does not match instruction_input_variables.")

        logger.info("Session ID: %s" % self.session_id)
        logger.info("-" * 100)

    def _load_prompt(self) -> str:
        """Load the prompt from a config_version specified at initialization."""
        prompt = ""
        for arg in self.instruction_input_variables:
            prompt = self.instruction_template.replace(f"{{{arg}}}", self.initial_payload[arg])
        return prompt

    def _process_input(self, response_text: str):
        """Process the messages in the conversation."""
        tool_calls = AutomataAgent._parse_input_string(response_text)
        logger.info("Tool Calls: %s" % tool_calls)
        outputs = []
        for tool_request in tool_calls:
            requested_tool, requested_tool_input = (
                tool_request["tool"],
                tool_request["input"] or "",
            )
            # Skip the automata-initializer tool
            if requested_tool == "automata-initializer":
                continue
            if requested_tool == "error-reporter":
                # In the event of an error, the tool_input becomes the output, as it is now a parsing error
                tool_output = requested_tool_input
                outputs.append(requested_tool_input)
            else:
                tool_found = False
                for toolkit in self.llm_toolkits.values():
                    for tool in toolkit.tools:
                        if tool.name == requested_tool:
                            tool_output = tool.run(requested_tool_input, verbose=False)
                            outputs.append(tool_output)
                            tool_found = True
                            break  # Tool found, no need to continue the inner loop
                    if tool_found:
                        break  # Tool found, no need to continue the outer loop
                if not tool_found:
                    error_message = f"Error: Tool '{requested_tool}' not found."
                    outputs.append(error_message)
        return outputs

    def _init_database(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(CONVERSATION_DB_NAME)  # noqa F405
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                session_id INTEGER,
                interaction_id INTEGER,
                role TEXT,
                content TEXT,
                PRIMARY KEY (session_id, interaction_id)
            )
            """
        )
        self.conn.commit()

    def _save_interaction(self, interaction: Dict[str, str]):
        """Save the interaction to the database."""
        interaction_id = len(self.messages)
        role = interaction["role"]
        content = interaction["content"]
        self.cursor.execute(
            "INSERT INTO interactions (session_id, interaction_id, role, content) VALUES (?, ?, ?, ?)",
            (self.session_id, interaction_id, role, content),
        )
        self.conn.commit()
        self.messages.append(interaction)

    def _load_previous_interactions(self):
        self.cursor.execute(
            "SELECT role, content FROM interactions WHERE session_id = ? ORDER BY interaction_id ASC",
            (self.session_id,),
        )
        self.messages = [
            {"role": role, "content": content} for role, content in self.cursor.fetchall()
        ]

    @staticmethod
    def _extract_json_objects(input_str: str) -> List[str]:
        """Extract non-nested JSON objects from the input string."""
        json_objects = []
        stack = []
        start_idx = -1

        for idx, char in enumerate(input_str):
            if char == "{":
                stack.append(char)
                if len(stack) == 1:
                    start_idx = idx
            elif char == "}":
                if stack and stack[-1] == "{":
                    stack.pop()
                if not stack:
                    json_objects.append(input_str[start_idx : idx + 1])

        return json_objects

    @staticmethod
    def _extract_tool_and_input(json_object_str: List[str]) -> List[Tuple[str, Optional[str]]]:
        """Extract the tool and input from the JSON object string."""
        results = []
        for json_object in json_object_str:
            tool_tag, input_tag = '"tool":', '"input":'
            if tool_tag not in json_object:
                continue

            def _strip_trailing_cruft(s: str) -> str:
                return s.strip()[1:-1].strip("'").strip('"').strip("'\n").strip('"\n')

            tool = _strip_trailing_cruft(json_object.split(tool_tag)[1].split(",")[0])

            input_str = None
            if input_tag in json_object:
                split_on_input_tag = json_object.split(input_tag)[1].split("}")
                joined_input_str = "}".join(split_on_input_tag[:-1])
                input_str = joined_input_str.strip()[1:-1]
            results.append((tool, input_str))
        return results

    @staticmethod
    def _parse_input_string(input_str: str) -> List[Dict[str, Optional[str]]]:
        """Parse the input string into a list of tool and input pairs."""
        extracted_json_objects = AutomataAgent._extract_json_objects(input_str)
        tool_input_pairs = AutomataAgent._extract_tool_and_input(extracted_json_objects)
        parsed_entries = []
        for tool_input_pair in tool_input_pairs:
            parsed_entries.append({"tool": tool_input_pair[0], "input": tool_input_pair[1]})
        return [{"tool": entry["tool"], "input": entry.get("input")} for entry in parsed_entries]

    @staticmethod
    def is_completion_message(message: str):
        """Check if the message is a completion message."""
        match_filter = "result_0"
        match_string = '"%s":' % (match_filter)
        return match_string in message
