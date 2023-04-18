"""
    AgentMrMeeseeks is an autonomous agent that performs the actual work of the Spork
    system. Meeseeks are responsible for executing instructions and reporting
    the results back to the master.

    Example:

        python_parser = PythonParser()
        python_writer = PythonWriter(python_parser)

        exec_tools = []
        exec_tools += build_tools(python_parser)
        exec_tools += build_tools(python_writer)
        overview = python_parser.get_overview()

        initial_payload = {
            "overview": overview,
        }
        agent = AgentMrMeeseeks(initial_payload, exec_tools)

        next_instruction = agent.iter_task(instructions)
        ...
"""
import json
import logging
import re
import sqlite3
import uuid
from typing import Dict, List, Optional

import openai
import regex
import yaml
from demjson import decode
from langchain.tools.base import BaseTool
from transformers import GPT2Tokenizer

from spork.config import *  # noqa F403

from ...tools.utils import format_config_path
from ..tool_managers.tool_builder import build_tools
from .agent_configs.agent_version import AgentVersion

CONTINUE_MESSAGE = "Continue"
COMPLETION_MESSAGE = "TASK_COMPLETED"

logger = logging.getLogger(__name__)


class AgentMrMeeseeks:
    """
    AgentMrMeeseeks is an autonomous agent that performs the actual work of the Spork
    system. Meeseeks are responsible for executing instructions and reporting
    the results back to the master.
    """

    def __init__(
        self,
        initial_payload: Dict[str, str],
        tools: List[BaseTool],
        instructions: str,
        version: AgentVersion = AgentVersion.MEESEEKS_V1,
        model: str = "gpt-4",
        session_id: Optional[str] = None,
        stream: bool = False,
    ):
        """
        Args:
            initial_payload (Dict[str, str]): The initial payload to be used for the agent.
            initial_instructions (List[Dict[str, str]]): The initial instructions to be used for the agent.
            tools (List[BaseTool]): The tools to be used for the agent.
            version (AgentVersion, optional): The version of the agent. Defaults to AgentVersion.MEESEEKS_V1.
            model (str, optional): The model to be used for the agent. Defaults to "gpt-4".
            session_id (Optional[str], optional): The session id to be used for the agent. Defaults to None.

        Attributes:
            model (str): The model to be used for the agent.
            version (AgentVersion): The version of the agent.
            tools (List[BaseTool]): The tools to be used for the agent.
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
        self.tools = tools
        self.messages: List[Dict[str, str]] = []
        self.stream = stream

        initial_payload["tools"] = "".join(
            ["\n%s: %s\n" % (tool.name, tool.description) for tool in self.tools]
        )
        initial_payload["completion_message"] = COMPLETION_MESSAGE
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
                    "content": '{"tool": "meeseeks-initializer", "input": "Hello, I am Mr. Meeseeks, one OpenAI\'s most skilled coders. What coding challenge can I solve for you today?"}',
                },
                {"role": "user", "content": instructions},
            ]

            for message in initial_messages:
                self._save_interaction(message)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

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

        logger.info("OpenAI Response:\n%s\n" % response_text)
        processed_inputs = self._process_input(response_text)
        self._save_interaction({"role": "assistant", "content": response_text})

        if len(processed_inputs) > 0:
            message = "{" + "\n"
            for i, output in enumerate(processed_inputs):
                message += f'"output_{i}": {(output)}, \n'
            message += "}"
            self._save_interaction({"role": "user", "content": message})
            logger.info("Synthetic User Message:\n%s\n" % message)
            return processed_inputs

        # If there are no outputs, then the user has must respond to continue
        self._save_interaction({"role": "user", "content": CONTINUE_MESSAGE})
        logger.info("Synthetic User Message:\n%s\n" % CONTINUE_MESSAGE)
        context_length = sum(
            [
                len(self.tokenizer.encode(message["content"], max_length=1024 * 8))
                for message in self.messages
            ]
        )

        logger.info("Chat Context length: %s", context_length)
        logger.info("-" * 100)

        return None

    def run(self) -> None:
        """Run until the initial instruction terminates."""
        while True:
            self.iter_task()
            if COMPLETION_MESSAGE in self.messages[-1]["content"]:
                break
            if COMPLETION_MESSAGE in self.messages[-2]["content"]:
                break

    def replay_messages(self) -> None:
        """Replay the messages in the conversation."""
        if len(self.messages) == 0:
            logger.info("No messages to replay.")
            return
        for message in self.messages:
            if message["role"] == "user":
                continue
            logger.info("Role:\n%s\n\nMessage:\n%s\n" % (message["role"], message["content"]))
            logger.info("Processing message content = ", message["content"])
            processed_outputs = self._process_input(message["content"])
            logger.info("\nProcessed Outputs:\n%s\n" % processed_outputs)
            logger.info("-" * 100)

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
        tool_calls = AgentMrMeeseeks._parse_input_string(response_text)
        outputs = []
        for tool_request in tool_calls:
            tool, tool_input = tool_request["tool"], tool_request["input"]
            if tool == "error-reporter":
                # In the event of an error, the tool_input becomes the output, as it is now a parsing error
                tool_output = tool_input
                outputs.append(tool_input)

            for tool_instance in self.tools:
                if tool_instance.name == tool:
                    tool_output = tool_instance.run(tool_input, verbose=False)
                    outputs.append(tool_output)
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
    def _replace_single_quotes(input_str: str) -> str:
        input_str = re.sub(r"((?<!\\)')", '"', input_str)
        return re.sub(r'(?<!\\)""(?!\s*[:,}])', "'", input_str)

    @staticmethod
    def _fix_unquoted_keys(input_str: str) -> str:
        return re.sub(r'(?<!")(\b\w+\b)(?!":)', r'"\1"', input_str)

    @staticmethod
    def _add_missing_commas(input_str: str) -> str:
        return re.sub(r"\}(?=\s*\{)", "},", input_str)

    @staticmethod
    def _remove_trailing_commas(input_str: str) -> str:
        return re.sub(r",\s*(}|\])", r"\1", input_str)

    @staticmethod
    def _extract_json_objects(input_str: str) -> str:
        """Extract all JSON objects from the input string."""
        json_pattern = r"\{(?:[^{}]|(?R))*?\}"
        json_matches = regex.findall(json_pattern, input_str, regex.MULTILINE)
        return json_matches

    @staticmethod
    def preprocess_input_string(input_str: str) -> str:
        input_str = AgentMrMeeseeks._replace_single_quotes(input_str)
        input_str = AgentMrMeeseeks._fix_unquoted_keys(input_str)
        input_str = AgentMrMeeseeks._add_missing_commas(input_str)
        input_str = AgentMrMeeseeks._remove_trailing_commas(input_str)
        return input_str

    @staticmethod
    def _sanitize_json(json_str: str) -> str:
        try:
            # Replace single quotes with double quotes, but not when escaped
            sanitized_str = re.sub(r"(?<!\\)'", '"', json_str)
            decoded = decode(sanitized_str, encoding="utf-8")
            return json.dumps(decoded)
        except Exception as e:
            return "Error parsing JSON: %s" % e

    @staticmethod
    def _parse_input_string(input_str: str) -> List[Dict[str, str]]:
        json_objects = AgentMrMeeseeks._extract_json_objects(input_str)
        parsed_entries = []
        for json_str in json_objects:
            sanitized_str = AgentMrMeeseeks._sanitize_json(json_str)
            if sanitized_str is None:
                continue

            try:
                parsed_entry = json.loads(sanitized_str)
                if "tool" in parsed_entry:
                    parsed_entries.append(parsed_entry)
            except json.JSONDecodeError as e:
                parsed_entries.append(
                    {"tool": "error-reporter", "input": "Error parsing JSON: %s" % e}
                )
        return [{"tool": entry["tool"], "input": entry.get("input")} for entry in parsed_entries]


if __name__ == "__main__":
    import logging.config

    from spork.tools.python_tools.python_parser import PythonParser
    from spork.tools.python_tools.python_writer import PythonWriter
    from spork.tools.tool_managers.python_parser_tool_manager import PythonParserToolManager
    from spork.tools.tool_managers.python_writer_tool_manager import PythonWriterToolManager
    from spork.tools.utils import get_logging_config

    from ...config import *  # noqa F403

    logging_config = get_logging_config(logging.INFO)
    logging.config.dictConfig(logging_config)

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = []
    exec_tools += build_tools(PythonParserToolManager(python_parser))
    exec_tools += build_tools(PythonWriterToolManager(python_writer))
    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }

    # first_instruction = (
    #     f"Write a file called agent_mr_meeseeks_tool_manager.py which imitates the workflow "
    #     f"of python_parser_tool_manager.py, and is located in the same directory."
    #     f" Implement a single tool named python-agent-python-task, which exposes the agent mr meeseeks iter_task command."
    #     f" Be sure to include a sensible description of the functionality of the tool and include an example."
    # )
    # first_instruction = f"Write a script which builds API documentation for the local repository, put it into an intelligent location. "
    first_instruction = f"Create a script similar to main_static which is used exclusively to run the AgentMrMeeseeks. Use argparse to make all relevant parameters configurable. Name the script main_meeseeks.py. "

    agent = AgentMrMeeseeks(
        initial_payload,
        exec_tools,
        first_instruction,
        stream=True,
        # model="gpt-3.5-turbo",
        # session_id="04f84ef2-c896-49d0-9d20-f50bb7d42f8a",
    )
    # agent.replay_messages()
    agent.run()

    import pdb

    pdb.set_trace()
