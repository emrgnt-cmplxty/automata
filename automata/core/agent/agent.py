import logging
import re
from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional, Tuple

import openai
from termcolor import colored

from automata.config.config_types import AutomataAgentConfig, ConfigCategory
from automata.core.base.agent import Agent
from automata.core.base.llm.llm_types import LLMCompletionResult
from automata.core.base.llm.openai import (
    OpenAIChatCompletionResult,
    OpenAIChatMessage,
    OpenAIChatProvider,
    OpenAIConversation,
)
from automata.core.utils import format_text, load_config, set_openai_api_key

logger = logging.getLogger(__name__)


class AutomataOpenAIAgent(Agent):
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
        super().__init__(instructions, config)
        self.conversation = OpenAIConversation()
        self.chat_provider = OpenAIChatProvider(
            model=config.model, temperature=config.temperature, stream=config.stream
        )

    def iter_step(self) -> Optional[Tuple[LLMCompletionResult, LLMCompletionResult]]:
        """
        Executes a single iteration of the task and returns the latest assistant and user messages.

        Raises:
            ValueError: If the agent has already completed its task.

        Returns:
            Optional[Tuple[LLMCompletionResult, LLMCompletionResult]] Latest assistant and user messages, or None if the task is completed.
        """

        if not self.completed:
            assistant_message = self._get_openai_assistant_response()

            user_message = self._generate_user_response(assistant_message)

            if self._is_task_complete(user_message):
                self.completed = True

            return (
                assistant_message,
                user_message,
            )
        else:
            return None

    def run(self) -> str:
        """
        Runs the agent and iterates through the tasks until a result is produced
          or the max iterations are exceeded.

        Returns:
            str: The final result or an error message if the result wasn't found in time.
        """
        latest_responses = self.iter_step()
        while latest_responses is not None:
            # Each iteration adds two messages, one from the assistant and one from the user
            # If we have equal to or more than 2 * max_iters messages (less the default messages),
            # then we have exceeded the max_iters
            if len(self.chat_provider.iteration_count) >= self.config.max_iters:
                raise ValueError("Max iterations exceeded.")
        return self.conversation.result()

    def setup(self) -> None:
        """
        Sets up the agent by initializing the database and loading the config.

        Note: This should be called before running the agent.

        Raises:
            ValueError: If the config was not properly initialized.
        """
        set_openai_api_key()

        if not self.config.session_id:
            raise ValueError("Config was not properly initialized.")

        ## Should we setup a database connection here?
        raise NotImplementedError

    # def _build_initial_messages(self, formatters: Dict[str, str]) -> List[OpenAIChatMessage]:
    #     """
    #     Builds the initial messages for the agent's conversation.

    #     Args:
    #         formatters (Dict[str, str]): A dictionary of formatters used to format the messages.

    #     Returns:
    #         List[OpenAIChatMessage]: A list of initial messages for the conversation.
    #     """
    #     assert "user_input_instructions" in formatters
    #     formatters["initializer_dummy_tool"] = AutomataAgent.INITIALIZER_DUMMY

    #     messages_config = load_config(
    #         ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
    #     )
    #     initial_messages = messages_config["initial_messages"]

    #     input_messages = []
    #     for message in initial_messages:
    #         input_message = format_text(formatters, message["content"])
    #         input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

    #     return input_messages

    # def _save_message(self, role: str, content: str) -> OpenAIChatMessage:
    #     """
    #     Saves the messagee for the agent.

    #     Args:
    #         role (str): The role of the messagee.
    #         content (str): The content of the messagee.
    #     """
    #     self.database_manager.put_message(role, content, len(self.messages))
    #     message = OpenAIChatMessage(role=role, content=content)
    #     self.messages.append(message)
    #     return message

    # def _get_debug_summary(self):
    #     """Get the debug summary for the agent."""
    #     user_message = "Provide a succinct one-sentence summary of the errors encountered. Write nothing else."
    #     self._save_message("user", user_message)
    #     return self._get_openai_response()

    # def _get_openai_response(self) -> str:
    #     """Get the response from OpenAI."""

    #     def _stream_message(agent_name, response_summary: Any):
    #         """
    #         Streams the response message from the agent.

    #         Args:
    #             response_summary (Any): The response summary from the agent.

    #         Returns:
    #             str: The streamed response text.
    #         """
    #         print(colored(f"\n>>> {agent_name} Agent:", "green"))
    #         latest_accumulation = ""
    #         stream_separator = " "
    #         response_text = ""
    #         for chunk in response_summary:
    #             if "content" in chunk["choices"][0]["delta"]:
    #                 chunk_content = chunk["choices"][0]["delta"]["content"]
    #                 chunk_content.replace("\\n", "\n")
    #                 latest_accumulation += chunk_content
    #                 response_text += chunk_content
    #             if stream_separator in latest_accumulation:
    #                 words = latest_accumulation.split(stream_separator)
    #                 for word in words[:-1]:
    #                     print(colored(str(word), "green"), end=" ", flush=True)
    #                 latest_accumulation = words[-1]
    #         print(colored(str(latest_accumulation), "green"))
    #         return response_text

    #     response_summary = openai.ChatCompletion.create(
    #         model=self.config.model,
    #         messages=[ele.to_dict() for ele in self.messages],
    #         temperature=self.config.temperature,
    #         stream=self.config.stream,
    #     )

    #     return (
    #         _stream_message(self.config.config_name.value, response_summary)
    #         if self.config.stream
    #         else OpenAIChatCompletionResult(raw_data=response_summary).get_content()
    #     )


