import logging
from typing import Dict, Final, List, Sequence

from automata.config.config_types import AutomataAgentConfig, ConfigCategory
from automata.core.base.error import MaxIterError
from automata.core.llm.completion import (
    LLMChatMessage,
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.core.llm.providers.openai import (
    OpenAIAgent,
    OpenAIChatMessage,
    OpenAIChatProvider,
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

    def __init__(self, instructions: str, config: AutomataAgentConfig) -> None:
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
            ValueError: If the agent has already completed its task.

        Returns:
            Optional[Tuple[LLMCompletionResult, LLMCompletionResult]] Latest assistant and user messages, or None if the task is completed.
        """
        if self.completed or self.iteration_count >= self.config.max_iterations:
            print("raising stop iteration")
            raise StopIteration

        assistant_message = self.chat_provider.get_next_assistant_message()
        print("latest assistant_message = ", assistant_message)
        print("latest assistant_message = ", assistant_message.to_dict())

        self.conversation.add_message(assistant_message)
        self.iteration_count += 1

        user_message = self._get_next_user_response(assistant_message)
        self.conversation.add_message(user_message)

        return (assistant_message, user_message)

    @property
    def tools(self) -> List[OpenAITool]:
        """
        Gets the tools for the agent.

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

        Gets the available functions for the agent.

        Returns:
            Sequence[OpenAIFunction]: The available functions for the agent.
        """
        return [ele.openai_function for ele in self.tools]

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
        print("last_message = ", last_message)
        if self.iteration_count >= self.config.max_iterations:
            raise MaxIterError("The agent did not produce a result.")
        if not self.completed or not isinstance(last_message, OpenAIChatMessage):
            raise ValueError("The agent did not produce a result.")
        if not last_message.content:
            raise ValueError("The agent produced an empty result.")
        return last_message.content

    def set_database_provider(self, provider: LLMConversationDatabaseProvider) -> None:
        """
        Sets the database provider for the agent.

        Args:
            provider (LLMConversationDatabaseProvider): The database provider to use.

        """
        if not isinstance(provider, LLMConversationDatabaseProvider):
            raise ValueError(f"Invalid database provider type: {type(provider)}")
        if self.database_provider:
            raise ValueError("The database provider has already been set.")
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

        messages_config = load_config(
            ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
        )
        initial_messages = messages_config["initial_messages"]

        input_messages = []
        for message in initial_messages:
            input_message = format_text(formatters, message["content"])
            input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

        return input_messages

    def _get_next_user_response(self, assistant_message: OpenAIChatMessage) -> OpenAIChatMessage:
        """
        Generates a user message based on the assistant's message.

        Args:
            assistant_message (OpenAIChatMessage): The assistant's message.

        Returns:
            OpenAIChatMessage: The user's message.
        """
        if assistant_message.function_call:
            for tool in self.tools:
                if assistant_message.function_call.name == tool.openai_function.name:
                    print("Running tool: ", tool)
                    print("With arguments: ", assistant_message.function_call.arguments)
                    result = tool.run(assistant_message.function_call.arguments)
                    print("execution result = ", result)
                    return OpenAIChatMessage(
                        role="user", content=f"{AutomataOpenAIAgent.SUCCESS_PREFIX}{result}"
                    )

        return OpenAIChatMessage(role="user", content=AutomataOpenAIAgent.CONTINUE_MESSAGE)

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
        for message in list(
            self._build_initial_messages({"user_input_instructions": self.instructions})
        ):
            self.conversation.add_message(message)

        print("initial Messages = ", [ele.to_dict() for ele in self.conversation.messages])

        self.chat_provider = OpenAIChatProvider(
            model=self.config.model,
            temperature=self.config.temperature,
            stream=self.config.stream,
            conversation=self.conversation,
            functions=self.functions,
        )

        logger.debug(f"Initializing with System Instruction:{self.config.system_instruction}\n\n")
        logger.debug(f"{('-' * 60)}\nSession ID: {self.config.session_id}\n{'-'* 60}\n\n")
