import logging
from typing import Dict, Final, List, Sequence

from automata.config.base import ConfigCategory
from automata.config.openai_agent import AutomataOpenAIAgentConfig
from automata.core.agent.error import (
    AgentDatabaseError,
    AgentMaxIterError,
    AgentResultError,
    AgentStopIteration,
)
from automata.core.llm.completion import (
    LLMChatMessage,
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.core.llm.providers.openai import (
    OpenAIAgent,
    OpenAIChatCompletionProvider,
    OpenAIChatMessage,
    OpenAIFunction,
    OpenAITool,
)
from automata.core.utils import format_text, load_config

logger = logging.getLogger(__name__)


class AutomataOpenAIAgent(OpenAIAgent):
    """
    AutomataOpenAIAgent is an autonomous agent designed to execute instructions and report
    the results back to the main system. It communicates with the OpenAI API to generate
    responses based on given instructions and manages interactions with various tools.
    """

    CONTINUE_MESSAGE: Final = "Continue.."
    SUCCESS_PREFIX: Final = "Execution Result:\n"

    def __init__(self, instructions: str, config: AutomataOpenAIAgentConfig) -> None:
        """
        Initializes an AutomataAgent.

        Args:
            instructions (str): The instructions to be executed by the agent.
            config (AutomataAgentConfig): The configuration for the agent. Defaults to None.
        """
        super().__init__(instructions)
        self.config = config
        self.iteration_count = 0
        self._setup()

    def __iter__(self):
        return self

    def __next__(self) -> LLMIterationResult:
        """
        Executes a single iteration of the task and returns the latest assistant and user messages.

        Raises:
            AgentError: If the agent has already completed its task or exceeded the maximum number of iterations.

        Returns:
            LLMIterationResult Latest assistant and user messages, or None if the task is completed.
        """
        if self.completed or self.iteration_count >= self.config.max_iterations:
            raise AgentStopIteration

        assistant_message = self.chat_provider.get_next_assistant_completion()
        self.conversation.add_message(assistant_message)
        self.iteration_count += 1

        user_message = self._get_next_user_response(assistant_message)
        self.conversation.add_message(user_message)

        return (assistant_message, user_message)

    @property
    def tools(self) -> List[OpenAITool]:
        """
        Returns:
            List[OpenAITool]: The tools for the agent.
        """
        tools = []
        for tool in self.config.tools:
            if not isinstance(tool, OpenAITool):
                raise ValueError(f"Invalid tool type: {type(tool)}")
            tools.append(tool)
        tools.append(self._get_termination_tool())
        return tools

    @property
    def functions(self) -> List[OpenAIFunction]:
        """
        Returns:
            List[OpenAIFunction]: The available functions for the agent.
        """
        return [ele.openai_function for ele in self.tools]

    def run(self) -> str:
        """
        Runs the agent and iterates through the tasks until a result is produced
        or the max iterations are exceeded.

        The agent must be setup before running.
        This implementation calls next() on self until a AgentStopIteration exception is raised,
        at which point it will break out of the loop and return the final result.

        Returns:
            str: The final agent output or an error message if the result wasn't found before an exception.

        Raises:
            AgentError:
                If the agent exceeds the maximum number of iterations.
                If the agent does not produce a result.
        """
        while True:
            try:
                next(self)
            except AgentStopIteration:
                break

        last_message = self.conversation.get_latest_message()
        if self.iteration_count >= self.config.max_iterations:
            raise AgentMaxIterError("The agent exceeded the maximum number of iterations.")
        if not self.completed or not isinstance(last_message, OpenAIChatMessage):
            raise AgentResultError("The agent did not produce a result.")
        if not last_message.content:
            raise AgentResultError("The agent produced an empty result.")
        return last_message.content

    def set_database_provider(self, provider: LLMConversationDatabaseProvider) -> None:
        if not isinstance(provider, LLMConversationDatabaseProvider):
            raise AgentDatabaseError(f"Invalid database provider type: {type(provider)}")
        if self.database_provider:
            raise AgentDatabaseError("The database provider has already been set.")
        self.database_provider = provider
        self.conversation.register_observer(provider)

    def _build_initial_messages(
        self, instruction_formatter: Dict[str, str]
    ) -> Sequence[LLMChatMessage]:
        """
        Builds the initial messages for the agent's conversation.
        The messages are built from the initial messages in the instruction config.
        All messages are formatted using the given instruction_formatter.
        """
        assert "user_input_instructions" in instruction_formatter

        messages_config = load_config(
            ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
        )
        initial_messages = messages_config["initial_messages"]

        input_messages = []
        for message in initial_messages:
            input_message = format_text(instruction_formatter, message["content"])
            input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

        return input_messages

    def _get_next_user_response(self, assistant_message: OpenAIChatMessage) -> OpenAIChatMessage:
        """
        Generates a user message based on the assistant's message.
        This is done by checking if the assistant's message contains a function call.
        If it does, then the corresponding tool is run and the result is returned.
        Otherwise, the user is prompted to continue the conversation.
        """
        if assistant_message.function_call:
            for tool in self.tools:
                if assistant_message.function_call.name == tool.openai_function.name:
                    result = tool.run(assistant_message.function_call.arguments)
                    return OpenAIChatMessage(
                        role="user", content=f"{AutomataOpenAIAgent.SUCCESS_PREFIX}{result}"
                    )

        return OpenAIChatMessage(role="user", content=AutomataOpenAIAgent.CONTINUE_MESSAGE)

    def _setup(self) -> None:
        """
        Sets up the agent by initializing the conversation and chat provider.

        Note: This should be called before running the agent.

        Raises:
            AgentError: If the agent fails to initialize.
        """
        self.conversation.add_message(
            OpenAIChatMessage(role="system", content=self.config.system_instruction)
        )
        for message in list(
            self._build_initial_messages({"user_input_instructions": self.instructions})
        ):
            self.conversation.add_message(message)

        self.chat_provider = OpenAIChatCompletionProvider(
            model=self.config.model,
            temperature=self.config.temperature,
            stream=self.config.stream,
            conversation=self.conversation,
            functions=self.functions,
        )

        logger.debug(f"Initializing with System Instruction:{self.config.system_instruction}\n\n")
        logger.debug(f"{('-' * 60)}\nSession ID: {self.config.session_id}\n{'-'* 60}\n\n")