# import logging
# import re
# from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional, Tuple

# import openai
# from termcolor import colored

# from automata.config.config_types import AutomataAgentConfig, ConfigCategory
# from automata.core.base.agent import Agent
# from automata.core.base.llm.openai import (
#     OpenAIChatCompletionResult,
#     OpenAIChatMessage,
#     OpenAIChatProvider,
#     OpenAIConversation,
# )
# from automata.core.base.llm.llm_types import LLMCompletionResult
# from automata.core.utils import format_text, load_config, set_openai_api_key

# logger = logging.getLogger(__name__)


# class AutomataOpenAIAgent(Agent):
#     """
#     AutomataOpenAIAgent is an autonomous agent designed to execute instructions and report
#         the results back to the main system. It communicates with the OpenAI API to generate
#         responses based on given instructions and manages interactions with various tools.
#     """

#     CONTINUE_MESSAGE: Final = "Continue, and return a result JSON when finished."
#     NUM_DEFAULT_MESSAGES: Final = 3  # Prompt + Assistant Initialization + User Task
#     INITIALIZER_DUMMY: Final = "automata_initializer"
#     ERROR_DUMMY_TOOL: Final = "error_reporter"

#     def __init__(self, instructions: str, config: AutomataAgentConfig) -> None:
#         """
#         Initializes an AutomataAgent.

#         Args:
#             instructions (str): The instructions to be executed by the agent.
#             config (AutomataAgentConfig): The configuration for the agent. Defaults to None.
#         """
#         super().__init__(instructions, config)
#         self.conversation = OpenAIConversation()
#         self.chat_provider = OpenAIChatProvider(
#             model=config.model, temperature=config.temperature, stream=config.stream
#         )

#     def iter_step(self) -> Optional[Tuple[LLMCompletionResult, LLMCompletionResult]]:
#         """
#         Executes a single iteration of the task and returns the latest assistant and user messages.

#         Raises:
#             ValueError: If the agent has already completed its task.

#         Returns:
#             Optional[Tuple[LLMCompletionResult, LLMCompletionResult]] Latest assistant and user messages, or None if the task is completed.
#         """
#         # if self.completed:
#         #     raise ValueError("Cannot run an agent that has already completed.")

#         # response = self._get_openai_response()

#         # # assistant_message = self._save_message("assistant", response_text)
#         # # user_message = self._save_message(
#         # #     "user",
#         # #     generate_user_observation_message(observations)
#         # #     if len(observations) > 0
#         # #     else AutomataAgent.CONTINUE_MESSAGE,
#         # # )

#         # return (assistant_message, user_message)
#         return (
#             OpenAIChatCompletionResult(raw_data=None),
#             OpenAIChatCompletionResult(raw_data=None),
#         )

#     def run(self) -> str:
#         """
#         Runs the agent and iterates through the tasks until a result is produced
#           or the max iterations are exceeded.

#         Returns:
#             str: The final result or an error message if the result wasn't found in time.
#         """
#         # latest_responses = self.iter_step()
#         # while latest_responses is not None:
#         #     # Each iteration adds two messages, one from the assistant and one from the user
#         #     # If we have equal to or more than 2 * max_iters messages (less the default messages),
#         #     # then we have exceeded the max_iters
#         #     if (
#         #         len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES
#         #         >= self.config.max_iters * 2
#         #     ):
#         #         debug_summary = self._get_debug_summary()
#         #         return f"Result was not found before iterations exceeded configured max limit: {self.config.max_iters}. Debug summary: {debug_summary}"
#         #     latest_responses = self.iter_step()
#         # return self.messages[-1].content
#         return "Not yet implemented..."

#     def setup(self) -> None:
#         """
#         Sets up the agent by initializing the database and loading the config.

