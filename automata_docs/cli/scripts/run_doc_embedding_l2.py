import logging
import os

from tqdm import tqdm

from automata_docs.configs.config_enums import ConfigCategory
from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.symbol_embedding import SymbolDocumentEmbeddingHandler
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_fpath

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    print("We are in run doc embedding l2....")
    scip_path = os.path.join(
        config_fpath(), ConfigCategory.SYMBOLS.value, kwargs.get("index_file", "index.scip")
    )
    embedding_path = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOLS.value,
        kwargs.get("embedding_file", "symbol_doc_embedding.json"),
    )
    print("embedding_path = ", embedding_path)

    symbol_graph = SymbolGraph(scip_path)
    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
    print("filtered_symbols[0:10] = ", filtered_symbols[0:10])
    embedding_db = JSONVectorDatabase(embedding_path)
    print("embedding db loaded...")
    embedding_handler = SymbolDocumentEmbeddingHandler(embedding_db)
    print("embedding handler loaded...")
    print("Calling update embedding...")
    for symbol in tqdm(filtered_symbols):
        print("Updating symbol = ", symbol)
        embedding_handler.update_embedding(symbol)
        # embedding_db.save()
    return "Success"


# import argparse
# import logging
# import textwrap
# from typing import Any, Dict, List
# from automata_docs.core.symbol.symbol_types import Symbol

# import openai

# from automata_docs.core.context.python_context.python_context_retriever import (
#     PythonContextRetriever,
# )
# from automata_docs.core.symbol.search.symbol_factory import (
#     SymbolGraphFactory,
#     SymbolRankFactory,
#     SymbolSearcherFactory,
# )
# from automata_docs.core.symbol.search.symbol_rank import SymbolRank, SymbolRankConfig
# from automata_docs.core.symbol.symbol_types import Symbol, SymbolDescriptor
# from automata_docs.core.symbol.symbol_utils import convert_to_fst_object
# from config import OPENAI_API_KEY

# logger = logging.getLogger(__name__)


# def get_filtered_ranked_symbols(kwargs: Dict[str, Any], ranker: SymbolRank) -> List[Symbol]:
#     selected_symbols = []
#     selection_filters = kwargs.get("selection_filters", "").split(",")
#     for symbol, _rank in ranker.get_ranks():
#         if symbol.symbol_kind_by_suffix() != SymbolDescriptor.PythonKinds.Class:
#             continue
#         if any(filter_ in symbol.uri for filter_ in selection_filters):
#             selected_symbols.append(symbol)
#             if len(set(selected_symbols)) >= kwargs.get("top_n_symbols", 0):
#                 break

#     return selected_symbols


# # def get_full_doc_completion(selected_symbol: Symbol, symbol_overview: str) -> str:
# #     example_0 = textwrap.dedent(
# #         '''
# #         ...
# #         ## Usage Example

# #         ```python
# #         from transformers import PegasusForConditionalGeneration, PegasusTokenizer
# #         import torch

# #         src_text = [
# #             """ PG&E .... """
# #         ]

# #         model_name = "google/pegasus-xsum"
# #         device = "cuda" if torch.cuda.is_available() else "cpu"
# #         tokenizer = PegasusTokenizer.from_pretrained(model_name)
# #         model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
# #         batch = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(device)
# #         translated = model.generate(**batch)
# #         tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# #         assert (
# #             tgt_text[0]
# #             == "California's..."
# #         )
# #         '''
# #     )

# #     example_1 = textwrap.dedent(
# #         """
# #         # AutomataAgentConfig

# #         `AutomataAgentConfig` is a configuration class that helps configure, setup, and interact with an `AutomataAgent`. It contains various attributes such as `config_name`, `instruction_payload`, `llm_toolkits`, and others to provide the necessary setup and settings to be used by the agent.

# #         ## Overview

# #         `AutomataAgentConfig` provides a way to load the agent configurations specified by the `AgentConfigName`. The configuration options can be set during the instantiation of the class or can be loaded using the `load` classmethod. It provides utility methods to load and setup agent configurations while also validating the provided settings. The class offers a convenient way to create an agent with custom configurations and includes closely related symbols like `AgentConfigName`.

# #         ## Related Symbols

# #         - `configs.config_enums.AgentConfigName`
# #         - `automata_docs.core.agent.automata_agent.AutomataAgent`
# #         - `configs.automata_agent_config_utils.AutomataAgentConfigBuilder`
# #         - `automata_docs.core.coordinator.automata_instance.AutomataInstance`

# #         ## Example

# #         The following is an example demonstrating how to create an instance of `AutomataAgentConfig` using a predefined configuration name.

# #         ```python
# #         from configs.automata_agent_configs import AutomataAgentConfig
# #         from configs.config_enums import AgentConfigName

# #         config_name = AgentConfigName.AUTOMATA_MAIN_DEV
# #         config = AutomataAgentConfig.load(config_name)
# #         ```

# #         ## Limitations

