import logging
import os
import textwrap

from tqdm import tqdm

from automata.configs.config_enums import ConfigCategory
from automata.core.search.symbol_graph import SymbolGraph
from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
from automata.core.search.symbol_utils import get_rankable_symbols
from automata.core.utils import config_path

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the distance embedding based on the symbols present in the system.
    """
    scip_path = os.path.join(config_path(), ConfigCategory.SYMBOLS.value, "index.scip")
    embedding_path = os.path.join(
        config_path(), ConfigCategory.SYMBOLS.value, "symbol_embedding.json"
    )

    symbol_graph = SymbolGraph(scip_path)

    if kwargs.get("update_embedding_map"):
        all_defined_symbols = symbol_graph.get_all_defined_symbols()
        filtered_symbols = get_rankable_symbols(all_defined_symbols)
        chunks = [
            filtered_symbols[i : i + CHUNK_SIZE]
            for i in range(0, len(filtered_symbols), CHUNK_SIZE)
        ]

        for chunk in tqdm(chunks):
            if kwargs.get("build_new_embedding_map") and chunk == chunks[0]:
                symbol_embedding = SymbolEmbeddingMap(
                    all_defined_symbols=chunk,
                    build_new_embedding_map=True,
                    embedding_path=embedding_path,
                )
            else:
                symbol_embedding = SymbolEmbeddingMap(
                    load_embedding_map=True,
                    embedding_path=embedding_path,
                )
                symbol_embedding.update_embeddings(chunk)

            symbol_embedding.save(embedding_path, overwrite=True)
        return "Success"

    elif kwargs.get("query_embedding"):
        symbol_graph = SymbolGraph(scip_path)
        symbol_embedding = SymbolEmbeddingMap(
            load_embedding_map=True,
            embedding_path=embedding_path,
        )
        symbol_similarity = SymbolSimilarity(symbol_embedding)

        result_symbols = symbol_similarity.get_nearest_symbols_for_query(
            kwargs["query_text"], 10, norm_type=kwargs.get("norm_type", "l2")
        )
        print("-" * 100)
        print(">> Result symbols << ")
        print("-" * 100)
        for symbol in result_symbols:
            print("  >> %s (similarity = %s) << " % (symbol, result_symbols[symbol]))
        print("-" * 100)
        return "Success"


if __name__ == "__main__":
    # Setup argument parser
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Update the distance embedding based on the symbols present in the system."
    )

    # Add the arguments
    parser.add_argument(
        "--update_embedding_map", action="store_true", help="Flag to update the embedding map."
    )

    parser.add_argument(
        "--build_new_embedding_map", action="store_true", help="Flag to build a new embedding map."
    )

    parser.add_argument("--query_embedding", action="store_true", help="Query the embedding map.")

    sample_query_text = textwrap.dedent(
        '''
        def _parse_completion_message(self, completion_message: str) -> str:
            """
            Parses the completion message and replaces placeholders with actual tool outputs.

            Args:
                completion_message (str): The completion message with placeholders.

            Returns:
                str: The parsed completion message with placeholders replaced by tool outputs.
            """
            outputs = {}
            for message in self.messages:
                pattern = r"-\s(tool_output_\d+)\s+-\s(.*?)(?=-\s(tool_output_\d+)|$)"
                matches = re.finditer(pattern, message.content, re.DOTALL)
                for match in matches:
                    tool_name, tool_output = match.group(1), match.group(2).strip()
                    outputs[tool_name] = tool_output
            if self._has_helper_agents():
                for message in self.messages:
                    pattern = r"-\s(agent_output_\d+)\s+-\s(.*?)(?=-\s(agent_output_\d+)|$)"
                    matches = re.finditer(pattern, message.content, re.DOTALL)
                    for match in matches:
                        agent_version, agent_output = match.group(1), match.group(2).strip()
                        outputs[agent_version] = agent_output

                for output_name in outputs:
                    completion_message = completion_message.replace(
                        f"{{{output_name}}}", outputs[output_name]
                    )

            for output_name in outputs:
                completion_message = completion_message.replace(
                    f"{{{output_name}}}", outputs[output_name]
                )
            return completion_message
        '''
    )  # noqa
    parser.add_argument(
        "--query_text", default=sample_query_text, help="Text to query the embedding map for."
    )
    parser.add_argument("--norm_type", default="l2", help="Query the embedding map.")

    # Parse the arguments
    args = parser.parse_args()

    if args.query_embedding and args.build_new_embedding_map:
        raise ValueError(
            "Cannot build a new embedding map and query the embedding map at the same time."
        )

    # Call the main function with parsed arguments
    result = main(**vars(args))
    print("Result = ", result)