#         Note: This should be called before running the agent.

#         Raises:
#             ValueError: If the config was not properly initialized.
#         """
#         set_openai_api_key()

#         if not self.config.session_id:
#             raise ValueError("Config was not properly initialized.")
#         # self.database_manager: AutomataAgentDatabase = AutomataAgentDatabase(
#         #     self.config.session_id
#         # )
#         # self.database_manager._init_database()
#         # if not self.config.is_new_agent:
#         #     self.messages = self.database_manager.get_conversations()
#         # else:
#         #     if not self.config.system_instruction:
#         #         raise ValueError("System instruction must be provided if new agent.")

#         #     self._save_message("system", self.config.system_instruction)
#         #     initial_messages = self._build_initial_messages(
#         #         {"user_input_instructions": self.instructions}
#         #     )
#         #     for message in initial_messages:
#         #         self._save_message(message.role, message.content)

#         # logger.debug(
#         #     "Initializing with System Instruction:%s\n\n" % self.config.system_instruction
#         # )
#         # logger.debug("-" * 60)
#         # logger.debug(f"Session ID: {self.config.session_id}")
#         # logger.debug("-" * 60)
#         raise NotImplementedError

#     # def _build_initial_messages(self, formatters: Dict[str, str]) -> List[OpenAIChatMessage]:
#     #     """
#     #     Builds the initial messages for the agent's conversation.

#     #     Args:
#     #         formatters (Dict[str, str]): A dictionary of formatters used to format the messages.

#     #     Returns:
#     #         List[OpenAIChatMessage]: A list of initial messages for the conversation.
#     #     """
#     #     assert "user_input_instructions" in formatters
#     #     formatters["initializer_dummy_tool"] = AutomataAgent.INITIALIZER_DUMMY

#     #     messages_config = load_config(
#     #         ConfigCategory.INSTRUCTION.value, self.config.instruction_version.value
#     #     )
#     #     initial_messages = messages_config["initial_messages"]

#     #     input_messages = []
#     #     for message in initial_messages:
#     #         input_message = format_text(formatters, message["content"])
#     #         input_messages.append(OpenAIChatMessage(role=message["role"], content=input_message))

#     #     return input_messages

#     # def _save_message(self, role: str, content: str) -> OpenAIChatMessage:
#     #     """
#     #     Saves the messagee for the agent.

#     #     Args:
#     #         role (str): The role of the messagee.
#     #         content (str): The content of the messagee.
#     #     """
#     #     self.database_manager.put_message(role, content, len(self.messages))
#     #     message = OpenAIChatMessage(role=role, content=content)
#     #     self.messages.append(message)
#     #     return message

#     # def _get_debug_summary(self):
#     #     """Get the debug summary for the agent."""
#     #     user_message = "Provide a succinct one-sentence summary of the errors encountered. Write nothing else."
#     #     self._save_message("user", user_message)
#     #     return self._get_openai_response()

#     # def _get_openai_response(self) -> str:
#     #     """Get the response from OpenAI."""

#     #     def _stream_message(agent_name, response_summary: Any):
#     #         """
#     #         Streams the response message from the agent.

#     #         Args:
#     #             response_summary (Any): The response summary from the agent.

#     #         Returns:
#     #             str: The streamed response text.
#     #         """
#     #         print(colored(f"\n>>> {agent_name} Agent:", "green"))
#     #         latest_accumulation = ""
#     #         stream_separator = " "
#     #         response_text = ""
#     #         for chunk in response_summary:
#     #             if "content" in chunk["choices"][0]["delta"]:
#     #                 chunk_content = chunk["choices"][0]["delta"]["content"]
#     #                 chunk_content.replace("\\n", "\n")
#     #                 latest_accumulation += chunk_content
#     #                 response_text += chunk_content
#     #             if stream_separator in latest_accumulation:
#     #                 words = latest_accumulation.split(stream_separator)
#     #                 for word in words[:-1]:
#     #                     print(colored(str(word), "green"), end=" ", flush=True)
#     #                 latest_accumulation = words[-1]
#     #         print(colored(str(latest_accumulation), "green"))
#     #         return response_text

#     #     response_summary = openai.ChatCompletion.create(
#     #         model=self.config.model,
#     #         messages=[ele.to_dict() for ele in self.messages],
#     #         temperature=self.config.temperature,
#     #         stream=self.config.stream,
#     #     )

#     #     return (
#     #         _stream_message(self.config.config_name.value, response_summary)
#     #         if self.config.stream
#     #         else OpenAIChatCompletionResult(raw_data=response_summary).get_content()
#     #     )
