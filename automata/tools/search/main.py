from argparse import ArgumentParser

from automata.tools.search.symbol_graph import SymbolGraph
from automata.tools.search.symbol_parser import parse_uri_to_symbol
from automata.tools.search.symbol_searcher import SymbolSearcher

if __name__ == "__main__":
    symbol_prefix = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065"
    test_path = "automata"  # "automata.configs.automata_agent_configs"
    test_symbol = parse_uri_to_symbol("%s `%s`/AutomataAgentConfig#" % (symbol_prefix, test_path))

    argparse = ArgumentParser()
    argparse.add_argument("-i", type=str, dest="index", help="path to index file", required=True)
    args = argparse.parse_args()
    symbol_graph = SymbolGraph(args.index)
    symbol_searcher = SymbolSearcher(symbol_graph)

    # Dump all available files in the symbol graph
    print("-" * 200)
    print("Fetching all available files in SymbolGraph")
    file_nodes = symbol_graph.get_all_files()
    for file_node in file_nodes:
        print("File >> %s" % (file_node))
    print("-" * 200)

    # Dump all available symbols at the test path
    print("-" * 200)
    print("Fetching all available symbols along %s" % (test_path))
    available_symbols = symbol_graph.get_symbols_along_path(test_path)
    for symbol in available_symbols:
        print("Available Symbol >> %s" % (symbol))
        # symbol_type = symbol_graph.helper.find_symbol_type(symbol)
        # print("Symbol Type >> %s" % (symbol_type))
        # print("Symbol Type == class >> %s" % (symbol_type == "class"))

    print("-" * 200)

    # Get the context for the test symbol
    print("-" * 200)
    print("Dumping symbol context for %s" % (test_symbol))
    print(symbol_graph.get_symbol_context(test_symbol))
    print("-" * 200)

    # Find references of the test symbol
    print("-" * 200)
    print("Searching for references of the symbol %s" % (test_symbol))
    search_result = symbol_searcher.process_query("type:symbol %s" % (test_symbol.uri))
    print("References: ", search_result)
    print("-" * 200)

    # Find source code for the test symbol
    print("-" * 200)
    print("Searching for source code for symbol %s" % (test_symbol))
    search_result = symbol_searcher.process_query("type:source %s" % (test_symbol.uri))
    print("Source Code: ", search_result)
    print("-" * 200)

    # Find exact matches for abbrievated test symbol
    print("-" * 200)
    abbv_test_symbol = "AutomataAgentConfig"
    print("Searching for exact matches of the filter %s" % (abbv_test_symbol))
    search_result = symbol_searcher.process_query("type:exact %s" % (abbv_test_symbol))
    print("Search result: ", search_result)
    print("-" * 200)

    # Perform a find and replace on the test find symbol below
    print("-" * 200)
    test_find = "AutomataAgentConfigFactory"
    test_replace = "__Automata__Agent__Config__Factory__"
    print("Performing find on %s and replacing with %s" % (test_find, test_replace))
    do_write = False
    counts = symbol_searcher.process_query(
        "type:replace %s %s %s" % (test_find, test_replace, do_write)
    )
    print("In Mem Replacements: ", counts)
    print("-" * 200)

    # Perform a find and replace on the test find symbol below
    print("-" * 200)
    method_symbol = parse_uri_to_symbol(
        "%s `automata.configs.automata_agent_config_utils`/AutomataAgentConfigBuilder#build()."
        % (symbol_prefix)
    )
    print("Finding return type for %s" % (method_symbol))
    print("Return Symbol >> ", symbol_graph.find_return_symbol(method_symbol))
    print("-" * 200)

    # Get the callers of the test symbol
    print("-" * 200)
    print("Finding Callers for %s" % (test_symbol))
    callers = symbol_graph.get_callers(test_symbol)
    for caller in callers:
        print("Caller >> ", caller)
    print("-" * 200)
