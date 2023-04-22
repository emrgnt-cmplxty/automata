"""
    MrMeeseeksAgent is an autonomous agent that performs the actual work of the Spork
    system. Meeseeks are responsible for executing instructions and reporting
    the results back to the master.

    Example:

 
        inputs = {"model": args.model}
        llm_tools = load_llm_tools(tools_list, inputs, logger)

        initial_payload = {
            "overview": python_inexer.get_overview(),
        }

        logger.info("Passing in instructions: %s", args.instructions)
        logger.info("-" * 100)
        agent = MrMeeseeksAgent(
            initial_payload=initial_payload,
            instructions=args.instructions,
            llm_tools=llm_tools,
            version=args.version,
            model=args.model,
            session_id=args.session_id,
            stream=args.stream,
        )

        next_instruction = agent.iter_task(instructions)
        ...
        TODO - Add error checking to ensure that we don't terminate when
        our previous result returned an error
"""
import logging
import sqlite3
import uuid
from typing import Dict, List, Optional, Tuple

import openai
import yaml
from transformers import GPT2Tokenizer

from spork.config import *  # noqa F403
from spork.tools.base.tool_utils import Toolkit, ToolkitType
from spork.tools.utils import format_config_path

from .agent_configs.agent_version import AgentVersion

logger = logging.getLogger(__name__)


