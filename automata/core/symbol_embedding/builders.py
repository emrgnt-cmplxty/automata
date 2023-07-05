from typing import List

from jinja2 import Template

from automata.config.prompt.doc_generation import DEFAULT_DOC_GENERATION_PROMPT
from automata.core.code_handling.py.reader import PyReader
from automata.core.embedding.base import EmbeddingBuilder, EmbeddingVectorProvider
from automata.core.experimental.search.symbol_search import SymbolSearch
from automata.core.llm.foundation import LLMChatCompletionProvider
from automata.core.retrievers.py.context import PyContextRetriever
from automata.core.symbol.base import Symbol
from automata.core.symbol.symbol_utils import convert_to_fst_object
from automata.core.symbol_embedding.base import SymbolCodeEmbedding, SymbolDocEmbedding


class SymbolCodeEmbeddingBuilder(EmbeddingBuilder):
    """Builds `Symbol` source code embeddings."""

    def build(self, source_code: str, symbol: Symbol) -> SymbolCodeEmbedding:
        embedding_vector = self.embedding_provider.build_embedding_vector(source_code)
        return SymbolCodeEmbedding(symbol, source_code, embedding_vector)


class SymbolDocEmbeddingBuilder(EmbeddingBuilder):
    """Builds `Symbol` documentation embeddings."""

    # TODO - Make this class more modular and consider it's structure
    def __init__(
        self,
        embedding_provider: EmbeddingVectorProvider,
        completion_provider: LLMChatCompletionProvider,
        symbol_search: SymbolSearch,
        retriever: PyContextRetriever,
    ) -> None:
        super().__init__(embedding_provider)
        self.symbol_search = symbol_search
        self.retriever = retriever
        self.completion_provider = completion_provider

    def build(self, source_code: str, symbol: Symbol) -> SymbolDocEmbedding:
        """
        Build the embedding for a symbol's documentation.
        Example Document Output:
        ===========
        AgentConfig
        ===========
        ``AgentConfig`` is an abstract base class that provides a template for
        configurations related to providers. It contains abstract methods like
        ``setup()`` and ``load()`` that need to be implemented by subclasses.
        This class also handles the configuration of arbitrary types during the
        initialization.
        Overview
        --------
        ``AgentConfig`` is designed for ensuring configurability of providers.
        Subclasses need to provide implementations for the ``setup()`` and
        ``load()`` methods in order to properly define the behavior during the
        agent setup and configuration loading processes. This class follows the
        BaseModel design, making it easy to extend and customize according to
        specific agent requirements.
        Related Symbols
        ---------------
        -  ``automata.core.agent.instances.OpenAIAutomataAgentInstance.Config``
        -  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
        -  ``automata.tests.unit.test_task_environment.TestURL``
        -  ``automata.core.agent.agent.AgentInstance.Config``
        Example
        -------
        The following example demonstrates how to create a custom agent
        configuration by extending the ``AgentConfig`` class:
        .. code:: python
        from config.config_types import AgentConfig
        class CustomAgentConfig(AgentConfig):
            def setup(self):
                # Define your custom agent setup process
                pass
            @classmethod
            def load(cls, config_name: AgentConfigName) -> "CustomAgentConfig":
                # Load the config for your custom agent
                pass
        Limitations
        -----------
        ``AgentConfig`` itself is an abstract class and cannot directly be
        instantiated. It must be subclassed, and its methods need to be
        implemented by the extending class according to the specific agent
        requirements. Additionally, the current implementation allows for
        arbitrary types, which may lead to code that is not type-safe.
        Follow-up Questions:
        --------------------
        -  How can we ensure type safety while maintaining the flexibility and
        customizability provided by ``AgentConfig``?
        """
        abbreviated_selected_symbol = symbol.uri.split("/")[1].split("#")[0]
        search_list = self.generate_search_list(abbreviated_selected_symbol)
        self.retriever.reset()
        self.retriever.process_symbol(symbol, search_list)

        prompt = Template(DEFAULT_DOC_GENERATION_PROMPT).render(
            symbol_dotpath=abbreviated_selected_symbol,
            symbol_context=self.retriever.get_context_buffer(),
        )

        document = self.completion_provider.standalone_call(prompt)
        summary = self.completion_provider.standalone_call(
            f"Condense the documentation below down to one to two concise paragraphs:\n {document}\nIf there is an example, include that in full in the output."
        )
        embedding = self.embedding_provider.build_embedding_vector(document)

        return SymbolDocEmbedding(
            symbol,
            vector=embedding,
            source_code=source_code,
            document=document,
            summary=summary,
            context=prompt,
        )

    def build_non_class(self, source_code: str, symbol: Symbol) -> SymbolDocEmbedding:
        ast_object = convert_to_fst_object(symbol)
        raw_doctring = PyReader.get_docstring_from_node(ast_object)
        document = f"Symbol: {symbol.dotpath}\n{raw_doctring}"

        embedding = self.embedding_provider.build_embedding_vector(document)

        return SymbolDocEmbedding(
            symbol,
            vector=embedding,
            source_code=source_code,
            document=document,
            summary=document,
            context="",
        )

    def generate_search_list(self, abbreviated_selected_symbol: str) -> List[Symbol]:
        """Generate a search list by splicing the search results on the symbol with the search results biased on tests."""
        search_results = self.symbol_search.symbol_rank_search(f"{abbreviated_selected_symbol}")
        search_results_with_tests = [ele for ele in search_results if "test" in ele[0].uri]
        search_results_without_tests = [ele for ele in search_results if "test" not in ele[0].uri]
        search_list: List[Symbol] = []
        for i in range(max(len(search_results_with_tests), len(search_results_without_tests))):
            set_list = set(search_list)
            if i < len(search_results_with_tests) and search_results_with_tests[i] not in set_list:
                search_list.append(search_results_with_tests[i][0])
            if (
                i < len(search_results_without_tests)
                and search_results_without_tests[i] not in set_list
            ):
                search_list.append(search_results_without_tests[i][0])
        return search_list
