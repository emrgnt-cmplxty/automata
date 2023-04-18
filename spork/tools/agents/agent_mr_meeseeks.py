"""
    AgentMrMeeseeks is an autonomous agent that performs the actual work of the Spork
    system. Meeseeks are responsible for executing instructions and reporting
    the results back to the master.

    Example:

        python_parser = PythonParser()
        python_writer = PythonWriter(python_parser)

        exec_tools = []
        exec_tools += PythonParserToolBuilder(python_parser).build_tools()
        exec_tools += PythonWriterToolBuilder(python_writer).build_tools()
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
import sqlite3
import uuid
from typing import Dict, List, Optional

import openai
import regex
import yaml
from langchain.tools.base import BaseTool

from spork.config import *  # noqa F403

from .agent_configs.agent_version import AgentVersion
from .agent_langchain_manager import AgentLangchainManager

CONTINUE_MESSAGE = "Continue"
logger = logging.getLogger(__name__)


class AgentMrMeeseeks:
    def __init__(
        self,
        initial_payload: Dict[str, str],
        initial_instructions: List[Dict[str, str]],
        tools: List[BaseTool],
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
        prompt = self._load_prompt(initial_payload)
        self._init_database()

        if session_id:
            self.session_id = session_id
            self._load_previous_interactions()
        else:
            self.session_id = str(uuid.uuid4())
            self._save_interaction({"role": "system", "content": prompt})
            for instruction in initial_instructions:
                self._save_interaction(instruction)

        logger.info(
            "Initializing with Prompt:%s\n\nAnd SessionId:%s\n" % (prompt, self.session_id)
        )
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    def __del__(self):
        self.conn.close()

    def iter_task(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        """Run the test and report the tool outputs back to the master."""
        logger.info("Running instruction...")
        response_summary = openai.ChatCompletion.create(
            model=self.model, messages=self.messages, temperature=0.7, stream=True
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
        logger.info("-" * 100)

        return None

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

    def _load_prompt(self, initial_payload: Dict[str, str]) -> str:
        """Load the prompt from a config specified at initialization."""
        with open(
            AgentLangchainManager.format_config_path(
                "agent_configs", f"{self.version.value}.yaml"
            ),
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
    def _sanitize_json(json_str: str):
        """Sanitize the JSON string to make it parsable."""
        sanitized_str = json_str.replace("\n", "\\n")
        sanitized_str = sanitized_str.replace("'", '"')
        return sanitized_str

    @staticmethod
    def _extract_json_objects(input_str: str):
        """Extract all JSON objects from the input string."""
        json_pattern = r"\{(?:[^{}]|(?R))*?\}"
        json_matches = regex.findall(json_pattern, input_str, regex.MULTILINE)
        return json_matches

    @staticmethod
    def _parse_input_string(input_str: str) -> List[Dict[str, str]]:
        """Parse the input string and return a dictionary of tool names to tool inputs."""
        json_objects = AgentMrMeeseeks._extract_json_objects(input_str)
        parsed_entries = []
        for json_str in json_objects:
            try:
                sanitized_str = json_str  # _sanitize_json(json_str)
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

    from spork.tools.python_tools.python_parser_tool_builder import (
        PythonParser,
        PythonParserToolBuilder,
    )
    from spork.tools.python_tools.python_writer_tool_builder import (
        PythonWriter,
        PythonWriterToolBuilder,
    )
    from spork.tools.utils import get_logging_config

    from ...config import *  # noqa F403

    logging_config = get_logging_config(logging.INFO)
    logging.config.dictConfig(logging_config)

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = []
    exec_tools += PythonParserToolBuilder(python_parser).build_tools()
    exec_tools += PythonWriterToolBuilder(python_writer).build_tools()
    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }

    # first_instruction = (
    #     f"Write a file called python_meseeks_tool_builder.py which imitates the workflow "
    #     f"of python_parser_tool_builder.py, and is located in the same directory."
    #     f" The tool uses AgentMrMeeseeks to implement a single tool end-point called python-agent-python-task."
    #     f" Be sure to include a sensible description based on the context. You should begin this task by inspecting necessary docstrings."
    # )
    first_instruction = f"Write a script which builds API documentation for the local repository, put it into an intelligent location. "
    initial_instructions = [
        {
            "role": "assistant",
            "content": '{"tool": "meeseeks-initializer", "input": "Hello, I am Mr. Meeseeks, one OpenAI\'s most skilled coders. What coding challenge can I solve for you today?"}',
        },
        {"role": "user", "content": first_instruction},
    ]

    agent = AgentMrMeeseeks(
        initial_payload,
        initial_instructions,
        exec_tools,
        # model="gpt-3.5-turbo",
        # session_id="04f84ef2-c896-49d0-9d20-f50bb7d42f8a",
    )
    # agent.replay_messages()
    next_instruction = agent.iter_task()

    import pdb

    pdb.set_trace()
