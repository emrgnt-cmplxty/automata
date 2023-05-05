"""
    AutomataAgent is an autonomous agent that performs the actual work of the Automata
    system. Automata are responsible for executing instructions and reporting
    the results back to the master.

    Example:

        llm_toolkits = build_llm_toolkits(tools_list, **inputs)

        config_version = AgentConfigVersion.AUTOMATA_MASTER_PROD
        agent_config = AutomataAgentConfig.load(config_version)
        agent = (AutomataAgentBuilder.from_config(agent_config)
            .with_llm_toolkits(llm_toolkits)
            .with_instructions(instructions)
            .with_model(model)
            .build())

        agent.run()

        TODO - Add error checking to ensure that we don't terminate when
               our previous result returned an error

        TODO - Think about approach behind retrieve_completion_message
             - Right now, the job terminates when we get our first completion message
               e.g. return_result_0
               The correct thing to do would be to ensure we complete all tasks
               But before adding this cpability, we need to continue
               polishing the framework

        TODO - Add field for instruction config version to agent + builder
        TODO - Change _parse_completion_message to take action string from extractor
"""
import logging
import re
import sqlite3
import uuid
from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional, Tuple, cast

import openai
from termcolor import colored

from automata.config import CONVERSATION_DB_NAME, OPENAI_API_KEY
from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import ConfigCategory
from automata.core.agent.agent import Agent
from automata.core.agent.automata_action_extractor import (
    AutomataActionExtractor as ActionExtractor,
)
from automata.core.agent.automata_actions import AgentAction, ResultAction, ToolAction
from automata.core.agent.automata_agent_helpers import (
    generate_user_observation_message,
    retrieve_completion_message,
)
from automata.core.base.openai import OpenAIChatCompletionResult, OpenAIChatMessage
from automata.core.utils import format_prompt, load_config

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from automata.core.coordinator.automata_coordinator import (  # This import will only happen during type checking
        AutomataCoordinator,
    )


