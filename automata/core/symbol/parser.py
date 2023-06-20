import re
from typing import List, Optional

from automata.core.symbol.symbol_types import Symbol, SymbolDescriptor, SymbolPackage

"""
SCIP produces symbol URI, it identifies a class, method, or a local variable, along with the entire AST path to it.
Full spec: https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/docs/scip.md#symbol
The classes and functions in this file are used to convert the symbol URI into a human-readable form that can be used to query the index.
"""


class SymbolParser:
    """
    Translation of the logic defined in
    https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/bindings/go/scip/symbol.go
    to parse URIs into structured objects.
    It's not great that this implementation is not in hard sync with the Go one, but it's good enough for now.
    """

    def __init__(self, symbol: str) -> None:
        """
        Args:
            symbol (str): The symbol URI to parse
        """
        self.symbol = symbol
        self.index = 0
        self.symbol_str = symbol

    def error(self, message: str) -> ValueError:
        """
        Create a ValueError with the symbol and a pointer to the error location

        Args:
            message (str): The error message
        """
        return ValueError(f"{message}\n{self.symbol_str}\n{'_' * self.index}^")

    def current(self) -> str:
        """
        Get the current character in the symbol

        Returns:
            str - The current character in the symbol
        """
        return self.symbol[self.index]

    def peek_next(self) -> Optional[str]:
        """
        Peek at the next character in the symbol

        Returns:
            Optional[str] - The next character in the symbol,
                or None if there is no next character
        """
        if self.index + 1 < len(self.symbol):
            return self.symbol[self.index + 1]
        return None

    def parse_descriptors(self) -> List[SymbolDescriptor]:
        """
        Parse all descriptors in the symbol

        Returns:
            List[SymbolDescriptor] - The descriptors in the symbol
        """
        result = []
        while self.index < len(self.symbol):
            descriptor = self.parse_descriptor()
            result.append(descriptor)
        return result

    def parse_descriptor(self) -> SymbolDescriptor:
        """
        Parse a single descriptor in the symbol

        Returns:
            SymbolDescriptor - The descriptor in the symbol
        """
        next_char = self.current()
        if next_char == "(":
            self.index += 1
            name = self.accept_identifier("parameter name")
            descriptor = SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Parameter)
            self.accept_character(")", "closing parameter name")
            return descriptor
        elif next_char == "[":
            self.index += 1
            name = self.accept_identifier("type parameter name")
            descriptor = SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.TypeParameter)
            self.accept_character("]", "closing type parameter name")
            return descriptor
        else:
            name = self.accept_identifier("descriptor name")
            suffix = self.current()
            self.index += 1
            if suffix == "(":
                disambiguator = ""
                if self.current() != ")":
                    disambiguator = self.accept_identifier("method disambiguator")
                descriptor = SymbolDescriptor(
                    name, SymbolDescriptor.ScipSuffix.Method, disambiguator
                )
                self.accept_character(")", "closing method")
                self.accept_character(".", "closing method")
                return descriptor
            elif suffix == "/":
                return SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Namespace)
            elif suffix == ".":
                return SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Term)
            elif suffix == "#":
                return SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Type)
            elif suffix == ":":
                return SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Meta)
            elif suffix == "!":
                return SymbolDescriptor(name, SymbolDescriptor.ScipSuffix.Macro)
            else:
                raise self.error("Expected a descriptor suffix")

    def accept_identifier(self, what: str) -> str:
        """
        Accepts an identifier from the symbol

        Args:
            what (str): The name of the identifier

        Returns:
            str - The identifier
        """
        if self.current() == "`":
            self.index += 1
            return self.accept_backtick_escaped_identifier(what)
        start = self.index
        while self.index < len(self.symbol) and self.is_identifier_character(self.current()):
            self.index += 1
        if start == self.index:
            raise self.error("empty identifier: " + what)
        return self.symbol[start : self.index]

    def accept_space_escaped_identifier(self, what: str) -> str:
        """
        Accepts an identifier from the symbol, where the identifier is escaped by spaces

        Args:
            what (str): The name of the identifier

        Returns:
            str - The identifier
        """
        return self.accept_escaped_identifier(what, " ")

    def accept_backtick_escaped_identifier(self, what: str) -> str:
        """
        Accepts an identifier from the symbol,
            where the identifier is escaped by backticks

        Args:
            what (str): The name of the identifier

        Returns:
            str - The identifier
        """
        return self.accept_escaped_identifier(what, "`")

    def accept_escaped_identifier(self, what: str, escape_character: str) -> str:
        """
        Accepts an identifier from the symbol,
            where the identifier is escaped by a given character

        Args:
            what (str): The name of the identifier

        Returns:
            str - The identifier
        """
        builder = []
        while self.index < len(self.symbol):
            ch = self.current()
            if ch == escape_character:
                self.index += 1
                if self.index >= len(self.symbol):
                    break
                if self.current() == escape_character:
                    builder.append(ch)
                else:
                    return "".join(builder)
            else:
                builder.append(ch)
            self.index += 1
        raise self.error(
            f"reached end of symbol while parsing <{what}>, expected a '{escape_character}' character"
        )

    def accept_character(self, r: str, what: str):
        """
        Accepts a character from the symbol

        Args:
            r (str): The character to accept
            what (str): The name of the character
        """
        if self.current() == r:
            self.index += 1
        else:
            raise self.error(f"expected '{r}', obtained '{self.current()}', while parsing {what}")

    @staticmethod
    def is_identifier_character(c: str) -> bool:
        """
        Checks if a character is a valid identifier character

        Args:
            c (str): The character to check

        """
        return c.isalpha() or c.isdigit() or c in ["-", "+", "$", "_"]


