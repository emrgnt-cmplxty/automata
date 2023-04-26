"""
    AutomataAgent is an autonomous agent that performs the actual work of the Automata
    system. Automata are responsible for executing instructions and reporting
    the results back to the master.

    Example:

 
        llm_toolkits = build_llm_toolkits(tools_list, **inputs)

        config_version = AutomataConfigVersion.AUTOMATA_MASTER_PROD
        agent_config = AutomataAgentConfig.load(config_version)
        agent = (AutomataAgentBuilder(agent_config)
            .with_llm_toolkits(llm_toolkits)
            .with_instructions(instructions)
            .with_model(model)
            .build())

        agent.run()

        TODO - Add error checking to ensure that we don't terminate when
        our previous result returned an error
        TODO - Move action to a separate class
             - Cleanup cruft associated w/ old actiion definition
        TODO - Add more unit tests to the iter_task workflow
        TODO - Cleanup approach behind _retrieve_completion_message
             - Right now, multiple results are not handled properly
               Moreover, messages with results + tool outputs will
               not be handled properly, as outputs are discarded
"""
import logging
import sqlite3
import textwrap
import uuid
from typing import Dict, List, Optional, Tuple, Union, cast

import openai
from termcolor import colored
from transformers import GPT2Tokenizer

from automata.config import CONVERSATION_DB_NAME, OPENAI_API_KEY
from automata.configs.agent_configs.config_type import AutomataAgentConfig
from automata.core.base.tool import Toolkit, ToolkitType

