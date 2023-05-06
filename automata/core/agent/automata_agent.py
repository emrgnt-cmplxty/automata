import logging
import re
import uuid
from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional, Tuple, cast

import openai
from termcolor import colored

from automata.config import OPENAI_API_KEY
from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import ConfigCategory
from automata.core.agent.agent import Agent
from automata.core.agent.automata_action_extractor import (
    AutomataActionExtractor as ActionExtractor,
)
from automata.core.agent.automata_actions import AgentAction, ResultAction, ToolAction
from automata.core.agent.automata_agent_helpers import (
    format_prompt,
    generate_user_observation_message,
    retrieve_completion_message,
)
from automata.core.agent.automata_database_manager import AutomataDatabaseManager
from automata.core.base.openai import OpenAIChatCompletionResult, OpenAIChatMessage
from automata.core.base.tool import ToolNotFoundError
from automata.core.utils import format_text, load_config

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from automata.core.coordinator.automata_coordinator import (  # This import will only happen during type checking
        AutomataCoordinator,
    )


class AutomataAgent(Agent):
    """
    AutomataAgent is an autonomous agent designed to execute instructions and report
    the results back to the master system. It communicates with the OpenAI API to generate responses
    based on given instructions and manages interactions with various tools.
    """

    CONTINUE_MESSAGE: Final = "Continue, and return a result JSON when finished."
    NUM_DEFAULT_MESSAGES: Final = 3  # Prompt + Assistant Initialization + User Task
    INITIALIZER_DUMMY: Final = "automata_initializer"
    ERROR_DUMMY_TOOL: Final = "error_reporter"

    def __init__(self, config: Optional[AutomataAgentConfig] = None):
        """
        Initialize the AutomataAgent with a given configuration.

        Args:
            config (Optional[AutomataAgentConfig]): The agent configuration to use.
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

    def run(self) -> str:
        """
        Runs the agent and iterates through the tasks until a result is produced or the max iterations are exceeded.

        Returns:
            str: The final result or an error message if the result wasn't found in time.
        """
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
        """
        Executes a single iteration of the task and returns the latest assistant and user messages.

        Raises:
            ValueError: If the agent has already completed its task.

        Returns:
            Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]: Latest assistant and user messages, or None if the task is completed.
        """
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
            self._save_message(
                "assistant",
                self._parse_completion_message(completion_message)
                if not self.eval_mode
                else response_text,
            )
            return None

        assistant_message = self._save_message("assistant", response_text)
        user_message = self._save_message(
            "user",
            generate_user_observation_message(observations)
            if len(observations) > 0
            else AutomataAgent.CONTINUE_MESSAGE,
        )

        return (assistant_message, user_message)

    def replay_messages(self) -> str:
        """
        Replays the messages in the conversation and returns the completion message if found.

        Returns:
            str: The completion message if found, otherwise a message indicating that no completion message was found.
        """
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

    def modify_last_instruction(self, updated_instruction: str) -> None:
        """
        Modifies the last instruction in the conversation with a new message.

        Args:
            new_instruction (str): The new instruction to replace the last message.

        Raises:
            ValueError: If the last message is not a user message.
        """
        previous_message = self.messages[-1]
        if previous_message.role != "user":
            raise ValueError("Cannot modify the last instruction if it was not a user message.")
        self.messages[-1] = OpenAIChatMessage(
            role=previous_message.role, content=updated_instruction
        )

    def get_non_instruction_messages(self) -> List[OpenAIChatMessage]:
        """
        Retrieves all messages in the conversation that are not system instructions.

        Returns:
            List[OpenAIChatMessage]: A list of non-instruction messages.
        """
        return self.messages[self.NUM_DEFAULT_MESSAGES :]

    def _setup(self):
        """
        Sets up the agent, initializing the session and loading previous interactions if applicable.
        """
        openai.api_key = OPENAI_API_KEY
        if "tools" in self.instruction_input_variables:
            self.instruction_payload.tools = self._build_tool_message()
        system_instruction = format_prompt(
            self.instruction_payload, self.system_instruction_template
        )
        session_id = self.session_id if self.session_id else str(uuid.uuid4())
        self.database_manager: AutomataDatabaseManager = AutomataDatabaseManager(session_id)

        self.database_manager._init_database()
        if self.session_id:
            self.messages = self.database_manager._load_previous_interactions()
        else:
            self.session_id = session_id
            self._save_message("system", system_instruction)
            initial_messages = self._build_initial_messages(
                {"user_input_instructions": self.instructions}
            )
            for message in initial_messages:
                self._save_message(message.role, message.content)

        self.instruction_payload.validate_fields(self.instruction_input_variables)

        logger.debug("Initializing with System Instruction:%s\n\n" % system_instruction)
        logger.debug("-" * 60)
        logger.debug("Session ID: %s" % self.session_id)
        logger.debug("-" * 60)

    def _generate_observations(self, response_text: str) -> Dict[str, str]:
        """
        Processes the agent's response text and generates observations.

        Args:
            response_text (str): The agent's response text.

        Returns:
            Dict[str, str]: A dictionary of observations.
        """
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
        """
        Executes a tool with the given name and input.

        Args:
            tool_name (str): The name of the tool to execute.
            tool_input (List[str]): The input arguments for the tool.

        Returns:
            str: The output of the executed tool.
        """
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
            return ToolNotFoundError(tool_name).__str__()

        return cast(str, tool_output)

    def _build_tool_message(self):
        """
        Builds a message containing information about all available tools.

        Returns:
            str: A formatted string containing the names and descriptions of all available tools.
        """
        return "Tools:\n" + "".join(
            [
                f"\n{tool.name}: {tool.description}\n"
                for toolkit in self.llm_toolkits.values()
                for tool in toolkit.tools
            ]
        )

    def _parse_completion_message(self, completion_message: str) -> str:
        """
        Parses the completion message and replaces placeholders with actual tool outputs.

        Args:
            completion_message (str): The completion message with placeholders.

        Returns:
            str: The parsed completion message with placeholders replaced by tool outputs.
        """
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
        """
        Builds the initial messages for the agent's conversation.

        Args:
            formatters (Dict[str, str]): A dictionary of formatters used to format the messages.

        Returns:
            List[OpenAIChatMessage]: A list of initial messages for the conversation.
        """
        assert "user_input_instructions" in formatters
        formatters["initializer_dummy_tool"] = AutomataAgent.INITIALIZER_DUMMY

        messages_config = load_config(ConfigCategory.INSTRUCTION.value, self.instruction_version)
        initial_messages = messages_config["initial_messages"]

        input_messages = []
        for message in initial_messages:
            input_message = format_text(formatters, message["content"])
            input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

        return input_messages

    def _stream_message(self, response_summary: Any):
        """
        Streams the response message from the agent.

        Args:
            response_summary (Any): The response summary from the agent.

        Returns:
            str: The streamed response text.
        """
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

    def _save_message(self, role: str, content: str) -> OpenAIChatMessage:
        """
        Saves the messagee for the agent.

        Args:
            role (str): The role of the messagee.
            content (str): The content of the messagee.
        """
        self.database_manager.put_message(role, content, len(self.messages))
        message = OpenAIChatMessage(role=role, content=content)
        self.messages.append(message)
        return message


class MasterAutomataAgent(AutomataAgent):
    """
    A MasterAutomataAgent is a specialized AutomataAgent that can interact with an AutomataCoordinator
    to execute and manipulate other AutomataAgents as part of the conversation.
    """

    def __init__(self, agent_config, *args, **kwargs):
        """Initialize the MasterAutomataAgent with agent_config and other optional arguments."""
        super().__init__(agent_config, *args, **kwargs)
        self.coordinator = None

    def set_coordinator(self, coordinator: "AutomataCoordinator"):
        """
        Set the coordinator for the MasterAutomataAgent.

        Args:
            coordinator (AutomataCoordinator): An instance of an AutomataCoordinator.
        """
        self.coordinator = coordinator

    def _generate_observations(self, response_text: str) -> Dict[str, str]:
        """Process the messages in the conversation and extract agent actions.

        Args:
            response_text (str): The response text from the conversation.

        Returns:
            Dict[str, str]: A dictionary containing the agent outputs, indexed by their query names.
        """
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
        """
        Generate the result from the specified agent_action using the coordinator.

        Args:
            agent_action (AgentAction): An instance of an AgentAction to be executed.

        Returns:
            str: The output generated by the agent.
        """
        return self.coordinator.run_agent(agent_action)

    def _add_agent_observations(
        self,
        observations: Dict[str, str],
        agent_observations: Dict[str, str],
        agent_action: AgentAction,
    ) -> None:
        """
        Add agent observations to the given observations dictionary.

        Args:
            observations (Dict[str, str]): The existing observations dictionary.
            agent_observations (Dict[str, str]): The agent observations to be added.
            agent_action (AgentAction): An instance of an AgentAction for which the observations are generated.
        """
        for observation in agent_observations:
            agent_observation = observation.replace(
                "return_result_0", agent_action.agent_query.replace("query", "output")
            )
            observations[agent_observation] = agent_observations[observation]

    def _parse_completion_message(self, completion_message: str) -> str:
        """
        Parse the completion message and replace the tool outputs with their appropriate values.

        Args:
            completion_message (str): The completion message to be parsed and modified.

        Returns:
            str: The modified completion message with replaced tool outputs.
        """
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
        """
        Create a MasterAutomataAgent from an existing AutomataAgent.

        Args:
            agent (AutomataAgent): An instance of an AutomataAgent to be converted to a MasterAutomataAgent.

        Returns:
            MasterAutomataAgent: A new instance of MasterAutomataAgent with the same properties as the input agent.
        """
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
