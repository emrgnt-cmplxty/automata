import logging
from typing import Dict, Final, Sequence

from automata.config.config_types import AutomataAgentConfig, ConfigCategory
from automata.core.llm.completion import (
    LLMChatMessage,
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.core.llm.providers.openai import (
    OpenAIAgent,
    OpenAIChatMessage,
    OpenAIChatProvider,
    OpenAIConversation,
    OpenAIFunction,
)
from automata.core.utils import format_text, load_config

logger = logging.getLogger(__name__)


class AutomataOpenAIAgent(OpenAIAgent):
    """
    AutomataOpenAIAgent is an autonomous agent designed to execute instructions and report
    the results back to the main system. It communicates with the OpenAI API to generate
    responses based on given instructions and manages interactions with various tools.
    """

    CONTINUE_MESSAGE: Final = "Continue, and return a result JSON when finished."
    NUM_DEFAULT_MESSAGES: Final = 3  # Prompt + Assistant Initialization + User Task
    INITIALIZER_DUMMY: Final = "automata_initializer"
    ERROR_DUMMY_TOOL: Final = "error_reporter"

    def __init__(self, instructions: str, config: AutomataAgentConfig) -> None:
        """
        Initializes an AutomataAgent.

        Args:
            instructions (str): The instructions to be executed by the agent.
            config (AutomataAgentConfig): The configuration for the agent. Defaults to None.
        """
        super().__init__(instructions)
        self.config = config
        self.conversation = OpenAIConversation()
        self.iteration_count = 0
        self._setup()

    def __iter__(self):
        return self

    def __next__(self) -> LLMIterationResult:
        """
        Executes a single iteration of the task and returns the latest assistant and user messages.

        Raises:
            ValueError: If the agent has already completed its task.

        Returns:
            Optional[Tuple[LLMCompletionResult, LLMCompletionResult]] Latest assistant and user messages, or None if the task is completed.
        """
        if self.completed or self.iteration_count >= self.config.max_iterations:
            print("raising stop iteration")
            raise StopIteration

        assistant_message = self.chat_provider.get_next_assistant_message()
        self.conversation.add_message(assistant_message)
        self.iteration_count += 1

        if self._is_finished(assistant_message):
            self.completed = True
            return (assistant_message, None)

        user_message = self._get_next_user_response(assistant_message)
        self.conversation.add_message(user_message)

        return (assistant_message, user_message)

    def run(self) -> str:
        """
        Runs the agent and iterates through the tasks until a result is produced
          or the max iterations are exceeded.

        Returns:
            str: The final result or an error message if the result wasn't found in time.

        Notes:
            The agent must be setup before running.

            This implementation calls next() on self until a StopIteration exception is raised,
            at which point it will break out of the loop and return the final result.
        """
        while True:
            try:
                next(self)
            except StopIteration:
                break

        last_message = self.conversation.get_latest_message()
        if (
            not self.completed
            or not isinstance(last_message, OpenAIChatMessage)
            or not last_message.function_call
            or "result" not in last_message.function_call.arguments
        ):
            raise ValueError("The agent did not produce a result.")
        return last_message.function_call.arguments["result"]

    def set_database_provider(self, provider: LLMConversationDatabaseProvider) -> None:
        """
        Sets the database provider for the agent.

        Args:
            provider (LLMConversationDatabaseProvider): The database provider to use.

        """
        self.database_provider = provider
        self.conversation.register_observer(provider)

    def _build_initial_messages(self, formatters: Dict[str, str]) -> Sequence[LLMChatMessage]:
        """
        Builds the initial messages for the agent's conversation.

        Args:
            formatters (Dict[str, str]): A dictionary of formatters used to format the messages.

        Returns:
            List[OpenAIChatMessage]: A list of initial messages for the conversation.
        """
        assert "user_input_instructions" in formatters
        formatters["initializer_dummy_tool"] = AutomataOpenAIAgent.INITIALIZER_DUMMY

        messages_config = load_config(
            ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
        )
        initial_messages = messages_config["initial_messages"]

        input_messages = []
        for message in initial_messages:
            input_message = format_text(formatters, message["content"])
            input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

        return input_messages

    def _is_finished(self, assistant_message: OpenAIChatMessage) -> bool:
        """
        Checks if the task is complete based on the assistant's message.

        Args:
            assistant_message (OpenAIChatMessage): The assistant's message.

        Returns:
            bool: True if the task is complete, False otherwise.
        """
        if assistant_message.function_call:
            return assistant_message.function_call.name == "call_termination"
        return False

    def _get_next_user_response(self, assistant_message: OpenAIChatMessage) -> OpenAIChatMessage:
        """
        Generates a user message based on the assistant's message.

        Args:
            assistant_message (OpenAIChatMessage): The assistant's message.

        Returns:
            OpenAIChatMessage: The user's message.
        """
        return OpenAIChatMessage(role="user", content="Continue")

    def _get_available_functions(self) -> Sequence[OpenAIFunction]:
        """

        Gets the available functions for the agent.

        Returns:
            Sequence[OpenAIFunction]: The available functions for the agent.
        """
        return [self._get_termination_function()]

    def _setup(self) -> None:
        """
        Sets up the agent by initializing the database and loading the config.

        Note: This should be called before running the agent.

        Raises:
            ValueError: If the config was not properly initialized.
        """

        self.conversation.add_message(
            OpenAIChatMessage(role="system", content=self.config.system_instruction)
        )

        self.conversation.add_messages(
            list(self._build_initial_messages({"user_input_instructions": self.instructions}))
        )

        self.chat_provider = OpenAIChatProvider(
            model=self.config.model,
            temperature=self.config.temperature,
            stream=self.config.stream,
            conversation=self.conversation,
            functions=list(self._get_available_functions()),
        )

        logger.debug(f"Initializing with System Instruction:{self.config.system_instruction}\n\n")
        logger.debug(f"{('-' * 60)}\nSession ID: {self.config.session_id}\n{'-'* 60}\n\n")
