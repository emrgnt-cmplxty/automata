import argparse
import logging
import textwrap
from typing import Any, Dict

import openai
from cli.cli_utils import load_docs, save_docs

from automata_docs.core.context.python_context.python_context_retriever import (
    PythonContextRetriever,
)
from automata_docs.core.search.symbol_factory import (
    SymbolGraphFactory,
    SymbolRankFactory,
    SymbolSearcherFactory,
)
from automata_docs.core.search.symbol_rank.symbol_rank import SymbolRank, SymbolRankConfig
from automata_docs.core.search.symbol_utils import convert_to_fst_object
from automata_docs.core.symbol.symbol_types import Symbol, SymbolDescriptor
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


def get_filtered_ranked_symbols(kwargs: Dict[str, Any], ranker: SymbolRank):
    selected_symbols = []
    selection_filters = kwargs.get("selection_filters", "").split(",")
    for symbol, _rank in ranker.get_ranks():
        if symbol.symbol_kind_by_suffix() != SymbolDescriptor.PythonKinds.Class:
            continue
        if any(filter_ in symbol.uri for filter_ in selection_filters):
            selected_symbols.append(symbol)
            if len(set(selected_symbols)) >= kwargs.get("top_n_symbols", 0):
                break

    return selected_symbols


def get_full_doc_completion(selected_symbol: Symbol, symbol_overview: str) -> str:
    example_0 = textwrap.dedent(
        '''
        ...
        ## Usage Example

        ```python
        from transformers import PegasusForConditionalGeneration, PegasusTokenizer
        import torch

        src_text = [
            """ PG&E .... """
        ]

        model_name = "google/pegasus-xsum"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = PegasusTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
        batch = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(device)
        translated = model.generate(**batch)
        tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        assert (
            tgt_text[0]
            == "California's..."
        )
        '''
    )

    example_1 = textwrap.dedent(
        """
        # AutomataAgentConfig

        `AutomataAgentConfig` is a configuration class that helps configure, setup, and interact with an `AutomataAgent`. It contains various attributes such as `config_name`, `instruction_payload`, `llm_toolkits`, and others to provide the necessary setup and settings to be used by the agent.

        ## Overview

        `AutomataAgentConfig` provides a way to load the agent configurations specified by the `AgentConfigName`. The configuration options can be set during the instantiation of the class or can be loaded using the `load` classmethod. It provides utility methods to load and setup agent configurations while also validating the provided settings. The class offers a convenient way to create an agent with custom configurations and includes closely related symbols like `AgentConfigName`.

        ## Related Symbols

        - `configs.config_enums.AgentConfigName`
        - `automata_docs.core.agent.automata_agent.AutomataAgent`
        - `configs.automata_agent_config_utils.AutomataAgentConfigBuilder`
        - `automata_docs.core.coordinator.automata_instance.AutomataInstance`

        ## Example

        The following is an example demonstrating how to create an instance of `AutomataAgentConfig` using a predefined configuration name.

        ```python
        from configs.automata_agent_configs import AutomataAgentConfig
        from configs.config_enums import AgentConfigName

        config_name = AgentConfigName.AUTOMATA_MAIN_DEV
        config = AutomataAgentConfig.load(config_name)
        ```

        ## Limitations

        The primary limitation of `AutomataAgentConfig` is that it relies on the predefined configuration files based on `AgentConfigName`. It can only load configurations from those files and cannot load custom configuration files. In addition, it assumes a specific directory structure for the configuration files.

        ## Follow-up Questions:

        - How can we include custom configuration files for loading into the `AutomataAgentConfig` class?
        
        """
    )

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"Generate the documentation for {selected_symbol.path} using the context shown below -\n {symbol_overview}."
                f" The output documentation should include an overview section, related symbols, examples, and discussion around limitations."
                f" Examples should be comprehensive and readily executable (e.g. correct imports and values)."
                f" If there are references to 'Mock' objects in test files from your context, do your best to replace these with the actual underlying object."
                f" If that is not possible, note this in a footnote. Mock objects are used in testing to simplify working with complex objects."
                f" For reference, write in the style of in the original Python Library documentation -\n{example_0}"
                f" For further reference, see the local documentation here -\n{example_1}"
                f" Some information is just included for contextual reference, and this may be omitted from the output documentation."
                f" Lastly, if some points are unclear, note these in a footnote that begins with ## Follow-up Questions:",
            }
        ],
    )
    if not completion.choices:
        return "Error: No completion found"
    return completion.choices[0]["message"]["content"]


