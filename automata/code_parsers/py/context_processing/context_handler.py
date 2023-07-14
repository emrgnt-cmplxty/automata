from typing import TYPE_CHECKING, Dict, List, Set

from automata.code_parsers.py.context_processing.context_retriever import (
    ContextComponent,
    PyContextRetriever,
)

if TYPE_CHECKING:
    from automata.experimental.search import SymbolSearch
    from automata.symbol import Symbol


class PyContextHandlerConfig:
    """The configuration for the PyContextHandlerConfig"""

    def __init__(
        self,
        top_n_symbol_rank_matches: int = 5,
        top_n_dependency_matches: int = 5,
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
        self.obs_symbols: Set["Symbol"] = set([])

    def construct_symbol_context(
        self,
        symbol: "Symbol",
        primary_active_components: Dict[ContextComponent, Dict],
        tertiary_active_components: Dict[ContextComponent, Dict],
        related_symbols_header="Related Symbols:",
        dependent_symbols_header="Dependent Symbols:",
    ) -> str:
        """Construct the context for a symbol."""
        self.obs_symbols.add(symbol)
        base_context = f"{self.retriever.process_symbol(symbol, primary_active_components)}"

        if self.config.top_n_symbol_rank_matches > 0:
            base_context += (
                f"\n{self.retriever.spacer}{related_symbols_header}\n\n"
            )
            secondary_symbols = self.get_top_n_symbol_rank_matches(symbol)
            for secondary_symbol in secondary_symbols:
                base_context += self.retriever.process_symbol(
                    secondary_symbol,
                    tertiary_active_components,
                    indent_level=2,
                )

        if self.config.top_n_dependency_matches > 0:
            base_context += (
                f"\n{self.retriever.spacer}{dependent_symbols_header}\n\n"
            )

            dependent_symbols = self.get_top_n_symbol_dependencies(symbol)
            for dependent_symbol in dependent_symbols:
                base_context += self.retriever.process_symbol(
                    dependent_symbol,
                    tertiary_active_components,
                    indent_level=2,
                )

        return base_context

    def get_top_n_symbol_rank_matches(
        self, symbol: "Symbol"
    ) -> List["Symbol"]:
        """Get the top N symbols according to their ranks."""
        query = symbol.descriptors[-1].name
        symbol_rank_results = self.symbol_search.get_symbol_rank_results(query)
        return [
            ele[0]
            for ele in symbol_rank_results[
                : self.config.top_n_symbol_rank_matches
            ]
        ]

    def get_top_n_symbol_dependencies(
        self, symbol: "Symbol"
    ) -> List["Symbol"]:
        """
        Get the tpo N symbols that the given symbol depends on.
        TODO - Sort results by some metric like similarity or ranked search.
        """
        symbol_dependencies = (
            self.symbol_search.symbol_graph.get_symbol_dependencies(symbol)
        )
        return list(symbol_dependencies)[
            : self.config.top_n_dependency_matches
        ]
