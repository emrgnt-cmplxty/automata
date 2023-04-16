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


class AgentMrMeeseeks:
    def __init__(
        self,
        initial_payload: Dict[str, str],
        initial_instructions: List[Dict[str, str]],
        tools: List[BaseTool],
        version: AgentVersion = AgentVersion.RETRIEVAL_V2,
        model: str = "gpt-4",
        session_id: Optional[str] = None,
    ):
        """
        AgentMrMeeseeks is an autonomous agent that performs the actual work of the Spork
        system. Meeseeks are responsible for executing instructions and reporting
        the results back to the master.
        """

        # Initialize OpenAI API Key
        openai.api_key = OPENAI_API_KEY  # noqa F405

        # Initialize state variables
        self.model = model
        self.version = version
        self.tools = tools
        self.messages: List[Dict[str, str]] = []

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

        # print("Initializing with Prompt:%s\n\nAnd SessionId:%s\n" % (prompt, self.session_id))
        print("Initializing SessionId: %s\n" % (self.session_id))

    def __del__(self):
        self.conn.close()

    def iter_task(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        """Run the test and report the tool outputs back to the master."""
        response_summary = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
        )
        response_text = response_summary["choices"][0]["message"]["content"]
        processed_inputs = self._process_input(response_text)
        self._save_interaction({"role": "assistant", "content": response_text})

        if len(processed_inputs) > 0:
            message = "{" + "\n"
            for i, output in enumerate(processed_inputs):
                message += f'"output_{i}": {(output)}, \n'
            message += "}"
            self._save_interaction({"role": "user", "content": message})
            return processed_inputs

        # If there are no outputs, then the user has must respond to continue
        self._save_interaction({"role": "user", "content": CONTINUE_MESSAGE})
        return None

    def replay_messages(self):
        """Replay the messages in the conversation."""
        for message in self.messages:
            if message["role"] == "user":
                continue
            print("Role:\n%s\n\nMessage:\n%s\n" % (message["role"], message["content"]))
            print("Processing message content = ", message["content"])
            processed_outputs = self._process_input(message["content"])
            print("\nProcessed Outputs:\n%s\n" % processed_outputs)
            print("-" * 100)

    def _load_prompt(self, initial_payload: Dict[str, str]):
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

    def _process_input(self, response_text: str):
        """Process the messages in the conversation."""
        tool_calls = AgentMrMeeseeks._parse_input_string(response_text)
        outputs = []
        print("Tool Calls len = %s" % (len(tool_calls.keys())))
        for tool, tool_input in tool_calls.items():
            if tool == "error-reporter":
                # In the event of an error, the tool_input becomes the output, as it is now a parsing error
                tool_output = tool_input
                outputs.append(tool_input)

            for tool_instance in self.tools:
                if tool_instance.name == tool:
                    tool_output = tool_instance.run(tool_input, verbose=True)
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
    def _parse_input_string(input_str: str) -> Dict[str, str]:
        """Parse the input string and return a dictionary of tool names to tool inputs."""
        print("Receiving input string = ", input_str)
        json_objects = AgentMrMeeseeks._extract_json_objects(input_str)
        print("json_objects = ", json_objects)
        parsed_entries = []
        for json_str in json_objects:
            try:
                sanitized_str = json_str  # _sanitize_json(json_str)
                parsed_entry = json.loads(sanitized_str)
                print("parsed_entry = ", parsed_entry)
                if "tool" in parsed_entry:
                    parsed_entries.append(parsed_entry)
            except json.JSONDecodeError as e:
                print("error parsing json")
                parsed_entries.append(
                    {"tool": "error-reporter", "input": "Error parsing JSON: %s" % e}
                )
        print("parsed_entries = ", parsed_entries)
        return {entry["tool"]: entry.get("input") for entry in parsed_entries}


if __name__ == "__main__":
    from spork.tools.python_tools.python_parser_tool_builder import (
        PythonParser,
        PythonParserToolBuilder,
    )
    from spork.tools.python_tools.python_writer_tool_builder import (
        PythonWriter,
        PythonWriterToolBuilder,
    )

    from ...config import *  # noqa F403

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = []
    exec_tools += PythonParserToolBuilder(python_parser).build_tools()
    exec_tools += PythonWriterToolBuilder(python_writer).build_tools()
    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }
    first_instruction = (
        f"Write a file called python_meseeks_tool_builder.py which imitates the workflow "
        f"of python_parser_tool_builder.py, and is located in the same directory."
        f" The tool uses AgentMrMeeseeks to implement a single tool end-point called python-agent-python-task."
        f" Be sure to include a sensible description based on the context. You should begin this task by inspecting necessary docstrings."
    )
    initial_instructions = [
        {
            "role": "assistant",
            "content": '{"tool": "meeseeks-initializer", "input": "Hello, I am Mr. Meeseeks, look at me."}',
        },
        {"role": "user", "content": first_instruction},
    ]
    agent = AgentMrMeeseeks(
        initial_payload,
        initial_instructions,
        exec_tools,
        session_id="ec8172f1-2a75-4fed-9278-8476cfc1d967",
    )
    agent.replay_messages()
    # next_instruction = agent.iter_task()

    # pdb.set_trace()
    # print("Next Instruction: %s" % next_instruction)
