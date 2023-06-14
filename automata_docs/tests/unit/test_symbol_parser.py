from automata_docs.core.symbol.parser import Symbol, is_global_symbol, is_local_symbol


def test_parse_symbol(symbols):
    for symbol in symbols:
        assert symbol.scheme == "scip-python"
        assert symbol.package.manager == "python"
        assert symbol.package.name == "automata_docs"
        assert symbol.package.version == "75482692a6fe30c72db516201a6f47d9fb4af065"
        assert len(symbol.descriptors) > 0


def test_is_global_symbol(symbols):
    for symbol in symbols:
        assert is_global_symbol(symbol.uri)


def test_is_local_symbol(symbols):
    for symbol in symbols:
        assert is_local_symbol("local " + symbol.uri)


def _unparse(symbol: Symbol):
    """Converts back into URI string"""
    return f"{symbol.scheme} {symbol.package.unparse()} {''.join([descriptor.unparse() for descriptor in symbol.descriptors])}"


def test_unparse_symbol(symbols):
    for symbol in symbols:
        assert _unparse(symbol) == symbol.uri