def get_summary_doc(input_doc: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"Condense the documentation below down to one to two concise paragraphs:\n {input_doc}\nIf there is an example, include that in full in the output.",
            }
        ],
    )
    if not completion.choices:
        return "Error: No completion found"
    return completion.choices[0]["message"]["content"]


def main(*args, **kwargs):
    docs = load_docs(kwargs)

    graph = SymbolGraphFactory().create(build_caller_relationships=True)
    config = SymbolRankConfig()
    subgraph = graph.get_rankable_symbol_subgraph(
        flow_rank=kwargs.get("rank_direction", "bidirectional")
    )
    ranker = SymbolRankFactory().create(subgraph, config)
    symbol_searcher = SymbolSearcherFactory().create()
    selected_symbols = get_filtered_ranked_symbols(kwargs, ranker)

    desc_to_full_symbol = {
        ".".join([desc.name for desc in symbol.descriptors]): symbol for symbol in docs.keys()
    }

    for selected_symbol in selected_symbols:
        raw_code = convert_to_fst_object(selected_symbol).dumps()
        symbol_desc_identifier = ".".join([desc.name for desc in selected_symbol.descriptors])
        map_symbol = desc_to_full_symbol.get(symbol_desc_identifier, None)

        if (
            not map_symbol
            or (map_symbol and docs[map_symbol][0] != raw_code)
            or kwargs.get("hard_refresh")
        ):
            print(f"Generating docs for {selected_symbol}")
            abbreviated_selected_symbol = selected_symbol.uri.split("/")[1].split("#")[0]

            # Splice the search results for the symbol with the symbol biased on tests
            search_results_0 = symbol_searcher.symbol_rank_search(f"{abbreviated_selected_symbol}")
            search_results_1 = symbol_searcher.symbol_rank_search(
                f"{abbreviated_selected_symbol} tests or conftest"
            )

            search_list = []
            for i in range(len(search_results_0)):
                set_list = set(search_list)
                if search_results_0[i] not in set_list:
                    search_list.append(search_results_0[i][0])
                elif search_results_1[i] not in set_list:
                    search_list.append(search_results_1[i][0])

            printer = PythonContextRetriever(graph)
            printer.process_symbol(selected_symbol, search_list)
            symbol_overview = printer.message
            completion = get_full_doc_completion(selected_symbol, symbol_overview)
            completion_summary = get_summary_doc(completion)
            docs[selected_symbol] = (
                raw_code,
                symbol_overview,
                completion,
                completion_summary,
            )
            # Save after each iteration to lock in progress (saving is short compared to generating completion)
            save_docs(kwargs, docs)

        elif map_symbol and docs[map_symbol][0] == raw_code and map_symbol != selected_symbol:
            print(f"Updating symbol for {selected_symbol}")
            docs[selected_symbol] = docs[map_symbol]
            del docs[map_symbol]

        elif map_symbol and docs[map_symbol][0] == raw_code:
            print(f"Continuing on {selected_symbol}")

        else:
            print(f"Symbol {selected_symbol} skipped.")


if __name__ == "__main__":
    openai.api_key = OPENAI_API_KEY

    # Function for argument parsing
    def parse_args():
        parser = argparse.ArgumentParser(
            description="Update documentation based on local code changes."
        )
        parser.add_argument("-i", "--input", help="The path to the file that needs documentation.")
        parser.add_argument(
            "-s",
            "--selection_filters",
            default="Automata,Symbol",
            help="Selection criteria for symbols.",
        )
        parser.add_argument(
            "-n",
            "--top_n_symbols",
            type=int,
            default=5,
            help="Number of top symbols to select.",
        )
        parser.add_argument(
            "-u", "--update_docs", action="store_true", help="Flag to update the docs."
        )
        parser.add_argument(
            "-r",
            "--hard_refresh",
            action="store_true",
            help="Should we re-run files with no code-diff?",
        )
        parser.add_argument(
            "-documentation_path",
            default="symbol_documentation.json",
            help="Selection criteria for symbols.",
        )
        parser.add_argument(
            "-rank_direction",
            default="bidirectional",
            help="Selection criteria for symbols.",
        )
        return parser.parse_args()

    # Parse the arguments
    args = parse_args()

    # Call the main function with parsed arguments
    result = main(**vars(args))
    print("Result = ", result)