class MrMeeseeksAgent:
    """
    MrMeeseeksAgent is an autonomous agent that performs the actual work of the Spork
    system. Meeseeks are responsible for executing instructions and reporting
    the results back to the master.
    """

    CONTINUE_MESSAGE = "Continue, and return a result JSON when finished."

    def __init__(
        self,
        initial_payload: Dict[str, str],
        llm_tools: Dict[ToolkitType, Toolkit],
        instructions: str,
        version: AgentVersion = AgentVersion.MEESEEKS_MASTER_V2,
        model: str = "gpt-4",
        session_id: Optional[str] = None,
        stream: bool = False,
        verbose: bool = True,
    ):
        """
        Args:
            initial_payload (Dict[str, str]): The initial payload to be used for the agent.
            initial_instructions (List[Dict[str, str]]): The initial instructions to be used for the agent.
            tools (Dict[ToolkitType, Toolkit] ): The tools to be used for the agent.
            version (AgentVersion, optional): The version of the agent. Defaults to AgentVersion.MEESEEKS_MASTER_V1.
            model (str, optional): The model to be used for the agent. Defaults to "gpt-4".
            session_id (Optional[str], optional): The session id to be used for the agent. Defaults to None.

        Attributes:
            model (str): The model to be used for the agent.
            version (AgentVersion): The version of the agent.
            tools (Dict[ToolkitType, Toolkit] ): The tools to be used for the agent.
            messages (List[Dict[str, str]]): The messages that have been sent to the agent.
            session_id (str): The session id to be used for the agent.

        Methods:
            iter_task(instructions: List[Dict[str, str]]) -> Dict[str, str]: Iterates through the instructions and returns the next instruction.
            replay_messages() -> List[Dict[str, str]]: Replays agent messages buffer.

        """

        # Initialize OpenAI API Key
        openai.api_key = OPENAI_API_KEY  # noqa F405

        # Initialize state variables
        self.model = model
        self.version = version
        self.toolkits = llm_tools
        self.messages: List[Dict[str, str]] = []
        self.stream = stream
        self.verbose = verbose

        initial_payload["tools"] = "".join(
            [
                f"\n{tool.name}: {tool.description}\n"
                for toolkit in self.toolkits.values()
                for tool in toolkit.tools
            ]
        )

        prompt = self._load_prompt(initial_payload)

        self._init_database()

        if session_id:
            self.session_id = session_id
            self._load_previous_interactions()
        else:
            self.session_id = str(uuid.uuid4())
            self._save_interaction({"role": "system", "content": prompt})
            initial_messages = [
                {
                    "role": "assistant",
                    "content": 'Thought: I will begin by initializing myself. {"tool": "meeseeks-initializer", "input": "Hello, I am Mr. Meeseeks, one OpenAI\'s most skilled coders. What coding challenge can I solve for you today?"}',
                },
                {"role": "user", "content": f'Observation:\n{{"task_0":"{instructions}"}}'},
            ]

            for message in initial_messages:
                self._save_interaction(message)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        if self.verbose:
            logger.info("Initializing with Prompt:%s\n" % (prompt))
            logger.info("-" * 100)
        logger.info("Session ID: %s" % self.session_id)
        logger.info("-" * 100)

    def __del__(self):
        self.conn.close()

    def iter_task(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        """Run the test and report the tool outputs back to the master."""
        logger.info("Running instruction...")
        response_summary = openai.ChatCompletion.create(
            model=self.model, messages=self.messages, temperature=0.7, stream=self.stream
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
        self._save_interaction({"role": "user", "content": MrMeeseeksAgent.CONTINUE_MESSAGE})
        if self.verbose:
            logger.info("Synthetic User Message:\n%s\n" % MrMeeseeksAgent.CONTINUE_MESSAGE)
        context_length = sum(
            [
                len(self.tokenizer.encode(message["content"], max_length=1024 * 8))
                for message in self.messages
            ]
        )
        if self.verbose:
            logger.info("Chat Context length: %s", context_length)
            logger.info("-" * 100)

        return None

    def run(self) -> str:
        """Run until the initial instruction terminates."""

        while True:
            self.iter_task()

            if MrMeeseeksAgent.is_completion_message(self.messages[-1]["content"]):
                return self.messages[-1]["content"]
            # Check the previous previous message to see if it is a completion message
            if MrMeeseeksAgent.is_completion_message(self.messages[-2]["content"]):
                return self.messages[-2]["content"]

    def replay_messages(self) -> str:
        """Replay the messages in the conversation."""
        if len(self.messages) == 0:
            if self.verbose:
                logger.info("No messages to replay.")
            return "No messages to replay."
        for message in self.messages[1:]:
            if MrMeeseeksAgent.is_completion_message(message["content"]):
                return message["content"]
            processed_outputs = self._process_input(message["content"])
            if self.verbose:
                logger.info("Role:\n%s\n\nMessage:\n%s\n" % (message["role"], message["content"]))
                logger.info("Processing message content =  %s" % (message["content"]))
                logger.info("\nProcessed Outputs:\n%s\n" % processed_outputs)
                logger.info("-" * 100)
        return "No completion message found."

    def extend_last_instructions(self, new_message: str) -> None:
        previous_message = self.messages[-1]
        self.messages[-1] = {
            "role": previous_message["role"],
            "content": f"{previous_message}\n{new_message}",
        }

    def _load_prompt(self, initial_payload: Dict[str, str]) -> str:
        """Load the prompt from a config specified at initialization."""
        with open(
            format_config_path("agent_configs", f"{self.version.value}.yaml"),
            "r",
        ) as file:
            loaded_yaml = yaml.safe_load(file)
        prompt = loaded_yaml["template"]
        for arg in loaded_yaml["input_variables"]:
            prompt = prompt.replace(f"{{{arg}}}", initial_payload[arg])
        return prompt

    def _process_input(self, response_text: str):
        """Process the messages in the conversation."""
        tool_calls = MrMeeseeksAgent._parse_input_string(response_text)
        logger.info("Tool Calls: %s" % tool_calls)
        outputs = []
        for tool_request in tool_calls:
            requested_tool, requested_tool_input = (
                tool_request["tool"],
                tool_request["input"] or "",
            )
            # Skip the meeseeks-initializer tool
            if requested_tool == "meeseeks-initializer":
                continue
            if requested_tool == "error-reporter":
                # In the event of an error, the tool_input becomes the output, as it is now a parsing error
                tool_output = requested_tool_input
                outputs.append(requested_tool_input)
            else:
                tool_found = False
                for toolkit in self.toolkits.values():
                    for tool in toolkit.tools:
                        if tool.name == requested_tool:
                            tool_output = tool.run(requested_tool_input, verbose=False)
                            outputs.append(tool_output)
                            tool_found = True
                            break  # Tool found, no need to continue the inner loop
                    if tool_found:
                        break  # Tool found, no need to continue the outer loop                if not tool_found:
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
        extracted_json_objects = MrMeeseeksAgent._extract_json_objects(input_str)
        tool_input_pairs = MrMeeseeksAgent._extract_tool_and_input(extracted_json_objects)
        parsed_entries = []
        for tool_input_pair in tool_input_pairs:
            parsed_entries.append({"tool": tool_input_pair[0], "input": tool_input_pair[1]})
        return [{"tool": entry["tool"], "input": entry.get("input")} for entry in parsed_entries]

    @staticmethod
    def is_completion_message(message: str):
        match_filter = "result_0"
        match_string = '"%s":' % (match_filter)
        return match_string in message
