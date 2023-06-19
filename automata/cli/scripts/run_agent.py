import logging
from typing import Any, Set

from automata.config.agent_config_builder import AutomataAgentConfigBuilder
from automata.config.config_types import AgentConfigName
from automata.core.agent.agent import AutomataAgent
from automata.core.agent.tools.tool_utils import (
    AgentToolFactory,
    DependencyFactory,
    build_llm_toolkits,
)
from automata.core.base.tool import ToolkitType

logger = logging.getLogger(__name__)


def main(*args, **kwargs):
    """
    Runs the main automata agent
    """
    logger.info("Building toolkits...")

    instructions = kwargs.get("instructions", "This is a dummy instruction, return True.")
    tool_list = kwargs.get("tools", "context_oracle").split(",")

    # A list of all dependencies that will be used to build the toolkits
    dependencies: Set[Any] = set()
    for tool in tool_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[ToolkitType(tool)]:
            dependencies.add(dependency_name)
    kwargs = {}
    logger.info("  - Building dependencies...")
    for dependency in dependencies:
        logger.info(f"Building {dependency}...")
        kwargs[dependency] = DependencyFactory().get(dependency)
    print("kwargs = ", kwargs)

    llm_toolkits = build_llm_toolkits(tool_list, **kwargs)
    logger.info("Done building toolkits...")

    config_name = AgentConfigName.AUTOMATA_RETRIEVER
    agent_config = (
        AutomataAgentConfigBuilder.from_name(config_name)
        .with_llm_toolkits(llm_toolkits)
        .with_model("gpt-3.5-turbo-16k")
        .build()
    )

    agent = AutomataAgent(instructions, config=agent_config)
    agent.setup()
    return agent.run()


#     DEFAULT_SCIP_FPATH = os.path.join(config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

#     graph = SymbolGraph(DEFAULT_SCIP_FPATH)
#     subgraph = graph.get_rankable_symbol_subgraph()

#     code_embedding_fpath = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
#     )
#     embedding_provider = OpenAIEmbedding()
#     code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
#     code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)

#     symbol_similarity = SymbolSimilarity(code_embedding_handler)
#     symbol_search = SymbolSearch(
#         graph,
#         symbol_similarity,
#         symbol_rank_config=SymbolRankConfig(),
#         code_subgraph=subgraph,
#     )
#     retriever = PyContextRetriever(graph)

#     doc_embedding_fpath = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
#     )
#     doc_embedding_db = JSONVectorDatabase(doc_embedding_fpath)
#     doc_embedding_handler = SymbolDocEmbeddingHandler(
#         doc_embedding_db, embedding_provider, symbol_search, retriever
#     )

#     symbol_doc_similarity = SymbolSimilarity(doc_embedding_handler)

#     llm_toolkits = build_llm_toolkits(
#         tool_list, symbol_search=symbol_search, symbol_doc_similarity=symbol_doc_similarity
#     )
#     logger.info("Done building toolkits...")

#     config_name = AgentConfigName.AUTOMATA_RETRIEVER
#     agent_config = (
#         AutomataAgentConfigBuilder.from_name(config_name)
#         .with_llm_toolkits(llm_toolkits)
#         .with_model("gpt-3.5-turbo-16k")
#         .build()
#     )

#     agent = AutomataAgent(instructions, config=agent_config)
#     agent.setup()
#     return agent.run()


# class DependencyFactory:
#     """Creates dependencies for input Toolkit construction."""

#     DEFAULT_SCIP_FPATH = os.path.join(config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

#     DEFAULT_CODE_EMBEDDING_FPATH = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
#     )

#     DEFAULT_DOC_EMBEDDING_FPATH = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
#     )

#     def __init__(self, **kwargs):
#         """
#         overrides = {
#             embedding_provider - Defaults to OpenAIEmbedding()
#             symbol_graph_path - Defaults to DependencyFactory.DEFAULT_SCIP_FPATH
#             code_embedding_fpath - Defaults to DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
#             doc_embedding_fpath - Defaults to DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
#         }
#         """
#         self._instances = {}
#         self.overrides = kwargs

#     def get(self, dependency):
#         if dependency in self.overrides:
#             return self.overrides[dependency]

#         if dependency in self._instances:
#             return self._instances[dependency]

#         method_name = f"create_{dependency.__name__.lower()}"
#         if hasattr(self, method_name):
#             creation_method = getattr(self, method_name)
#             instance = creation_method()
#         else:
#             instance = dependency()

