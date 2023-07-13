import pytest

from automata.symbol import Symbol, SymbolDescriptor, parse_symbol


@pytest.fixture
def parsed_symbol():
    return parse_symbol(
        "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#description."
    )


# Test to ensure that a symbol is parsed correctly
def test_parse_symbol(parsed_symbol):
    assert isinstance(parsed_symbol, Symbol)
    assert parsed_symbol.package.manager == "python"
    assert parsed_symbol.package.name == "automata"
    assert parsed_symbol.package.version == "v0.0.0"
    assert parsed_symbol.module_path == "config.automata_agent_config"
    assert (
        parsed_symbol.full_dotpath
        == "config.automata_agent_config.AutomataAgentConfig.description"
    )
    assert parsed_symbol.descriptors[-1].name == "description"
    assert parsed_symbol.parent().descriptors[-1].name == "AutomataAgentConfig"


# Test that symbols with different descriptors are parsed correctly
@pytest.mark.parametrize(
    "symbol_str, expected_descriptor",
    [
        (
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#load().(config_name)",
            SymbolDescriptor.PyKind.Parameter,
        ),
        (
            "scip-python python automata v0.0.0 `core.tasks.automata_task_executor`/logger.",
            SymbolDescriptor.PyKind.Value,
        ),
        (
            "scip-python python automata v0.0.0 `core.agent.automata_agent_enums`/ActionIndicator#CODE.",
            SymbolDescriptor.PyKind.Value,
        ),
        (
            "scip-python python automata v0.0.0 `core.agent.automata_agent_enums`/ActionIndicator#",
            SymbolDescriptor.PyKind.Class,
        ),
        (
            "scip-python python automata v0.0.0 `core.tools.base`/ToolNotFoundError#__init__().",
            SymbolDescriptor.PyKind.Method,
        ),
    ],
)
def test_parse_symbol_descriptor(symbol_str, expected_descriptor):
    symbol = parse_symbol(symbol_str)
    assert (
        SymbolDescriptor.convert_scip_to_python_suffix(
            symbol.descriptors[-1].suffix
        )
        == expected_descriptor
    )


# Test the __str__ method of the Symbol class
def test_symbol_str(parsed_symbol):
    assert (
        str(parsed_symbol)
        == "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#description."
    )


@pytest.mark.parametrize(
    "symbol2, expected",
    [
        (
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#description.",
            True,
        ),
        (
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#load().(config_name)",
            False,
        ),
    ],
)
def test_symbol_equality(parsed_symbol, symbol2, expected):
    assert (parsed_symbol == parse_symbol(symbol2)) == expected


# Test the hash function of Symbol
def test_symbol_hash(parsed_symbol):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#description."
    )
    assert hash(parsed_symbol) == hash(symbol)
