# import json
# import os
# from copy import deepcopy

# import pytest

# from automata.configs.config_enums import ConfigCategory
# from automata.core.search.symbol_converter import SymbolConverter
# from automata.core.search.symbol_graph import SymbolGraph
# from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
# from automata.core.search.symbol_rank.symbol_rank import SymbolRank, SymbolRankConfig
# from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
# from automata.core.search.symbol_searcher import SymbolSearcher
# from automata.core.search.symbol_types import Symbol, SymbolEmbedding

# TEST_QUERIES = {
#     "symbol_references": "test_symbol_uri",
#     "symbol_rank": "test_query",
#     "exact": "test_pattern",
#     "source": "test_symbol_uri",
#     "replace": "test_find test_replace True",
# }

# # def get_searcher() -> SymbolSearcher:
# # def setup_module(module):
# #     file_dir = os.getcwd()

# #     scip_path = os.path.join(
# #         file_dir, "..", "configs", ConfigCategory.SYMBOLS.value, "index.scip"
# #     )
# #     embedding_path = os.path.join(
# #         file_dir, "..", "configs", ConfigCategory.SYMBOLS.value, "symbol_embedding.json"
# #     )
# #     # Initialize symbol converter
# #     module.symbol_converter = SymbolConverter()

# #     # Initialize symbol graph and get subgraph
# #     module.symbol_graph = SymbolGraph(scip_path, symbol_converter)

# #     # Load symbol embedding map
# #     module.symbol_embedding_map = SymbolEmbeddingMap(load_embedding_map=True, embedding_path=embedding_path)

# #     # Initialize symbol similarity
# #     module.symbol_similarity = SymbolSimilarity(symbol_embedding_map)

# #     module.symbol_searcher = SymbolSearcher(symbol_converter, symbol_graph, symbol_embedding_map, symbol_similarity, SymbolRankConfig(alpha=0.25))

# # @pytest.mark.parametrize("query_type, query_content", TEST_QUERIES.items())
# # def test_process_queries(query_type, query_content):
# #     result = symbol_searcher.process_query(f"type:{query_type} {query_content}")

# #     with open(f"./expected_results/{query_type}_expected_result.json") as f:
# #         expected_result = json.load(f)
# #     assert result == expected_result

# # def test_invalid_query():
# #     with pytest.raises(ValueError):
# #         symbol_searcher.process_query("invalid_query")

# # def test_unknown_query_type():
# #     with pytest.raises(ValueError):
# #         symbol_searcher.process_query("type:unknown query")

# # def generate_expected_results():
# #     for query_type, query_content in TEST_QUERIES.items():
# #         result = symbol_searcher.process_query(f"type:{query_type} {query_content}")

# #         with open(f"./expected_results/{query_type}_expected_result.json", "w") as f:
# #             json.dump(result, f)

# # if __name__ == "__main__":
# #     # Call this function whenever you want to regenerate the expected results
# #     generate_expected_results()

# #     # Call this to run the tests
# #     pytest.main([os.path.realpath(__file__)])
