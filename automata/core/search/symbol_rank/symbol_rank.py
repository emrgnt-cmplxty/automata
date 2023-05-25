from typing import Dict, Hashable, List, Optional, Tuple

import networkx as nx
from networkx.exception import NetworkXError
from pydantic import BaseModel


class SymbolRankConfig(BaseModel):
    alpha: float = 0.85
    max_iterations: int = 100
    tolerance: float = 1.0e-6
    weight_key: str = "weight"

    @classmethod
    def validate(cls, config):
        """
        Validate configuration parameters.

        Args:
            config (SymbolRankConfig): Configuration parameters.

        Raises:
            ValueError: If alpha is not in (0, 1), or tolerance is not in (1e-4, 1e-8).
        """
        if not 0 < config.alpha < 1:
            raise ValueError(f"alpha must be in (0,1), but got {config.alpha}")

        if not 1.0e-8 < config.tolerance < 1.0e-4:
            raise ValueError(f"tolerance must be in (1e-4,1e-8), but got {config.tolerance}")


class SymbolRank:
    """SymbolRank class to compute SymbolRank values of nodes in a graph."""

    def __init__(self, graph: nx.DiGraph, config: Optional[SymbolRankConfig] = None):
        if not config:
            config = SymbolRankConfig()
        self.graph = graph
        self.config = config
        self.config.validate(self.config)

    def get_ranks(
        self,
        symbol_similarity: Optional[Dict[str, float]] = None,
        initial_weights: Optional[Dict[str, float]] = None,
        dangling: Optional[Dict[str, float]] = None,
    ) -> List[Tuple[str, float]]:
        """
        Calculate and return the SymbolRank of each node in the graph.

        Args:
            symbol_similarity (Optional[Dict[str, float]]): symbol_similarity dictionary.
            initial_weights (Optional[Dict[str, float]]): Initial weights dictionary.
            dangling (Optional[list]): List of dangling nodes.

        Returns:
            (Dict[str, float]): A dictionary mapping each node to its SymbolRank.
        """
        stochastic_graph = self._prepare_graph()
        node_count = stochastic_graph.number_of_nodes()

        rank_vec = self._prepare_initial_ranks(stochastic_graph, initial_weights)
        prepared_similarity = self._prepare_symbol_similarity(
            node_count, stochastic_graph, symbol_similarity
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

    def _prepare_graph(self) -> nx.DiGraph:
        """
        Prepare the graph for the SymbolRank algorithm. If the graph is not directed,
        convert it to a directed graph. Create a stochastic graph from the given graph.

        Returns:
            stochastic_graph (nx.DiGraph): A NetworkX stochastic DiGraph.
        """
        if not self.graph.is_directed():
            direct_graph = self.graph.to_directed()
        else:
            direct_graph = self.graph

        stochastic_graph = nx.stochastic_graph(direct_graph, weight=self.config.weight_key)
        return stochastic_graph

    def _prepare_initial_ranks(
        self, stochastic_graph: nx.DiGraph, initial_weights: Optional[Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Prepare initial rank values for each node in the graph.

        Args:
            stochastic_graph (nx.DiGraph): A NetworkX DiGraph.
            initial_weights (Optional[Dict[str, float]]): Initial weight for each node.

        Returns:
            (Dict[str, float]): A dictionary mapping each node to its initial rank.
        """

        node_count = stochastic_graph.number_of_nodes()
        if initial_weights is None:
            return {k: 1.0 / node_count for k in stochastic_graph}
        else:
            s = sum(initial_weights.values())
            return {k: v / s for k, v in initial_weights.items()}

    def _prepare_symbol_similarity(
        self,
        node_count: int,
        stochastic_graph: nx.DiGraph,
        symbol_similarity: Optional[Dict[str, float]],
    ) -> Dict[str, float]:
        """
        Prepare the symbol similarity matrix.
        Note - The term "personalization" is used in the context of the PageRank algorithm to refer to a mechanism that allows
        the modification of the rank computation based on some user-defined preferences. In this instance, symbol similarity is
        an implementation of personalization that allows the modification of the rank computation based on symbol source-code similarity.

        Args:
            node_count (int): Number of nodes in the graph.
            stochastic_graph (nx.DiGraph): A NetworkX DiGraph.
            symbol_similarity (Optional[Dict[str, float]]): Initial symbol similarity for each node.
        """
        if symbol_similarity is None:
            return {k: 1.0 / node_count for k in stochastic_graph}
        else:
            missing = set(self.graph) - set(symbol_similarity)
            if missing:
                raise NetworkXError(
                    "symbol_similarity dictionary must have a value for every node. Missing nodes %s"
                    % missing
                )
            s = sum(symbol_similarity.values())
            return {k: v / s for k, v in symbol_similarity.items()}

    def _prepare_dangling_weights(
        self, dangling: Optional[Dict[str, float]], symbol_similarity: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Prepare the weights for dangling nodes.

        Args:
            dangling (list): List of dangling nodes.
            symbol_similarity (Dict[str, float]): symbol_similarity dictionary.

        Returns:
            (Dict[str, float]): A dictionary mapping each node to its weight.
        """
        if dangling is None:
            return symbol_similarity
        else:
            missing = set(self.graph) - set(dangling)
            if missing:
                raise NetworkXError(
                    "Dangling node dictionary must have a value for every node. Missing nodes %s"
                    % missing
                )
            s = sum(dangling.values())
            return {k: v / s for k, v in dangling.items()}

    def _get_dangling_nodes(self, stochastic_graph: nx.DiGraph) -> List[Hashable]:
        """
        Identify dangling nodes in the graph.

        Args:
            stochastic_graph (nx.DiGraph): A NetworkX DiGraph.

        Returns:
            (list): List of dangling nodes.
        """
        return [
            node
            for node in stochastic_graph
            if stochastic_graph.out_degree(node, weight=self.config.weight_key) == 0.0
        ]