class AutomataAgent(Agent):
    """
    AutomataAgent is an autonomous agent that performs the actual work of the Automata
    system. Automata are responsible for executing instructions and reporting
    the results back to the master.
    """

    CONTINUE_MESSAGE: Final = "Continue, and return a result JSON when finished."
    NUM_DEFAULT_MESSAGES: Final = 3  # Prompt + Assistant Initialization + User Task
    INITIALIZER_DUMMY: Final = "automata_initializer"
    ERROR_DUMMY_TOOL: Final = "error_reporter"

    def __init__(self, config: Optional[AutomataAgentConfig] = None):
        """
        Args:
            config (Optional[AutomataAgentConfig]): The agent config to use
        Methods:
            iter_task(instructions: List[Dict[str, str]]) -> Dict[str, str]: Iterates through the instructions and returns the next instruction.
            modify_last_instruction(new_instruction: str) -> None
            replay_messages() -> List[Dict[str, str]]: Replays agent messages buffer.
            run() -> str: Runs the agent.
            get_non_instruction_messages() -> List[Dict[str, str]]: Returns all messages that are not instructions.
        """
        if config is None:
            config = AutomataAgentConfig()
        self.instruction_payload = config.instruction_payload
        self.llm_toolkits = config.llm_toolkits
        self.instructions = config.instructions
        self.config_version = config.config_version
        self.system_instruction_template = config.system_instruction_template
        self.instruction_input_variables = config.instruction_input_variables
        self.model = config.model
        self.stream = config.stream
        self.verbose = config.verbose
        self.max_iters = config.max_iters
        self.temperature = config.temperature
        self.instruction_version = config.instruction_version
        self.completed = False
        self.eval_mode = False
        self.messages: List[OpenAIChatMessage] = []
        self.session_id = config.session_id
        self.conn: Optional[sqlite3.Connection] = None

    def __del__(self):
        """Close the connection to the agent."""
        if self.conn:
            self.conn.close()

    def run(self) -> str:
        latest_responses = self.iter_task()
        while latest_responses is not None:
            # Each iteration adds two messages, one from the assistant and one from the user
            # If we have equal to or more than 2 * max_iters messages (less the default messages),
            # then we have exceeded the max_iters
            if len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES >= self.max_iters * 2:
                return "Result was not found before iterations exceeded max limit."
            latest_responses = self.iter_task()
        return self.messages[-1].content

    def iter_task(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
        """Run the test and report the tool outputs back to the master."""
        if self.completed:
            raise ValueError("Cannot run an agent that has already completed.")
        response_summary = openai.ChatCompletion.create(
            model=self.model,
            messages=[ele.to_dict() for ele in self.messages],
            temperature=self.temperature,
            stream=self.stream,
        )
        response_text = (
            self._stream_message(response_summary)
            if self.stream
            else OpenAIChatCompletionResult(raw_data=response_summary).get_completion()
        )

        observations = self._generate_observations(response_text)

        completion_message = retrieve_completion_message(observations)
        if completion_message is not None:
            self.completed = True
            self._save_interaction(
                "assistant",
                self._parse_completion_message(completion_message)
                if not self.eval_mode
                else response_text,
            )
            return None

        assistant_message = self._save_interaction("assistant", response_text)
        user_message = self._save_interaction(
            "user",
            generate_user_observation_message(observations)
            if len(observations) > 0
            else AutomataAgent.CONTINUE_MESSAGE,
        )

        return (assistant_message, user_message)

    def replay_messages(self) -> str:
        """Replay the messages in the conversation."""
        if len(self.messages) == 0:
            logger.debug("No messages to replay.")
            return "No messages to replay."
        for message in self.messages[self.NUM_DEFAULT_MESSAGES :]:
            observations = self._generate_observations(message.content)
            completion_message = retrieve_completion_message(observations)
            if completion_message:
                return completion_message
            logger.debug("Role:\n%s\n\nMessage:\n%s\n" % (message.role, message.content))
            logger.debug("Processing message content =  %s" % message.content)
            logger.debug("\nProcessed Outputs:\n%s\n" % observations)
            logger.debug("-" * 60)
        return "No completion message found."

    def modify_last_instruction(self, new_instruction: str) -> None:
        """Extend the last instructions with a new message."""
        previous_message = self.messages[-1]
        if previous_message.role != "user":
            raise ValueError("Cannot modify the last instruction if it was not a user message.")
        self.messages[-1] = OpenAIChatMessage(role=previous_message.role, content=new_instruction)

    def get_non_instruction_messages(self) -> List[OpenAIChatMessage]:
        """Get the non-instruction messages."""
        return self.messages[self.NUM_DEFAULT_MESSAGES :]

    def _setup(self):
        """Setup the agent."""
        openai.api_key = OPENAI_API_KEY
        if "tools" in self.instruction_input_variables:
            self.instruction_payload["tools"] = self._build_tool_message()
        system_instruction = format_prompt(
            self.instruction_payload, self.system_instruction_template
        )
        self._init_database()
        if self.session_id:
            self._load_previous_interactions()
        else:
            self.session_id = str(uuid.uuid4())
            self._save_interaction("system", system_instruction)
            initial_messages = self._build_initial_messages(
                {"user_input_instructions": self.instructions}
            )
            for message in initial_messages:
                self._save_interaction(message.role, message.content)
        logger.debug("Initializing with System Instruction:%s\n\n" % system_instruction)
        logger.debug("-" * 60)
        if set(self.instruction_input_variables) != set(list(self.instruction_payload.keys())):
            raise ValueError(f"Initial payload does not match instruction_input_variables.")
        logger.debug("Session ID: %s" % self.session_id)
        logger.debug("-" * 60)

    def _generate_observations(self, response_text: str) -> Dict[str, str]:
        """Process the messages in the conversation."""
        outputs = {}
        actions = ActionExtractor.extract_actions(response_text)
        for action in actions:
            if isinstance(action, ToolAction):
                (tool_query, tool_name, tool_input) = (
                    action.tool_query,
                    action.tool_name,
                    action.tool_args,
                )
                # Skip the initializer dummy tool which exists only for providing context
                if tool_name == AutomataAgent.INITIALIZER_DUMMY:
                    continue
                if tool_name == AutomataAgent.ERROR_DUMMY_TOOL:
                    # Input becomes the output when an error is registered
                    outputs[tool_query.replace("query", "output")] = cast(str, tool_input)
                else:
                    tool_output = self._execute_tool(tool_name, tool_input)
                    outputs[tool_query.replace("query", "output")] = tool_output
            elif isinstance(action, ResultAction):
                (result_name, result_outputs) = (action.result_name, action.result_outputs)
                # Skip the return result indicator which exists only for marking the return result
                outputs[result_name] = "\n".join(result_outputs)

        return outputs

    def _execute_tool(self, tool_name: str, tool_input: List[str]) -> str:
        """Execute the tool with the given name and input."""
        tool_found = False
        tool_output = None

        for toolkit in self.llm_toolkits.values():
            for tool in toolkit.tools:
                if tool.name == tool_name:
                    processed_tool_input = [ele if ele != "None" else None for ele in tool_input]
                    tool_output = tool.run(tuple(processed_tool_input), verbose=False)
                    tool_found = True
                    break
            if tool_found:
                break

        if not tool_found:
            error_message = f"Error: Tool '{tool_name}' not found."
            return error_message

        return cast(str, tool_output)

    def _init_database(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(CONVERSATION_DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "\n            CREATE TABLE IF NOT EXISTS interactions (\n                session_id INTEGER,\n                interaction_id INTEGER,\n                role TEXT,\n                content TEXT,\n                PRIMARY KEY (session_id, interaction_id)\n            )\n            "
        )
        self.conn.commit()

    def _save_interaction(self, role: str, content: str) -> OpenAIChatMessage:
        """Save the interaction to the database."""
        assert self.session_id is not None, "Session ID is not set."
        assert self.conn is not None, "Database connection is not set."
        interaction = OpenAIChatMessage(role=role, content=content)
        interaction_id = len(self.messages)
        self.cursor.execute(
            "INSERT INTO interactions (session_id, interaction_id, role, content) VALUES (?, ?, ?, ?)",
            (self.session_id, interaction_id, role, content),
        )
        self.conn.commit()
        self.messages.append(interaction)
        return interaction

    def _load_previous_interactions(self):
        """Load the previous interactions from the database."""
        self.cursor.execute(
            "SELECT role, content FROM interactions WHERE session_id = ? ORDER BY interaction_id ASC",
            (self.session_id,),
        )
        self.messages = [
            OpenAIChatMessage(role=role, content=content)
            for (role, content) in self.cursor.fetchall()
        ]

    def _build_tool_message(self):
        """Builds a message containing all tools and their descriptions."""
        return "Tools:\n" + "".join(
            [
                f"\n{tool.name}: {tool.description}\n"
                for toolkit in self.llm_toolkits.values()
                for tool in toolkit.tools
            ]
        )

    def _parse_completion_message(self, completion_message: str) -> str:
        """Parse the completion message and replace the tool outputs."""
        outputs = {}
        for message in self.messages:
            pattern = r"-\s(tool_output_\d+)\s+-\s(.*?)(?=-\s(tool_output_\d+)|$)"
            matches = re.finditer(pattern, message.content, re.DOTALL)
            for match in matches:
                tool_name, tool_output = match.group(1), match.group(2).strip()
                outputs[tool_name] = tool_output

        for output_name in outputs:
            completion_message = completion_message.replace(
                f"{{{output_name}}}", outputs[output_name]
            )
        return completion_message

    def _build_initial_messages(self, formatters: Dict[str, str]) -> List[OpenAIChatMessage]:
        """Build the initial messages."""
        assert "user_input_instructions" in formatters
        formatters["initializer_dummy_tool"] = AutomataAgent.INITIALIZER_DUMMY

        messages_config = load_config(ConfigCategory.INSTRUCTION.value, self.instruction_version)
        initial_messages = messages_config["initial_messages"]

        input_messages = []
        for message in initial_messages:
            input_message = format_prompt(formatters, message["content"])
            input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

        return input_messages

    def _stream_message(self, response_summary: Any):
        """Stream the response message."""
        print(colored("\n>>>", "green", attrs=["blink"]) + colored(" Agent:", "green"))
        latest_accumulation = ""
        stream_separator = " "
        response_text = ""
        for chunk in response_summary:
            if "content" in chunk["choices"][0]["delta"]:
                chunk_content = chunk["choices"][0]["delta"]["content"]
                latest_accumulation += chunk_content
                response_text += chunk_content
            if stream_separator in latest_accumulation:
                words = latest_accumulation.split(stream_separator)
                for word in words[:-1]:
                    print(colored(str(word), "green"), end=" ", flush=True)
                latest_accumulation = words[-1]
        print(colored(str(latest_accumulation), "green"))
        return response_text


class MasterAutomataAgent(AutomataAgent):
    """A master automata agent that works with the coordinater to manipulate other automata agents."""

    def __init__(self, agent_config, *args, **kwargs):
        """Initialize the master automata agent."""
        super().__init__(agent_config, *args, **kwargs)
        self.coordinator = None

    def set_coordinator(self, coordinator: "AutomataCoordinator"):
        """Set the coordinator."""
        self.coordinator = coordinator

    def _generate_observations(self, response_text: str) -> Dict[str, str]:
        """Process the messages in the conversation."""
        outputs = super()._generate_observations(response_text)
        actions = ActionExtractor.extract_actions(response_text)
        for agent_action in actions:
            if isinstance(agent_action, AgentAction):
                if agent_action.agent_version.value == AutomataAgent.INITIALIZER_DUMMY:
                    continue
                agent_output = self._execute_agent(agent_action)
                query_name = agent_action.agent_query.replace("query", "output")
                outputs[query_name] = agent_output
        return outputs

    def _execute_agent(self, agent_action) -> str:
        """Generate the agent result."""
        return self.coordinator.run_agent(agent_action)

    def _add_agent_observations(
            self,
            observations: Dict[str, str],
            agent_observations: Dict[str, str],
            agent_action: AgentAction,
    ) -> None:
        """Generate the agent observations."""
        for observation in agent_observations:
            agent_observation = observation.replace(
                "return_result_0", agent_action.agent_query.replace("query", "output")
            )
            observations[agent_observation] = agent_observations[observation]

    def _parse_completion_message(self, completion_message: str) -> str:
        """Parse the completion message and replace the tool outputs."""
        completion_message = super()._parse_completion_message(completion_message)
        outputs = {}
        for message in self.messages:
            pattern = r"-\s(agent_output_\d+)\s+-\s(.*?)(?=-\s(agent_output_\d+)|$)"
            matches = re.finditer(pattern, message.content, re.DOTALL)
            for match in matches:
                agent_version, agent_output = match.group(1), match.group(2).strip()
                outputs[agent_version] = agent_output

        for output_name in outputs:
            completion_message = completion_message.replace(
                f"{{{output_name}}}", outputs[output_name]
            )
        return completion_message

    # TODO - Can we implement this more cleanly?
    @classmethod
    def from_agent(cls, agent: AutomataAgent) -> "MasterAutomataAgent":
        """Create a master automata agent from an automata agent."""
        master_agent = cls(None)
        master_agent.llm_toolkits = agent.llm_toolkits
        master_agent.instructions = agent.instructions
        master_agent.model = agent.model
        master_agent.instruction_payload = agent.instruction_payload
        master_agent.config_version = agent.config_version
        master_agent.system_instruction_template = agent.system_instruction_template
        master_agent.instruction_input_variables = agent.instruction_input_variables
        master_agent.stream = agent.stream
        master_agent.verbose = agent.verbose
        master_agent.max_iters = agent.max_iters
        master_agent.temperature = agent.temperature
        master_agent.session_id = agent.session_id
        master_agent.completed = False
        master_agent._setup()
        return master_agent