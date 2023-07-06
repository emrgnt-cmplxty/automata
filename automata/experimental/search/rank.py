from typing import Dict, Hashable, List, Optional, Tuple

import networkx as nx
from networkx.exception import NetworkXError
from pydantic import BaseModel

from automata.symbol.base import Symbol


class SymbolRankConfig(BaseModel):
    """A configuration class for SymbolRank"""

    alpha: float = 0.25
    max_iterations: int = 100
    tolerance: float = 1.0e-6
    weight_key: str = "weight"

    @staticmethod
    def validate_config(config) -> None:
        """
        Raises:
            ValueError: If alpha is not in (0, 1), or tolerance is not in (1e-4, 1e-8).
        """
        if not 0 < config.alpha < 1:
            raise ValueError(f"alpha must be in (0,1), but got {config.alpha}")

        if not 1.0e-8 < config.tolerance < 1.0e-4:
            raise ValueError(f"tolerance must be in (1e-4,1e-8), but got {config.tolerance}")


class SymbolRank:
    """Computes the PageRank algorithm on symbols in a graph"""

    def __init__(self, graph: nx.DiGraph, config: SymbolRankConfig) -> None:
        self.graph = graph
        self.config = config
        self.config.validate_config(self.config)

    def get_ranks(
        self,
        query_to_symbol_similarity: Optional[Dict[Symbol, float]] = None,
        initial_weights: Optional[Dict[Symbol, float]] = None,
        dangling: Optional[Dict[Symbol, float]] = None,
    ) -> List[Tuple[Symbol, float]]:
        # sourcery skip: inline-immediately-returned-variable, use-dict-items
        """
        Calculate the SymbolRanks of each node in the graph.

        SymbolRank is a semantic code analyzer for software corpora. Leveraging language models
        and graph theory, SymbolRank assesses and ranks symbols such as classes and methods based
        on their semantic context and structural relationships within the software. The algorithm
        starts by embedding a global context using a concrete implementation of the
        SymbolEmbeddingHandler class, which applies a provider to generate vector representations
        of each symbol in the source code.

        These embeddings capture the semantic essence of the symbols, providing a basis for the
        subsequent stages of the process. Simultaneously, the software corpus is used to construct
        a SymbolGraph. Each symbol in the corpus becomes a node in this graph, with dependencies
        between symbols forming the edges. The graph provides a comprehensive map of structural
        information in the codebase, offering methods to understand symbol dependencies,
        relationships, callers, and callees, and the ability to produce a rankable subgraph of
        symbols.

        The SymbolRank class then uses a prepared similarity dictionary for a given query and
        the SymbolGraph. The algorithm subsequently executes an iterative computation akin to
        Google's PageRank, but considers both the symbols' similarity scores to the query and
        their  connectivity within the graph. This amalgamation of natural language processing,
        information retrieval, and graph theory methods results in a ranking of code symbols,
        significantly aiding tasks like code understanding, navigation, recommendation, and search.
        """
        stochastic_graph = self._prepare_graph()
        node_count = stochastic_graph.number_of_nodes()

        rank_vec = self._prepare_initial_ranks(stochastic_graph, initial_weights)
        prepared_similarity = self._prepare_query_to_symbol_similarity(
            node_count, stochastic_graph, query_to_symbol_similarity
        )
        dangling_weights = self._prepare_dangling_weights(dangling, prepared_similarity)
        dangling_nodes = self._get_dangling_nodes(stochastic_graph)

        for _ in range(self.config.max_iterations):
            last_rank_vec = rank_vec
            rank_vec = {k: 0.0 for k in last_rank_vec.keys()}
            danglesum = self.config.alpha * sum(last_rank_vec[node] for node in dangling_nodes)  # type: ignore
            for node in rank_vec:
                for nbr in stochastic_graph[node]:
                    rank_vec[nbr] += (
                        self.config.alpha
                        * last_rank_vec[node]
                        * stochastic_graph[node][nbr][self.config.weight_key]
                    )
                rank_vec[node] += (
                    danglesum * dangling_weights[node]
                    + (1.0 - self.config.alpha) * prepared_similarity[node]
                )

            err = sum(abs(rank_vec[node] - last_rank_vec[node]) for node in rank_vec)
            if err < node_count * self.config.tolerance:
                sorted_dict = sorted(rank_vec.items(), key=lambda x: x[1], reverse=True)
                return sorted_dict

        raise NetworkXError(
            "SymbolRank: power iteration failed to converge in %d iterations."
            % self.config.max_iterations
        )

    def get_top_symbols(self, n: int) -> List[Tuple[str, float]]:
        """
        Get the top N symbols according to their ranks.

        Args:
            n: The number of top symbols to retrieve.

        Returns:
            A list of tuples each containing the dotpath of a symbol and its rank.
        """
        ranks = self.get_ranks()
        return [(".".join(symbol.dotpath.split(".")[1:]), rank) for symbol, rank in ranks[:n]]

    def _prepare_graph(self) -> nx.DiGraph:
        """
        Prepare the graph for the SymbolRank algorithm. If the graph is not directed,
        convert it to a directed graph, then create a stochastic graph from the directed graph.
        """
        if not self.graph.is_directed():
            directed_graph = self.graph.to_directed()
        else:
            directed_graph = self.graph

        stochastic_graph = nx.stochastic_graph(directed_graph, weight=self.config.weight_key)
        return stochastic_graph

    def _prepare_initial_ranks(
        self,
        stochastic_graph: nx.DiGraph,
        initial_weights: Optional[Dict[Symbol, float]],
    ) -> Dict[Symbol, float]:
        """
        Prepare initial rank values for each node in the graph.
        If initial weights are not provided, set the initial rank value for each node to 1/n.
        """

        node_count = stochastic_graph.number_of_nodes()
        if initial_weights is None:
            return {k: 1.0 / node_count for k in stochastic_graph}
        s = sum(initial_weights.values())
        return {k: v / s for k, v in initial_weights.items()}

    def _prepare_query_to_symbol_similarity(
        self,
        node_count: int,
        stochastic_graph: nx.DiGraph,
        query_to_symbol_similarity: Optional[Dict[Symbol, float]],
    ) -> Dict[Symbol, float]:
        """
        Prepare the similarity input dictionary for the SymbolRank algorithm.

        Raises:
            NetworkXError: If the query_to_symbol_similarity dictionary does not have a value for every node

        Note - Similarity is the same as "personalization" in the context of the original PageRank algorithm
            Personalization modifies the rank computation based on user-defined preferences.

            In this instance, symbol similarity is an implementation of personalization that allows
            the modification of the rank computation based on symbol source-code similarity

        """
        if query_to_symbol_similarity is None:
            return {k: 1.0 / node_count for k in stochastic_graph}
        missing = set(self.graph) - set(query_to_symbol_similarity)
        if missing:
            raise NetworkXError(
                f"query_to_symbol_similarity dictionary must have a value for every node. Missing {len(missing)} nodes."
            )
        s = sum(query_to_symbol_similarity.values())
        return {k: v / s for k, v in query_to_symbol_similarity.items()}

    def _prepare_dangling_weights(
        self,
        dangling: Optional[Dict[Symbol, float]],
        query_to_symbol_similarity: Dict[Symbol, float],
    ) -> Dict[Symbol, float]:
        if dangling is None:
            return query_to_symbol_similarity
        missing = set(self.graph) - set(dangling)
        if missing:
            raise NetworkXError(
                f"Dangling node dictionary must have a value for every node. Missing nodes {missing}"
            )
        s = sum(dangling.values())
        return {k: v / s for k, v in dangling.items()}

    def _get_dangling_nodes(self, stochastic_graph: nx.DiGraph) -> List[Hashable]:
        return [
            node
            for node in stochastic_graph
            if stochastic_graph.out_degree(node, weight=self.config.weight_key) == 0.0
        ]