# #         The primary limitation of `AutomataAgentConfig` is that it relies on the predefined configuration files based on `AgentConfigName`. It can only load configurations from those files and cannot load custom configuration files. In addition, it assumes a specific directory structure for the configuration files.

# #         ## Follow-up Questions:

# #         - How can we include custom configuration files for loading into the `AutomataAgentConfig` class?

# #         """
# #     )

# #     completion = openai.ChatCompletion.create(
# #         model="gpt-4",
# #         messages=[
# #             {
# #                 "role": "user",
# #                 "content": f"Generate the documentation for {selected_symbol.dotpath} using the context shown below -\n {symbol_overview}."
# #                 f" The output documentation should include an overview section, related symbols, examples, and discussion around limitations."
# #                 f" Examples should be comprehensive and readily executable (e.g. correct imports and values)."
# #                 f" If there are references to 'Mock' objects in test files from your context, do your best to replace these with the actual underlying object."
# #                 f" If that is not possible, note this in a footnote. Mock objects are used in testing to simplify working with complex objects."
# #                 f" For reference, write in the style of in the original Python Library documentation -\n{example_0}"
# #                 f" For further reference, see the local documentation here -\n{example_1}"
# #                 f" Some information is just included for contextual reference, and this may be omitted from the output documentation."
# #                 f" Lastly, if some points are unclear, note these in a footnote that begins with ## Follow-up Questions:",
# #             }
# #         ],
# #     )
# #     if not completion.choices:
# #         return "Error: No completion found"
# #     return completion.choices[0]["message"]["content"]


# # def get_summary_doc(input_doc: str) -> str:
# #     completion = openai.ChatCompletion.create(
# #         model="gpt-4",
# #         messages=[
# #             {
# #                 "role": "user",
# #                 "content": f"Condense the documentation below down to one to two concise paragraphs:\n {input_doc}\nIf there is an example, include that in full in the output.",
# #             }
# #         ],
# #     )
# #     if not completion.choices:
# #         return "Error: No completion found"
# #     return completion.choices[0]["message"]["content"]


# def main(*args, **kwargs):
#     docs = load_docs(kwargs)

#     graph = SymbolGraphFactory().create(build_caller_relationships=True)
#     config = SymbolRankConfig()
#     subgraph = graph.get_rankable_symbol_subgraph(
#         flow_rank=kwargs.get("rank_direction", "bidirectional")
#     )
#     ranker = SymbolRankFactory().create(subgraph, config)
#     symbol_searcher = SymbolSearcherFactory().create()
#     selected_symbols = get_filtered_ranked_symbols(kwargs, ranker)

#     desc_to_full_symbol = {
#         ".".join([desc.name for desc in symbol.descriptors]): symbol for symbol in docs.keys()
#     }

#     for selected_symbol in selected_symbols:
#         raw_code = convert_to_fst_object(selected_symbol).dumps()
#         symbol_desc_identifier = ".".join([desc.name for desc in selected_symbol.descriptors])
#         map_symbol = desc_to_full_symbol.get(symbol_desc_identifier, None)

#         if (
#             not map_symbol
#             or (map_symbol and docs[map_symbol][0] != raw_code)
#             or kwargs.get("hard_refresh")
#         ):
#             print(f"Generating docs for {selected_symbol}")
#             abbreviated_selected_symbol = selected_symbol.uri.split("/")[1].split("#")[0]

#             # Splice the search results for the symbol with the symbol biased on tests
#             search_results_0 = symbol_searcher.symbol_rank_search(f"{abbreviated_selected_symbol}")
#             search_results_1 = symbol_searcher.symbol_rank_search(
#                 f"{abbreviated_selected_symbol} tests or conftest"
#             )

#             search_list = []
#             for i in range(len(search_results_0)):
#                 set_list = set(search_list)
#                 if search_results_0[i] not in set_list:
#                     search_list.append(search_results_0[i][0])
#                 elif search_results_1[i] not in set_list:
#                     search_list.append(search_results_1[i][0])

#             printer = PythonContextRetriever(graph)
#             printer.process_symbol(selected_symbol, search_list)
#             symbol_overview = printer.message
#             # completion = get_full_doc_completion(selected_symbol, symbol_overview)
#             # completion_summary = get_summary_doc(completion)
#             # docs[selected_symbol] = (
#             #     raw_code,
#             #     symbol_overview,
#             #     completion,
#             #     completion_summary,
#             # )
#             # # Save after each iteration to lock in progress (saving is short compared to generating completion)
#             # save_docs(kwargs, docs)

#         elif map_symbol and docs[map_symbol][0] == raw_code and map_symbol != selected_symbol:
#             print(f"Updating symbol for {selected_symbol}")
#             # docs[selected_symbol] = docs[map_symbol]
#             # del docs[map_symbol]
#             # save_docs(kwargs, docs)

#         elif map_symbol and docs[map_symbol][0] == raw_code:
#             print(f"Continuing on {selected_symbol}")

#         else:
#             print(f"Symbol {selected_symbol} skipped.")
