import pytest

from automata.tools.search.symbol_parser import (
    Descriptor,
    Package,
    Symbol,
    SymbolParser,
    get_escaped_name,
    is_global_symbol,
    is_local_symbol,
    parse_symbol,
)


def test_parse_symbol():
    symbol_uri = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.python_tools.tests.test_python_writer`/test_create_function_source_function()"
    parsed_symbol = parse_symbol(symbol_uri)

    assert parsed_symbol.scheme == "scip-python"
    assert parsed_symbol.package.manager == "python"
    assert parsed_symbol.package.name == "automata"
    assert parsed_symbol.package.version == "75482692a6fe30c72db516201a6f47d9fb4af065"
    assert len(parsed_symbol.descriptors) > 0


def test_is_global_symbol():
    symbol_uri = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.python_tools.tests.test_python_writer`/test_create_function_source_function()"
    assert is_global_symbol(symbol_uri)


def test_is_local_symbol():
    symbol_uri = "local scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.python_tools.tests.test_python_writer`/test_create_function_source_function()"
    assert is_local_symbol(symbol_uri)


def test_get_escaped_name():
    name = "test_create_function_source_function"
    escaped_name = get_escaped_name(name)
    assert escaped_name == name


def test_descriptor_unparse():
    descriptor = Descriptor("descriptor_name", Descriptor.ScipSuffix.Term)
    unparsed = descriptor.unparse()
    assert unparsed == "descriptor_name."


def test_package_unparse():
    package = Package("python", "automata", "75482692a6fe30c72db516201a6f47d9fb4af065")
    unparsed = package.unparse()
    assert unparsed == "python automata 75482692a6fe30c72db516201a6f47d9fb4af065"


def test_symbol_unparse():
    symbol = Symbol(
        "symbol_uri",
        "scheme",
        Package("manager", "package_name", "package_version"),
        [Descriptor("descriptor_name", Descriptor.ScipSuffix.Term)],
    )
    unparsed = symbol.unparse()
    assert unparsed == "symbol_uri"
