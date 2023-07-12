from typing import TYPE_CHECKING, Dict, List, Set

from automata.code_parsers.py.context_retriever import (
    ContextComponent,
    PyContextRetriever,
)
from automata.symbol import Symbol

if TYPE_CHECKING:
    from automata.experimental.search import SymbolSearch


class PyContextHandlerConfig:
    """The configuration for the PyContextHandlerConfig"""

    def __init__(
        self,
        top_n_symbol_rank_matches: int = 10,
        top_n_dependency_matches: int = 10,
    ) -> None:
        self.top_n_symbol_rank_matches = top_n_symbol_rank_matches
        self.top_n_dependency_matches = top_n_dependency_matches


class PyContextHandler:
    def __init__(
        self,
        config: PyContextHandlerConfig,
        retriever: PyContextRetriever,
        symbol_search: "SymbolSearch",
    ) -> None:
        self.config = config
        self.retriever = retriever
        self.symbol_search = symbol_search
        self.obs_symbols: Set[Symbol] = set([])

    def construct_symbol_context(
        self,
        symbol: Symbol,
        primary_active_components: Dict[ContextComponent, Dict],
        tertiary_active_components: Dict[ContextComponent, Dict],
    ) -> str:
        """Construct the context for a symbol."""
        self.obs_symbols.add(symbol)
        base_context = f"Primary Symbols:\n\n{self.retriever.process_symbol(symbol, primary_active_components)}"

        if self.config.top_n_symbol_rank_matches > 0:
            base_context += "Related Symbols:\n\n"
            secondary_symbols = self.get_top_n_symbol_rank_matches(symbol)
            for symbol in secondary_symbols:
                base_context += self.retriever.process_symbol(
                    symbol, tertiary_active_components, indent_level=1
                )

        if self.config.top_n_dependency_matches > 0:
            base_context += "Dependent Symbols:\n\n"
            secondary_symbols = self.get_top_n_symbol_dependencies(symbol)
            for symbol in secondary_symbols:
                base_context += self.retriever.process_symbol(
                    symbol, tertiary_active_components, indent_level=1
                )

        return base_context

    def get_top_n_symbol_rank_matches(self, symbol: Symbol) -> List[Symbol]:
        """Get the top N symbols according to their ranks."""
        query = symbol.descriptors[-1].name
        symbol_rank_results = self.symbol_search.get_symbol_rank_results(query)
        return [ele[0] for ele in symbol_rank_results[: self.config.top_n_symbol_rank_matches]]

    def get_top_n_symbol_dependencies(self, symbol: Symbol) -> List[Symbol]:
        """
        Get the tpo N symbols that the given symbol depends on.
        TODO - Sort results by some metric like similarity or ranked search.
        """
        symbol_dependencies = self.symbol_search.symbol_graph.get_symbol_dependencies(symbol)
        return list(symbol_dependencies)[: self.config.top_n_dependency_matches]

    # def handle_context(
    #     self,
    #     query: str,
    #     primary_symbol_components: Dict[ContextComponent, Dict],
    #     secondary_symbol_components: Dict[ContextComponent, Dict],
    # ) -> None:
    #     related_symbols = self.get_related_symbols(query)
    #     for symbol in related_symbols:
    #         self.retrieve_symbol_context(
    #             symbol,
    #             self.get_symbol_dependencies(symbol),
    #             primary_symbol_components,
    #             secondary_symbol_components,
    #         )


# class PyContextHandler:
#     def __init__(
#         self,
#         retriever: PyContextRetriever,
#         related_symbols: List[Symbol] = [],
#     ) -> None:
#         self.retriever = retriever
#         self.related_symbols = related_symbols
#         self.obs_symbols: Set[Symbol] = set([])

#     def retrieve_symbol_context(
#         self,
#         symbol: Symbol,
#         secondary_symbols: List[Symbol],
#         primary_symbol_components: Dict[ContextComponent, Dict],
#         secondary_symbol_components: Dict[ContextComponent, Dict],
#     ) -> None:
#         base_context = self.retriever.process_symbol(symbol, primary_symbol_components)

#         for symbol in secondary_symbols:
#             base_context += self.retriever.process_symbol(symbol, secondary_symbol_components)