#         self._instances[dependency] = instance

#         return instance

#     def create_symbol_graph(self):
#         if "symbol_graph" not in self._instances:
#             self._instances["symbol_graph"] = SymbolGraph(
#                 self.overrides.get("symbol_graph_path", DependencyFactory.DEFAULT_SCIP_FPATH)
#             )

#     def create_symbol_code_similarity(self):
#         if "symbol_code_similarity" not in self._instances:
#             code_embedding_fpath = self.overrides.get(
#                 "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
#             )
#             code_embedding_db = JSONVectorDatabase(code_embedding_fpath)

#             embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbedding())
#             code_embedding_handler = SymbolCodeEmbeddingHandler(
#                 code_embedding_db, embedding_provider
#             )
#             self._instances["symbol_code_similarity"] = SymbolSimilarity(code_embedding_handler)

#     def create_symbol_doc_similarity(self):
#         if "symbol_doc_similarity" not in self._instances:
#             doc_embedding_fpath = self.overrides.get(
#                 "doc_embedding_fpath", DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
#             )
#             doc_embedding_db = JSONVectorDatabase(doc_embedding_fpath)

#             embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbedding())
#             symbol_search = self.get(SymbolSearch)
#             py_context_retriever = self.get(PyContextRetriever)

#             doc_embedding_handler = SymbolDocEmbeddingHandler(
#                 doc_embedding_db, embedding_provider, symbol_search, py_context_retriever
#             )
#             self._instances["symbol_doc_similarity"] = SymbolSimilarity(doc_embedding_handler)

#     #     # if 'symbol_graph' not in self._instances:
#     #     #     if "symbol_graph_path" in self.dependency_overrides:
#     #     #         self._instances['symbol_graph'] = SymbolGraph(self.dependency_overrides["symbol_graph_path"])
#     #     #     else:
#     #     #         self._instances['symbol_graph'] = SymbolGraph()

#     # def create_symbolsearch(self):
#     #     if not 'symbolsearch' in self._instances:
#     #         if 'symbol_graph' not in self._instances:
#     #             self.create_symbol_graph()
#     #         self._instances['symbolsearch'] = SymbolSearch(self._instances['symbol_graph'])
#     #     # ... same as before ...

#     # def create_symbolsimilarity(self):
#     #     # ... same as before ...

#     # def create_pycontextretriever(self):
#     #     # ... same as before ...


# def main(*args, **kwargs):
#     """
#     Runs the main automata agent
#     """
#     logger.info("Building toolkits...")

#     instructions = kwargs.get("instructions", "This is a dummy instruction, return True.")
#     tool_list = kwargs.get("tools", "context_oracle").split(",")
#     DEFAULT_SCIP_FPATH = os.path.join(config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

#     graph = SymbolGraph(DEFAULT_SCIP_FPATH)
#     subgraph = graph.get_rankable_symbol_subgraph()

#     code_embedding_fpath = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
#     )
#     embedding_provider = OpenAIEmbedding()
#     code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
#     code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)

#     symbol_similarity = SymbolSimilarity(code_embedding_handler)
#     symbol_search = SymbolSearch(
#         graph,
#         symbol_similarity,
#         symbol_rank_config=SymbolRankConfig(),
#         code_subgraph=subgraph,
#     )
#     retriever = PyContextRetriever(graph)

#     doc_embedding_fpath = os.path.join(
#         config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
#     )
#     doc_embedding_db = JSONVectorDatabase(doc_embedding_fpath)
#     doc_embedding_handler = SymbolDocEmbeddingHandler(
#         doc_embedding_db, embedding_provider, symbol_search, retriever
#     )

#     symbol_doc_similarity = SymbolSimilarity(doc_embedding_handler)

#     llm_toolkits = build_llm_toolkits(
#         tool_list, symbol_search=symbol_search, symbol_doc_similarity=symbol_doc_similarity
#     )
#     logger.info("Done building toolkits...")

#     config_name = AgentConfigName.AUTOMATA_RETRIEVER
#     agent_config = (
#         AutomataAgentConfigBuilder.from_name(config_name)
#         .with_llm_toolkits(llm_toolkits)
#         .with_model("gpt-3.5-turbo-16k")
#         .build()
#     )

#     agent = AutomataAgent(instructions, config=agent_config)
#     agent.setup()
#     return agent.run()
