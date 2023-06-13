import os

import pytest

from automata_docs.core.symbol.symbol_graph import SymbolGraph
from automata_docs.core.symbol.symbol_parser import parse_symbol


@pytest.fixture
def symbols():
    symbols = [
        # Symbol with a simple attribute
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `configs.automata_agent_configs`/AutomataAgentConfig#description."
        ),
        # Symbol with a method with foreign argument
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `configs.automata_agent_configs`/AutomataAgentConfig#load().(config_name)"
        ),
        # Symbol with a class method, self as argument
        # parse_symbol(
        #     "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `tools.python_tools.python_ast_indexer`/PythonASTIndexer#get_module_path().(self)"
        # ),
        # Symbol with a locally defined object
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `core.tasks.automata_task_executor`/logger."
        ),
        # Symbol with a class object and class variable
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `configs.automata_agent_configs`/AutomataAgentConfig#verbose."
        ),
        # Symbol with a function in a module
        # parse_symbol("scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `core.coordinator.tests.test_automata_coordinator`/test().(coordinator)"),
        # Symbol with a class method
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `evals.eval_helpers`/EvalAction#__init__().(action)"
        ),
        # Symbol with an object
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `core.agent.automata_agent_enums`/ActionIndicator#CODE."
        ),
        # Class Name
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `core.agent.automata_agent_enums`/ActionIndicator#"
        ),
        # Init
        parse_symbol(
            "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `core.base.tool`/ToolNotFoundError#__init__()."
        ),
    ]

    return symbols


@pytest.fixture
def symbol_graph():
    # assuming the path to a valid index protobuf file, you should replace it with your own file path
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "index.scip")
    graph = SymbolGraph(index_path)
    return graph


@pytest.fixture
def symbol_graph_mock(mocker):
    mock = mocker.MagicMock(spec=SymbolGraph)
    return mock
