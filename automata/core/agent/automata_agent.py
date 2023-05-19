import logging
import re
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
from automata.core.agent.automata_agent_utils import (
    generate_user_observation_message,
    retrieve_completion_message,
)
from automata.core.agent.automata_database_manager import AutomataConversationDatabase
from automata.core.base.openai import OpenAIChatCompletionResult, OpenAIChatMessage
from automata.core.base.tool import ToolNotFoundError
from automata.core.utils import format_text, load_config

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from automata.core.coordinator.automata_coordinator import AutomataCoordinator


class AutomataAgent(Agent):
    """
    AutomataAgent is an autonomous agent designed to execute instructions and report
    the results back to the main system. It communicates with the OpenAI API to generate responses
    based on given instructions and manages interactions with various tools.
    """

    CONTINUE_MESSAGE: Final = "Continue, and return a result JSON when finished."
    NUM_DEFAULT_MESSAGES: Final = 3  # Prompt + Assistant Initialization + User Task
    INITIALIZER_DUMMY: Final = "automata_initializer"
    ERROR_DUMMY_TOOL: Final = "error_reporter"

    def __init__(self, instructions: str, config: Optional[AutomataAgentConfig] = None):
        """
        Initializes an AutomataAgent.
        """

        if config is None:
            config = AutomataAgentConfig()
        self.config = config
        self.completed = False
        self.instructions = instructions
        self.messages: List[OpenAIChatMessage] = []
        self.coordinator: Optional["AutomataCoordinator"] = None

    def set_coordinator(self, coordinator: "AutomataCoordinator"):
        """
        Set the coordinator for the AutomataAgent, necessary for the main agent.

        Args:
            coordinator (AutomataCoordinator): An instance of an AutomataCoordinator.
        """

        self.coordinator = coordinator

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
            model=self.config.model,
            messages=[ele.to_dict() for ele in self.messages],
            temperature=self.config.temperature,
            stream=self.config.stream,
        )
        response_text = (
            self._stream_message(response_summary)
            if self.config.stream
            else OpenAIChatCompletionResult(raw_data=response_summary).get_completion()
        )

        observations = self._generate_observations(response_text)

        completion_message = retrieve_completion_message(observations)
        if completion_message is not None:
            self.completed = True
            self._save_message(
                "assistant",
                self._parse_completion_message(completion_message)
                if not self.config.eval_mode
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
            if (
                len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES
                >= self.config.max_iters * 2
            ):
                return "Result was not found before iterations exceeded max limit."
            latest_responses = self.iter_task()
        return self.messages[-1].content

    def setup(self):
        openai.api_key = OPENAI_API_KEY
        if not self.config.session_id:
            raise ValueError("Config was not properly initialized.")
        self.database_manager: AutomataConversationDatabase = AutomataConversationDatabase(
            self.config.session_id
        )
        self.database_manager._init_database()
        if not self.config.is_new_agent:
            self.messages = self.database_manager.get_conversations()
        else:
            if not self.config.system_instruction:
                raise ValueError("System instruction must be provided if new agent.")

            self._save_message("system", self.config.system_instruction)
            initial_messages = self._build_initial_messages(
                {"user_input_instructions": self.instructions}
            )
            for message in initial_messages:
                self._save_message(message.role, message.content)

        logger.debug(
            "Initializing with System Instruction:%s\n\n" % self.config.system_instruction
        )
        logger.debug("-" * 60)
        logger.debug("Session ID: %s" % self.config.session_id)
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
            elif isinstance(action, AgentAction):
                if action.agent_version.value == AutomataAgent.INITIALIZER_DUMMY:
                    continue
                agent_output = self._execute_agent(action)
                query_name = action.agent_query.replace("query", "output")
                outputs[query_name] = agent_output

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

        for toolkit in self.config.llm_toolkits.values():
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

    def _has_helper_agents(self) -> bool:
        """
        The existence of a coordinator agent indicates that there are helper agents.

        Returns:
            bool: True if there are helper agents, False otherwise.
        """
        return self.coordinator is not None

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
        if self._has_helper_agents():
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

        messages_config = load_config(
            ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
        )
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
        print(colored(f"\n>>> {self.config.config_name.value} Agent:", "green"))
        latest_accumulation = ""
        stream_separator = " "
        response_text = ""
        for chunk in response_summary:
            if "content" in chunk["choices"][0]["delta"]:
                chunk_content = chunk["choices"][0]["delta"]["content"]
                chunk_content.replace("\\n", "\n")
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

    def _execute_agent(self, agent_action: AgentAction) -> str:
        """
        Generate the result from the specified agent_action using the coordinator.

        Args:
            agent_action (AgentAction): An instance of an AgentAction to be executed.

        Returns:
            str: The output generated by the agent.
        """
        if not self.coordinator:
            raise Exception("Agent has no coordinator.")

        return self.coordinator.run_agent(agent_action)
