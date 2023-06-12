import os
from typing import Optional

import networkx as nx

from configs.config_enums import ConfigCategory
from automata_docs.core.search.symbol_graph import SymbolGraph
from automata_docs.core.search.symbol_rank.symbol_embedding_map import (
    SymbolEmbeddingMap,
)
from automata_docs.core.search.symbol_rank.symbol_rank import (
    SymbolRank,
    SymbolRankConfig,
)
from automata_docs.core.search.symbol_rank.symbol_similarity import (
    NormType,
    SymbolSimilarity,
)
from automata_docs.core.utils import config_path
from tools.search.symbol_searcher import SymbolSearcher


class SymbolFactory:
    def create(self, *args, **kwargs):
        raise NotImplementedError


class SymbolGraphFactory(SymbolFactory):
    def create(
        self, index_path: Optional[str] = None, build_caller_relationships: bool = False
    ) -> SymbolGraph:
        """
        Creates a SymbolGraph object.

        Args:
            index_path (str): Path to the index file.
        """
        if not index_path:
            index_path = os.path.join(config_path(), ConfigCategory.SYMBOLS.value, "index.scip")
        return SymbolGraph(index_path, build_caller_relationships)


class SymbolEmbeddingMapFactory(SymbolFactory):
    def create(self, *args, **kwargs) -> SymbolEmbeddingMap:
        """
        Creates a SymbolEmbeddingMap object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        return SymbolEmbeddingMap(*args, **kwargs)


class SymbolSimilarityFactory(SymbolFactory):
    def create(
        self,
        symbol_embedding_map: SymbolEmbeddingMap,
        norm_type: NormType = NormType.L2,
    ) -> SymbolSimilarity:
        """
        Creates a SymbolSimilarity object.

        Args:
            symbol_embedding_map (SymbolEmbeddingMap): Symbol embedding map.
            norm_type (NormType): Type of norm to use for calculating similarity.
        """
        return SymbolSimilarity(symbol_embedding_map, norm_type)


class SymbolRankFactory(SymbolFactory):
    def create(self, graph: nx.DiGraph, config: Optional[SymbolRankConfig] = None) -> SymbolRank:
        """
        Creates a SymbolRank object.

        Args:
            graph (nx.DiGraph): Symbol graph.
            config (SymbolRankConfig): Configuration for the SymbolRank object.
        """
        return SymbolRank(graph, config)


class SymbolSearcherFactory(SymbolFactory):
    def create(
        self,
        symbol_graph_factory: SymbolGraphFactory = SymbolGraphFactory(),
        symbol_embedding_map_factory: SymbolEmbeddingMapFactory = SymbolEmbeddingMapFactory(),
        symbol_similarity_factory: SymbolSimilarityFactory = SymbolSimilarityFactory(),
        symbol_rank_config: Optional[SymbolRankConfig] = None,
        *args,
        **kwargs,
    ) -> SymbolSearcher:
        """
        Creates a SymbolSearcher object.

        Args:
            symbol_converter_factory (SymbolConverterFactory): Factory for creating a SymbolConverter object.
            symbol_graph_factory (SymbolGraphFactory): Factory for creating a SymbolGraph object.
            symbol_embedding_map_factory (SymbolEmbeddingMapFactory): Factory for creating a SymbolEmbeddingMap object.
            symbol_similarity_factory (SymbolSimilarityFactory): Factory for creating a SymbolSimilarity object.
            symbol_rank_config (SymbolRankConfig): Configuration for the SymbolRank object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Instantiate the SymbolConverter

        # Paths for SCIP file and Embedding map file
        scip_path = os.path.join(
            config_path(),
            ConfigCategory.SYMBOLS.value,
            kwargs.get("index_name", "index.scip"),
        )
        embedding_path = os.path.join(
            config_path(),
            ConfigCategory.SYMBOLS.value,
            kwargs.get("symbol_embedding_name", "symbol_embedding.json"),
        )

        # Instantiate the SymbolGraph
        symbol_graph = symbol_graph_factory.create(scip_path)

        # Instantiate the SymbolEmbeddingMap
        symbol_embedding_map = symbol_embedding_map_factory.create(
            load_embedding_map=True, embedding_path=embedding_path
        )

        # Instantiate the SymbolSimilarity
        symbol_similarity = symbol_similarity_factory.create(symbol_embedding_map)

        # Create a SymbolSearcher using the instantiated classes
        return SymbolSearcher(
            symbol_graph,
            symbol_embedding_map,
            symbol_similarity,
            symbol_rank_config,
            *args,
            **kwargs,
        )
