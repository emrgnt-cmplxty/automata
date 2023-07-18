import logging

import pytest

from automata.agent import OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.core.utils import calculate_similarity
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.factory import AgentToolFactory
from tests.utils.regression_utils import initialize_automata

logger = logging.getLogger(__name__)


# Uncomment if using gpt-3.5-turbo-16k
# @pytest.mark.flaky(
#     reruns=5
# )  # allowing up to 5 retries if using gpt-3.5-turbo-16k
@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, allowable_results",
    [
        # A simple 'hello-world' style instruction
        (
            "This is a dummy instruction, return True.",
            ["context-oracle"],
            "gpt-3.5-turbo-16k",
            "automata-main",
            1,
            ["True"],
        ),
        # A simple context search for `SymbolSearch`
        (
            "What class should we instantiate to search the codebase for relevant symbols? Please return just the class name.",
            ["context-oracle"],
            "gpt-4",
            "automata-main",
            2,
            ["SymbolSearch", "`SymbolSearch`"],
        ),
        # A simple context search for `OpenAIAutomataAgentConfig`
        (
            "What class is responsible for building OpenAI Agent configurations? Please jsut return the class name.",
            ["context-oracle"],
            "gpt-4",
            "automata-main",
            2,
            [
                "OpenAIAutomataAgentConfigBuilder",
                "`OpenAIAutomataAgentConfigBuilder`",
                "OpenAIAutomataAgentConfig",  # this is not the correct result, but let's allow it for now
                "`OpenAIAutomataAgentConfig`",  # same
            ],
        ),
    ],
)
def test_agent_execution(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    allowable_results,
):
    initialize_automata()

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkit_list
    )
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)
    config_name = AgentConfigName(agent_config_name)
    agent_config_builder = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(model)
    )

    agent_config_builder = agent_config_builder.with_max_iterations(
        max_iterations
    )

    agent = OpenAIAutomataAgent(
        instructions, config=agent_config_builder.build()
    )
    result = agent.run()
    result = result.replace("Execution Result:\n", "").strip()
    if result not in allowable_results:
        raise ValueError(
            f"Allowable results={allowable_results}, found result={result}"
        )