def parse_symbol(symbol_uri: str, include_descriptors: bool = True) -> Symbol:
    """
    Parses a symbol from a URI

    Args:
        symbol_uri (str): The URI of the symbol
        include_descriptors (bool): Whether to include descriptors in the symbol

    Returns:
        Symbol - The parsed symbol
    """
    s = SymbolParser(symbol_uri)
    scheme = s.accept_space_escaped_identifier("scheme")

    if scheme == "local":
        return new_local_symbol(symbol_uri, s.symbol[s.index :])
    manager = s.accept_space_escaped_identifier("package manager")

    manager = "" if manager == "." else manager
    package_name = s.accept_space_escaped_identifier("package name")

    package_name = "" if package_name == "." else package_name
    package_version = s.accept_space_escaped_identifier("package version")

    package_version = "" if package_version == "." else package_version
    descriptors = []
    if include_descriptors:
        descriptors = s.parse_descriptors()
    return Symbol(
        symbol_uri,
        scheme,
        SymbolPackage(manager, package_name, package_version),
        tuple(descriptors),
    )


def new_local_symbol(symbol: str, id: str) -> Symbol:
    """
    Creates a new local symbol

    Args:
        symbol (str): The symbol URI
        id (str): The id of the symbol
    TODO: this doesn't work yet (?)
    """
    return Symbol(
        symbol,
        "local",
        SymbolPackage("", "", ""),
        tuple([SymbolDescriptor(id, SymbolDescriptor.ScipSuffix.Local)]),
    )


def is_global_symbol(symbol: str) -> bool:
    """
    Checks if a symbol is a global symbol

    Args:
        symbol (str): The symbol URI

    Returns:
        bool - Whether the symbol is a global symbol
    """
    return not is_local_symbol(symbol)


def is_local_symbol(symbol: str) -> bool:
    """
    Checks if a symbol is a local symbol

    Args:
        symbol (str): The symbol URI

    Returns:
        bool - Whether the symbol is a local symbol
    """
    return symbol.startswith("local ")


def get_escaped_name(name: str) -> str:
    """
    Gets the escaped name of a symbol

    Args:
        name (str): The name of the symbol

    Returns:
        str - The escaped name of the symbol
    """
    if not name:
        return ""
    if is_simple_identifier(name):
        return name
    return "`" + re.sub("`", "``", name) + "`"


def is_simple_identifier(name: str) -> bool:
    """
    Checks if a name is a simple identifier

    Args:
        name (str): The name to check

    Returns:
        bool - Whether the name is a simple identifier
    """
    return re.match(r"^[\w$+-]+$", name) is not None