logger = logging.getLogger(__name__)
ActionType = Dict[str, Union[str, List[str]]]


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
        if model not in AutomataAgentConfig.Config.SUPPORTED_MDOELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool):
        if not isinstance(stream, bool):
            raise ValueError("Stream must be a boolean.")
        self._instance.stream = stream
        return self

    def with_verbose(self, verbose: bool):
        if not isinstance(verbose, bool):
            raise ValueError("Verbose must be a boolean.")
        self._instance.verbose = verbose
        return self

    def with_max_iters(self, max_iters: int):
        if not isinstance(max_iters, int):
            raise ValueError("Max iters must be an integer.")
        self._instance.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float):
        if not isinstance(temperature, float):
            raise ValueError("Temperature iters must be a float.")
        self._instance.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]):
        if session_id and (not isinstance(session_id, str)):
            raise ValueError("Session Id must be a str.")
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
            modify_last_instruction(new_instruction: str) -> None
            replay_messages() -> List[Dict[str, str]]: Replays agent messages buffer.
            run() -> str: Runs the agent.
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
        self.completed = False

    def __del__(self):
        """Close the connection to the agent."""
        self.conn.close()

    def iter_task(self) -> Optional[Tuple[Dict[str, str], Dict[str, str]]]:
        """Run the test and report the tool outputs back to the master."""
        if self.completed:
            raise ValueError("Cannot run an agent that has already completed.")
        context_length = sum(
            [
                len(
                    self.tokenizer.encode(message["content"], max_length=1024 * 8, truncation=True)
                )
                for message in self.messages
            ]
        )
        logger.debug("Chat Context length: %s", context_length)
        logger.debug("-" * 60)
        logger.info("Running instruction...")
        response_summary = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            stream=self.stream,
        )
        if self.stream:
            print(colored("\n>>>", "green", attrs=["blink"]) + colored(" Agent:", "green"))
            accumulated_output = ""
            separator = " "
            response_text = ""
            for chunk in response_summary:
                if "content" in chunk["choices"][0]["delta"]:
                    chunk_content = chunk["choices"][0]["delta"]["content"]
                    accumulated_output += chunk_content
                    response_text += chunk_content
                if separator in accumulated_output:
                    words = accumulated_output.split(separator)
                    for word in words[:-1]:
                        print(colored(str(word), "green"), end=" ", flush=True)
                    accumulated_output = words[-1]
            print(colored(str(accumulated_output), "green"))
        else:
            response_text = response_summary["choices"][0]["message"]["content"]
        logger.debug("OpenAI Response:\n%s\n" % response_text)
        assistant_message = {"role": "assistant", "content": response_text}
        responses: List[Dict[str, str]] = []
        responses.append(assistant_message)
        self._save_interaction(assistant_message)
        observations = self._generate_observations(response_text)
        completion_message = AutomataAgent._retrieve_completion_message(observations)
        if completion_message:
            self.completed = True
            self._save_interaction({"role": "assistant", "content": completion_message})
            return None
        if len(observations) > 0:
            user_observation_message = AutomataAgent._generate_user_observation_message(
                observations
            )
            user_message = {"role": "user", "content": user_observation_message}
            logger.debug("Synthetic User Message:\n%s\n" % user_observation_message)
        else:
            user_message = {"role": "user", "content": AutomataAgent.CONTINUE_MESSAGE}
            logger.debug("Synthetic User Message:\n%s\n" % AutomataAgent.CONTINUE_MESSAGE)
        responses.append(user_message)
        self._save_interaction(user_message)
        return (assistant_message, user_message)

    def run(self) -> str:
        latest_responses = self.iter_task()
        while latest_responses is not None:
            latest_responses = self.iter_task()
            if len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES >= self.max_iters * 2:
                return "Result was not captured before iterations exceeded max limit."
            print("IN RUN, self.messages[-1][content]=", self.messages[-1]["content"])
            print("IN RUN, self.messages[-2][content]=", self.messages[-2]["content"])
            print("IN RUN, latest_responses=", latest_responses)

        return self.messages[-1]["content"]

    def replay_messages(self) -> str:
        """Replay the messages in the conversation."""
        if len(self.messages) == 0:
            logger.debug("No messages to replay.")
            return "No messages to replay."
        for message in self.messages[1:]:
            observations = self._generate_observations(message["content"])
            completion_message = AutomataAgent._retrieve_completion_message(observations)
            if completion_message:
                return completion_message
            logger.debug("Role:\n%s\n\nMessage:\n%s\n" % (message["role"], message["content"]))
            logger.debug("Processing message content =  %s" % message["content"])
            logger.debug("\nProcessed Outputs:\n%s\n" % observations)
            logger.debug("-" * 60)
        return "No completion message found."

    def modify_last_instruction(self, new_instruction: str) -> None:
        """Extend the last instructions with a new message."""
        previous_message = self.messages[-1]
        self.messages[-1] = {"role": previous_message["role"], "content": f"{new_instruction}"}

    def _setup(self):
        """Setup the agent."""
        openai.api_key = OPENAI_API_KEY
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
                    "content": textwrap.dedent(
                        "\n                        - thoughts\n                            - I will begin by initializing myself.\n                        - actions\n                            - tool_query_0\n                            - tool\n                                - automata-initializer\n                            - input\n                                - Hello, I am Automata, OpenAI's most skilled coding system. How may I assist you today?\n                        "
                    ),
                },
                {
                    "role": "user",
                    "content": textwrap.dedent(
                        f"\n                        - observation:\n                          - task_0\n                            - Please carry out the following instruction {self.instructions},\n                        "
                    ),
                },
            ]
            for message in initial_messages:
                self._save_interaction(message)
        logger.debug("Initializing with Prompt:%s\n" % prompt)
        logger.debug("-" * 60)
        if set(self.instruction_input_variables) != set(list(self.initial_payload.keys())):
            raise ValueError(f"Initial payload does not match instruction_input_variables.")
        logger.debug("Session ID: %s" % self.session_id)
        logger.debug("-" * 60)

    def _load_prompt(self) -> str:
        """Load the prompt from a config_version specified at initialization."""
        prompt = ""
        for arg in self.instruction_input_variables:
            prompt = self.instruction_template.replace(f"{{{arg}}}", self.initial_payload[arg])
        return prompt

    def _generate_observations(self, response_text: str) -> Dict[str, str]:
        """Process the messages in the conversation."""
        actions = AutomataAgent._extract_actions(response_text)
        print("EXTRACTED ACTIONS:", actions)
        logger.debug("Actions: %s" % actions)
        outputs = {}
        (result_counter, tool_counter) = (0, 0)
        for action_request in actions:
            if "tool" in action_request:
                (requested_tool, requested_tool_input) = (
                    action_request["tool"],
                    action_request["input"] or "",
                )
                if requested_tool == "automata-initializer":
                    continue
                if AutomataAgent.ActionExtractor.return_result_indicator in requested_tool:
                    outputs[
                        "%s_%i"
                        % (AutomataAgent.ActionExtractor.return_result_indicator, result_counter)
                    ] = "\n".join(requested_tool_input)
                    result_counter += 1
                    continue
                if requested_tool == "error-reporter":
                    tool_output = requested_tool_input
                    outputs["%s_%i" % ("output", tool_counter)] = cast(str, tool_output)
                    tool_counter += 1
                else:
                    tool_found = False
                    for toolkit in self.llm_toolkits.values():
                        for tool in toolkit.tools:
                            if tool.name == requested_tool:
                                tool_output = tool.run(tuple(requested_tool_input), verbose=False)
                                outputs["%s_%i" % ("output", tool_counter)] = cast(
                                    str, tool_output
                                )
                                tool_counter += 1
                                tool_found = True
                                break
                        if tool_found:
                            break
                    if not tool_found:
                        error_message = f"Error: Tool '{requested_tool}' not found."
                        outputs["%s_%i" % ("output", tool_counter)] = error_message
                        tool_counter += 1
        return outputs

    def _init_database(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(CONVERSATION_DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "\n            CREATE TABLE IF NOT EXISTS interactions (\n                session_id INTEGER,\n                interaction_id INTEGER,\n                role TEXT,\n                content TEXT,\n                PRIMARY KEY (session_id, interaction_id)\n            )\n            "
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
        """Load the previous interactions from the database."""
        self.cursor.execute(
            "SELECT role, content FROM interactions WHERE session_id = ? ORDER BY interaction_id ASC",
            (self.session_id,),
        )
        self.messages = [
            {"role": role, "content": content} for (role, content) in self.cursor.fetchall()
        ]

    @staticmethod
    def _extract_actions(text: str) -> List[ActionType]:
        """Extract actions from the given text."""
        return AutomataAgent.ActionExtractor.extract_actions(text)

    @staticmethod
    def _retrieve_completion_message(processed_inputs: Dict[str, str]) -> Optional[str]:
        """Check if the result is a return result indicator."""
        for processed_input in processed_inputs.keys():
            if AutomataAgent.ActionExtractor.return_result_indicator in processed_input:
                return processed_inputs[processed_input]
        return None

    @staticmethod
    def _generate_user_observation_message(observations: Dict[str, str]) -> str:
        message = f"{AutomataAgent.ActionExtractor.action_indicator} observations\n"
        for observation_name in observations.keys():
            message += f"    - {observation_name}" + "\n"
            message += f"      - {observations[observation_name]}" + "\n"
        return message

    class ActionExtractor:
        """Class for extracting actions from an AutomataAgent string."""

        action_indicator = "- "
        code_indicator = "```"
        tool_indicator = "tool_query"
        return_result_indicator = "return_result"
        expected_coded_languages = ["python"]

        @classmethod
        def extract_actions(cls, text: str) -> List[ActionType]:
            """
            Extract actions from the given text.

            Args:
                text: A string containing actions formatted as nested lists.

            Returns:
                A list of dictionaries containing actions and their inputs.
            """
            lines = text.split("\n")
            actions: List[ActionType] = []
            action: Optional[ActionType] = None
            is_code = False
            skip_next = False
            for index, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                if cls._is_new_tool_action(lines, index):
                    action = cls._process_new_tool_action(action, line, actions)
                    skip_next = True
                elif cls._is_return_result_action(line):
                    action = cls._process_new_return_result_action(action, line, actions)
                else:
                    (is_code, skip_next) = cls._process_action_input(
                        lines, index, line, action, is_code, skip_next
                    )
            if action is not None:
                actions.append(action)
            return actions

        @staticmethod
        def _is_new_tool_action(lines, index):
            """Check if the current line is a new action."""
            return (
                f"{AutomataAgent.ActionExtractor.action_indicator}tool" in lines[index - 1]
                and f"{AutomataAgent.ActionExtractor.action_indicator}{AutomataAgent.ActionExtractor.tool_indicator}"
                in lines[index - 2]
                and (AutomataAgent.ActionExtractor.action_indicator in lines[index])
                and (len(lines) > index + 1)
                and (f"{AutomataAgent.ActionExtractor.action_indicator}inputs" in lines[index + 1])
            )

        @staticmethod
        def _process_new_tool_action(
            action: Optional[ActionType], line: str, actions: List[ActionType]
        ):
            """Process a new action."""
            if action is not None and "tool" in action:
                actions.append(action)
            tool_name = line.split(AutomataAgent.ActionExtractor.action_indicator)[1].strip()
            return {"tool": tool_name, "input": []}

        @staticmethod
        def _is_return_result_action(line: str) -> bool:
            return line.strip().startswith(
                f"{AutomataAgent.ActionExtractor.action_indicator}{AutomataAgent.ActionExtractor.return_result_indicator}"
            )

        @staticmethod
        def _process_new_return_result_action(
            action: Optional[ActionType], line: str, actions: List[ActionType]
        ):
            """Process a new return result action."""
            if action is not None and "tool" in action:
                actions.append(action)
            return {
                "tool": line.strip()
                .split(AutomataAgent.ActionExtractor.action_indicator)[1]
                .split(AutomataAgent.ActionExtractor.action_indicator)[0]
                .strip(),
                "input": [],
            }

        @staticmethod
        def _process_action_input(
            lines: List[str],
            index: int,
            line: str,
            action: Optional[ActionType],
            is_code: bool,
            skip_next: bool,
        ):
            """Process an action input."""
            if action is not None:
                inputs = cast(List[str], action["input"])
                if AutomataAgent.ActionExtractor._is_code_start(lines, index) and (not is_code):
                    is_code = True
                    for language in AutomataAgent.ActionExtractor.expected_coded_languages:
                        if language in line:
                            contains_language_definition = True
                    if contains_language_definition:
                        inputs.append("")
                    else:
                        inputs.append(line + "\n")
                    skip_next = True
                elif not AutomataAgent.ActionExtractor._is_code_indicator(line) and is_code:
                    inputs[-1] += line + "\n"
                elif AutomataAgent.ActionExtractor._is_code_end(line) and (not is_code):
                    raise ValueError(f"Invalid action format: {line}")
                elif AutomataAgent.ActionExtractor._is_code_end(line) and is_code:
                    is_code = False
                    inputs[-1] = textwrap.dedent(action["input"][-1])
                elif AutomataAgent.ActionExtractor.action_indicator in line:
                    clean_line = line.split(AutomataAgent.ActionExtractor.action_indicator)[
                        1
                    ].strip()
                    inputs.append(clean_line)
            return (is_code, skip_next)

        @staticmethod
        def _is_code_start(lines: List[str], index: int):
            """Check if the current line is the start of a code block."""
            return (
                len(lines) > index + 1
                and AutomataAgent.ActionExtractor.code_indicator in lines[index + 1]
            )

        @staticmethod
        def _is_code_end(line: str) -> bool:
            """Check if the current line is the end of a code block."""
            return AutomataAgent.ActionExtractor.code_indicator in line

        @staticmethod
        def _is_code_indicator(line: str) -> bool:
            """Check if the current line is a code indicator."""
            return line.strip() == AutomataAgent.ActionExtractor.code_indicator
