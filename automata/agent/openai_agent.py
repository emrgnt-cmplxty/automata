"""Defines the concrete OpenAIAutomataAgent class."""
import logging
import logging.config
from abc import ABC, abstractmethod
from typing import Final, List, Optional, Sequence

from automata.agent import Agent, AgentToolkitBuilder, AgentToolkitNames
from automata.agent.error import (
    AgentGeneralError,
    AgentMaxIterError,
    AgentResultError,
    AgentStopIterationError,
)
from automata.config import OpenAIAutomataAgentConfig
from automata.core.utils import get_logging_config
from automata.llm import (
    LLMChatMessage,
    LLMConversation,
    LLMIterationResult,
    OpenAIChatCompletionProvider,
    OpenAIChatMessage,
    OpenAIConversation,
    OpenAIFunction,
    OpenAITool,
    FunctionCall,
)
from automata.tools import ToolExecution, ToolExecutor

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


class OpenAIAutomataAgent(Agent):
    """
    OpenAIAutomataAgent is an autonomous agent designed to execute
    instructions and report the results back to the main system. It
    communicates with the OpenAI API to generate responses based on given
    instructions and manages interactions with various tools.
    """

    CONTINUE_PREFIX: Final = f"Continue...\n"
    OBSERVATION_MESSAGE: Final = "Observation:\n"
    GENERAL_SUFFIX_TEMPLATE: Final = "STATUS NOTES\nYou have used {iteration_count} out of a maximum of {max_iterations} iterations.\nYou have used {estimated_tokens} out of a maximum of {max_tokens} tokens.\nYour instructions are '{user_instructions}'"
    STOPPING_SUFFIX_TEMPLATE: Final = "STATUS NOTES:\nYOU HAVE EXCEEDED YOUR MAXIMUM ALLOWABLE ITERATIONS OR TOKENS, RETURN A RESULT NOW WITH call-termination.\nRECALL, YOUR INSTRUCTIONS WERE '{user_instructions}."

    def __init__(
        self, user_instructions: str, config: OpenAIAutomataAgentConfig
    ) -> None:
        # sourcery skip: docstrings-for-functions
        super().__init__(user_instructions)
        self.config = config
        self.iteration_count = 0
        self.completed = False
        self._conversation = OpenAIConversation()
        self._setup()

    def __iter__(self):
        return self

    def __repr__(self):
        return f"OpenAIAutomataAgent(config={str(self.config)}, iteration_count={self.iteration_count}, completed={self.completed}, _conversation={str(self._conversation)})"

    def __next__(self) -> LLMIterationResult:
        """
        Executes a single iteration of the task and returns the latest
        assistant and user messages.

        Raises:
            AgentStopIterationError: If the agent has already completed its task
            or exceeded the maximum number of iterations.

        TODO:
            - Add support for hierarchical agents.
        """
        if self.completed or self.iteration_count > self.config.max_iterations:
            raise AgentStopIterationError

        logger.info(f"\n{('-' * 120)}\nLatest Assistant Message -- \n")
        assistant_message = self.chat_provider.get_next_assistant_completion()
        self.chat_provider.add_message(assistant_message)
        if not self.config.stream:
            logger.info(f"{assistant_message}\n")
        logger.info(f"\n{('-' * 120)}")

        self.iteration_count += 1

        user_message = self._get_next_user_response(assistant_message)
        logger.info(f"Latest User Message -- \n{user_message}\n")
        self.chat_provider.add_message(user_message)
        logger.info(f"\n{('-' * 120)}")

        return (assistant_message, user_message)

    @property
    def conversation(self) -> LLMConversation:
        """A concrete property for getting the conversation associated with the agent."""
        return self._conversation

    @property
    def agent_responses(self) -> List[LLMChatMessage]:
        """A concrete property for getting the agent responses associated with the agent."""
        return [
            message
            for message in self._conversation.messages
            if message.role == "assistant"
        ][-self.iteration_count :]

    @property
    def tools(self) -> Sequence[OpenAITool]:
        """A concrete property for getting the tools associated with the agent."""
        tools = []
        for tool in self.config.tools:
            if not isinstance(tool, OpenAITool):
                raise ValueError(f"Invalid tool type: {type(tool)}")
            tools.append(tool)
        tools.append(self._get_termination_tool())
        return tools

    @property
    def functions(self) -> List[OpenAIFunction]:
        """A concrete property for getting the functions associated with the agent."""

        return [ele.openai_function for ele in self.tools]

    def run(self) -> str:
        """
        Runs the agent and iterates through the tasks until a result is produced
        or the max iterations are exceeded.

        The agent must be setup before running.
        This implementation calls next() on self until a AgentStopIterationError exception is raised,
        at which point it will break out of the loop and return the final result.

        Returns:
            str: The final agent output or an error message if the result wasn't found before an exception.

        Raises:
            AgentError:
                If the agent exceeds the maximum number of iterations.
                If the agent does not produce a result.
        """
        if not self._initialized:
            raise AgentGeneralError("The agent has not been initialized.")

        while True:
            try:
                next(self)
            except AgentStopIterationError:
                break

        last_message = self._conversation.get_latest_message()
        if (
            not self.completed
            and self.iteration_count > self.config.max_iterations
        ):
            raise AgentMaxIterError(
                "The agent exceeded the maximum number of iterations."
            )
        elif not self.completed or not isinstance(
            last_message, OpenAIChatMessage
        ):
            raise AgentResultError("The agent did not produce a result.")
        elif not last_message.content:
            raise AgentResultError("The agent produced an empty result.")
        return last_message.content

    def get_result(self) -> str:
        """Gets the result of the agent."""

        if not self.completed:
            raise ValueError("The agent has not completed its instructions.")
        if result := self._conversation.get_latest_message().content:
            return result
        else:
            raise ValueError("The agent did not produce a result.")

    def _get_next_user_response(
        self, assistant_message: OpenAIChatMessage
    ) -> OpenAIChatMessage:
        """
        Generates a user message based on the assistant's message.
        This is done by checking if the assistant's message contains a function call.
        If it does, then the corresponding tool is run and the result is returned.
        Otherwise, the user is prompted to continue the conversation.
        """

        if assistant_message.function_call:
            try:
                result = self.tool_executor.execute(
                    assistant_message.function_call
                )
                function_iteration_message = (
                    ""
                    if self.completed
                    else f"\n\n{self._get_iteration_status(result)}"
                )
                # TODO - Indent the result and iteration messages
                return OpenAIChatMessage(
                    role="user",
                    content=f"{OpenAIAutomataAgent.OBSERVATION_MESSAGE}{result}\n{function_iteration_message}",
                )
            except Exception as e:
                failure_message = f"Tool execution failed: {e}"
                logger.info(failure_message)
                return OpenAIChatMessage(
                    role="user",
                    content=failure_message,
                )

        return OpenAIChatMessage(
            role="user",
            content=f"{OpenAIAutomataAgent.CONTINUE_PREFIX}\n{self._get_iteration_status()}",
        )

    def _get_iteration_status(
        self, message_content: Optional[str] = None
    ) -> str:
        estimated_tokens_consumed = (
            self.chat_provider.approximate_tokens_consumed
            + (
                len(self.chat_provider.encoding.encode(message_content))
                if message_content
                else 0
            )
        )
        if (
            self.iteration_count != self.config.max_iterations
            and estimated_tokens_consumed < self.config.max_tokens
        ):
            return OpenAIAutomataAgent.GENERAL_SUFFIX_TEMPLATE.format(
                iteration_count=self.iteration_count,
                max_iterations=self.config.max_iterations,
                max_tokens=self.config.max_tokens,
                estimated_tokens=estimated_tokens_consumed,
                user_instructions=f"{self.user_instructions[:200]}...",
            )
        else:
            return OpenAIAutomataAgent.STOPPING_SUFFIX_TEMPLATE.format(
                user_instructions=f"{self.user_instructions[:200]}..."
            )

    def _setup(self) -> None:
        """
        Setup the agent by initializing the conversation and chat provider.

        Note:
            This should be called before running the agent.

        Raises:
            AgentError: If the agent fails to initialize.
        """
        logger.info(
            f"Initializing with System Instruction -- \n\n{self.config.system_instruction}\n\n"
        )
        self.chat_provider = OpenAIChatCompletionProvider(
            model=self.config.model,
            temperature=self.config.temperature,
            stream=self.config.stream,
            system_instruction=self.config.system_instruction,
            user_instruction=self.user_instructions,
            conversation=self._conversation,
            functions=self.functions,
        )

        self.tool_executor = ToolExecutor(ToolExecution(self.tools))
        self._initialized = True

    def _get_termination_tool(self) -> OpenAITool:
        """Gets the tool responsible for terminating the OpenAI agent."""

        def terminate(result: str) -> str:
            """Terminates the agent run."""
            self.completed = True
            return result

        return OpenAITool(
            name="call-termination",
            description="Terminates the conversation.",
            properties={
                "result": {
                    "type": "string",
                    "description": "The final result of the conversation.",
                }
            },
            required=["result"],
            function=terminate,
        )


class OpenAIAgentToolkitBuilder(AgentToolkitBuilder, ABC):
    """OpenAIAgentToolkitBuilder is an abstract class for building OpenAI agent tools."""

    @abstractmethod
    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds an OpenAITool to be used by the associated agent.
        TODO - Automate as much of this as possible, and modularize
        """
        pass

    @classmethod
    def can_handle(cls, tool_manager: AgentToolkitNames) -> bool:
        """Checks if the ToolkitBuilder matches the expecte dtool_manager type"""
        return cls.TOOL_NAME == tool_manager