@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, expected_result, min_similarity",
    [
        # Extracting source code directly from a module
        (
            "Fetch the source code for VectorDatabaseProvider.",
            ["py-reader"],
            "gpt-3.5-turbo-16k",
            "automata-main",
            2,
            "class VectorDatabaseProvider(abc.ABC, Generic[K, V]):\n\n    @abc.abstractmethod\n    def __len__(self) -> int:\n        pass\n\n    @abc.abstractmethod\n    def save(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def load(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def clear(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def get_ordered_keys(self) -> List[K]:\n        pass\n\n    @abc.abstractmethod\n    def get_ordered_embeddings(self) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def add(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_add(self, entries: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def update_entry(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_update(self, entries: List[V]) -> None:\n        pass\n\n    @abc.abstractmethod\n    def entry_to_key(self, entry: V) -> K:\n        pass\n\n    @abc.abstractmethod\n    def contains(self, key: K) -> bool:\n        pass\n\n    @abc.abstractmethod\n    def get(self, key: K) -> V:\n        pass\n\n    @abc.abstractmethod\n    def batch_get(self, keys: List[K]) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def discard(self, key: K) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_discard(self, keys: List[K]) -> None:\n        pass",
            0.95,
        ),
        (
            "Fetch the source code for OpenAIAutomataAgent.",
            ["py-reader"],
            "gpt-3.5-turbo-16k",
            "automata-main",
            2,
            """class OpenAIAutomataAgent(Agent):\n    CONTINUE_PREFIX: Final = f\'Continue...\'\n    EXECUTION_PREFIX: Final = \'\'\n    _initialized = False\n    GENERAL_SUFFIX: Final = \'STATUS NOTES\\nYou have used {iteration_count} out of a maximum of {max_iterations} iterations.\\nYou have used {estimated_tokens} out of a maximum of {max_tokens} tokens.\\nPlease return a result with call_termination when ready or if you are nearing limits.\'\n    STOPPING_SUFFIX: Final = \'STATUS NOTES:\\nYOU HAVE EXCEEDED YOUR MAXIMUM ALLOWABLE ITERATIONS, RETURN A RESULT NOW WITH call_termination.\'\n\n    def __init__(self, instructions: str, config: OpenAIAutomataAgentConfig) -> None:\n        super().__init__(instructions)\n        self.config = config\n        self.iteration_count = 0\n        self.agent_conversation_database = OpenAIConversation()\n        self.completed = False\n        self._setup()\n\n    def __iter__(self):\n        return self\n\n    def __next__(self) -> LLMIterationResult:\n        if self.completed or self.iteration_count >= self.config.max_iterations:\n            raise AgentStopIteration\n        logging.debug(f"\\n{\'-\' * 120}\\nLatest Assistant Message -- \\n")\n        assistant_message = self.chat_provider.get_next_assistant_completion()\n        self.chat_provider.add_message(assistant_message)\n        if not self.config.stream:\n            logger.debug(f\'{assistant_message}\\n\')\n        logging.debug(f"\\n{\'-\' * 120}")\n        self.iteration_count += 1\n        user_message = self._get_next_user_response(assistant_message)\n        logger.debug(f\'Latest User Message -- \\n{user_message}\\n\')\n        self.chat_provider.add_message(user_message)\n        logging.debug(f"\\n{\'-\' * 120}")\n        return (assistant_message, user_message)\n\n    @property\n    def tools(self) -> List[OpenAITool]:\n        tools = []\n        for tool in self.config.tools:\n            if not isinstance(tool, OpenAITool):\n                raise ValueError(f\'Invalid tool type: {type(tool)}\')\n            tools.append(tool)\n        tools.append(self._get_termination_tool())\n        return tools\n\n    @property\n    def functions(self) -> List[OpenAIFunction]:\n        return [ele.openai_function for ele in self.tools]\n\n    def run(self) -> str:\n        if not self._initialized:\n            raise AgentGeneralError(\'The agent has not been initialized.\')\n        while True:\n            try:\n                next(self)\n            except AgentStopIteration:\n                break\n        last_message = self.agent_conversation_database.get_latest_message()\n        if not self.completed and self.iteration_count >= self.config.max_iterations:\n            raise AgentMaxIterError(\'The agent exceeded the maximum number of iterations.\')\n        elif not self.completed or not isinstance(last_message, OpenAIChatMessage):\n            raise AgentResultError(\'The agent did not produce a result.\')\n        elif not last_message.content:\n            raise AgentResultError(\'The agent produced an empty result.\')\n        return last_message.content\n\n    def set_database_provider(self, provider: LLMConversationDatabaseProvider) -> None:\n        if not isinstance(provider, LLMConversationDatabaseProvider):\n            raise AgentDatabaseError(f\'Invalid database provider type: {type(provider)}\')\n        if self.database_provider:\n            raise AgentDatabaseError(\'The database provider has already been set.\')\n        self.database_provider = provider\n        self.agent_conversation_database.register_observer(provider)\n\n    def _build_initial_messages(self, instruction_formatter: Dict[str, str]) -> Sequence[LLMChatMessage]:\n        assert \'user_input_instructions\' in instruction_formatter\n        messages_config = load_config(ConfigCategory.INSTRUCTION.to_path(), self.config.instruction_version.to_path())\n        initial_messages = messages_config[\'initial_messages\']\n        input_messages = []\n        for message in initial_messages:\n            input_message = format_text(instruction_formatter, message[\'content\']) if \'content\' in message else None\n            function_call = message.get(\'function_call\')\n            input_messages.append(OpenAIChatMessage(role=message[\'role\'], content=input_message, function_call=FunctionCall(name=function_call[\'name\'], arguments=function_call[\'arguments\']) if function_call else None))\n        return input_messages\n\n    def _get_next_user_response(self, assistant_message: OpenAIChatMessage) -> OpenAIChatMessage:\n        if self.iteration_count != self.config.max_iterations - 1:\n            iteration_message = OpenAIAutomataAgent.GENERAL_SUFFIX.format(iteration_count=self.iteration_count, max_iterations=self.config.max_iterations, estimated_tokens=self.chat_provider.approximate_tokens_consumed, max_tokens=self.config.max_tokens)\n        else:\n            iteration_message = OpenAIAutomataAgent.STOPPING_SUFFIX\n        if assistant_message.function_call:\n            for tool in self.tools:\n                if assistant_message.function_call.name == tool.openai_function.name:\n                    result = tool.run(assistant_message.function_call.arguments)\n                    function_iteration_message = \'\' if self.completed else f\'\\n\\n{iteration_message}\'\n                    return OpenAIChatMessage(role=\'user\', content=f\'{OpenAIAutomataAgent.EXECUTION_PREFIX}\\n\\n{result}{function_iteration_message}\')\n        return OpenAIChatMessage(role=\'user\', content=f\'{OpenAIAutomataAgent.CONTINUE_PREFIX}{iteration_message}\')\n\n    def _setup(self) -> None:\n        logger.debug(f\'Setting up agent with tools = {self.config.tools}\')\n        self.agent_conversation_database.add_message(OpenAIChatMessage(role=\'system\', content=self.config.system_instruction))\n        for message in list(self._build_initial_messages({\'user_input_instructions\': self.instructions})):\n            logger.debug(f\'Adding the following initial mesasge to the conversation {message}\')\n            self.agent_conversation_database.add_message(message)\n            logging.debug(f"\\n{\'-\' * 120}")\n        self.chat_provider = OpenAIChatCompletionProvider(model=self.config.model, temperature=self.config.temperature, stream=self.config.stream, conversation=self.agent_conversation_database, functions=self.functions)\n        self._initialized = True\n        logger.debug(f\'Initializing with System Instruction -- \\n\\n{self.config.system_instruction}\\n\\n\')\n        logger.debug(f"\\n{\'-\' * 60}\\nSession ID: {self.config.session_id}\\n{\'-\' * 60}\\n\\n")\n\n    def _get_termination_tool(self) -> OpenAITool:\n\n        def terminate(result: str):\n            self.completed = True\n            return result\n        return OpenAITool(name=\'call_termination\', description=\'Terminates the conversation.\', properties={\'result\': {\'type\': \'string\', \'description\': \'The final result of the conversation.\'}}, required=[\'result\'], function=terminate)""",
            0.90,
        ),
    ],
)
def test_agent_execution_similarity(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    expected_result,
    min_similarity,
):
    initialize_automata()

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkit_list
    )
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)
    config_name = AgentConfigName(agent_config_name)
    agent_config_builder = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(model)
    )

    agent_config_builder = agent_config_builder.with_max_iterations(
        max_iterations
    )

    agent = OpenAIAutomataAgent(
        instructions, config=agent_config_builder.build()
    )
    result = agent.run()
    result = result.replace("Execution Result:\n", "").strip()
    print("result = ", result)

    provider = OpenAIEmbeddingProvider()
    similarity = calculate_similarity(result, expected_result, provider)
    print("similarity = ", similarity)
    if similarity < min_similarity:
        raise ValueError(
            f"Found a similarity of {similarity} required {min_similarity}."
        )
