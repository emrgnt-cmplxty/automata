import abc
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple

import numpy as np

from automata.core.symbol.scip_pb2 import Descriptor as DescriptorProto  # type: ignore


class SymbolDescriptor:
    """A class to represent the description component of a Symbol URI."""

    ScipSuffix = DescriptorProto

    class PyKind(Enum):
        Local = "local"
        Module = "module"
        Class = "class"
        Method = "method"
        Value = "value"
        Meta = "meta"
        Macro = "macro"
        Parameter = "parameter"
        TypeParameter = "type_parameter"

    def __init__(
        self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None
    ) -> None:
        self.name = name
        self.suffix = suffix
        self.disambiguator = disambiguator

    def __repr__(self) -> str:
        return f"Descriptor({self.name}, {self.suffix}" + (
            f", {self.disambiguator})" if self.disambiguator else ")"
        )

    def unparse(self) -> str:
        """Converts back into URI string"""
        escaped_name = SymbolDescriptor.get_escaped_name(self.name)
        if self.suffix == SymbolDescriptor.ScipSuffix.Namespace:
            return f"{escaped_name}/"
        elif self.suffix == SymbolDescriptor.ScipSuffix.Type:
            return f"{escaped_name}#"
        elif self.suffix == SymbolDescriptor.ScipSuffix.Term:
            return f"{escaped_name}."
        elif self.suffix == SymbolDescriptor.ScipSuffix.Meta:
            return f"{escaped_name}:"
        elif self.suffix == SymbolDescriptor.ScipSuffix.Method:
            return f"{escaped_name}({self.disambiguator})."
        elif self.suffix == SymbolDescriptor.ScipSuffix.Parameter:
            return f"({escaped_name})"
        elif self.suffix == SymbolDescriptor.ScipSuffix.TypeParameter:
            return f"[{escaped_name}]"
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.suffix}")

    @staticmethod
    def get_escaped_name(name) -> str:
        def is_simple_identifier(name):
            return re.match(r"^[\w$+-]+$", name) is not None

        if not name:
            return ""
        if is_simple_identifier(name):
            return name
        return "`" + re.sub("`", "``", name) + "`"

    @staticmethod
    def convert_scip_to_python_suffix(
        descriptor_suffix: DescriptorProto,
    ) -> PyKind:
        if descriptor_suffix == SymbolDescriptor.ScipSuffix.Local:
            return SymbolDescriptor.PyKind.Local

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Namespace:
            return SymbolDescriptor.PyKind.Module

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Type:
            return SymbolDescriptor.PyKind.Class

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Method:
            return SymbolDescriptor.PyKind.Method

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Term:
            return SymbolDescriptor.PyKind.Value

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Macro:
            return SymbolDescriptor.PyKind.Macro

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.Parameter:
            return SymbolDescriptor.PyKind.Parameter

        elif descriptor_suffix == SymbolDescriptor.ScipSuffix.TypeParameter:
            return SymbolDescriptor.PyKind.TypeParameter

        else:
            return SymbolDescriptor.PyKind.Meta


@dataclass
class SymbolPackage:
    """A class to represent the package component of a Symbol URI."""

    manager: str
    name: str
    version: str

    def __repr__(self) -> str:
        return f"Package({self.unparse()})"

    def unparse(self) -> str:
        """Converts back into URI string"""
        return f"{self.manager} {self.name} {self.version}"


@dataclass
class Symbol:
    """
    A class which contains associated logic for a Symbol.

    A Symbol specifies a python class, method, or a local variable.
    A Symbol has a standardized string representation called a URI. The syntax for Symbol is the following:

    # (<x>)+ stands for one or more repetitions of <x>
    <symbol>               ::= <scheme> ' ' <package> ' ' (<descriptor>)+ | 'local ' <local-id>
    <package>              ::= <manager> ' ' <package-name> ' ' <version>
    <scheme>               ::= any UTF-8, escape spaces with double space.
    <manager>              ::= same as above, use the placeholder '.' to indicate an empty value
    <package-name>         ::= same as above
    <version>              ::= same as above
    <descriptor>           ::= <namespace> | <type> | <term> | <method> | <type-parameter> | <parameter> | <meta> | <macro>
    <namespace>            ::= <name> '/'
    <type>                 ::= <name> '#'
    <term>                 ::= <name> '.'
    <meta>                 ::= <name> ':'
    <macro>                ::= <name> '!'
    <method>               ::= <name> '(' <method-disambiguator> ').'
    <type-parameter>       ::= '[' <name> ']'
    <parameter>            ::= '(' <name> ')'
    <name>                 ::= <identifier>
    <method-disambiguator> ::= <simple-identifier>
    <identifier>           ::= <simple-identifier> | <escaped-identifier>
    <simple-identifier>    ::= (<identifier-character>)+
    <identifier-character> ::= '_' | '+' | '-' | '$' | ASCII letter or digit
    <escaped-identifier>   ::= '`' (<escaped-character>)+ '`'
    <escaped-characters>   ::= any UTF-8 character, escape backticks with double backtick.

    Examples -
    from automata.core.symbol.search.symbol_parser import parse_symbol

    symbol_class = parse_symbol(
        "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#"
    )

    symbol_method = parse_symbol(
        "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__()."
    )
    """

    uri: str
    scheme: str
    package: SymbolPackage
    descriptors: Tuple[SymbolDescriptor, ...]

    def __repr__(self) -> str:
        return f"Symbol({self.uri}, {self.scheme}, {self.package}, {self.descriptors})"

    def __hash__(self) -> int:
        return hash(self.uri)

    def __eq__(self, other) -> bool:
        if isinstance(other, Symbol):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other
        return False

    def symbol_kind_by_suffix(self) -> SymbolDescriptor.PyKind:
        """Converts the suffix of the URI into a PyKind."""
        return SymbolDescriptor.convert_scip_to_python_suffix(self.symbol_raw_kind_by_suffix())

    def symbol_raw_kind_by_suffix(self) -> DescriptorProto:
        """Converts the suffix of the URI into a DescriptorProto."""
        if self.uri.startswith("local"):
            return SymbolDescriptor.ScipSuffix.Local
        if self.uri.endswith("/"):
            return SymbolDescriptor.ScipSuffix.Namespace
        elif self.uri.endswith("#"):
            return SymbolDescriptor.ScipSuffix.Type
        elif self.uri.endswith(")."):
            return SymbolDescriptor.ScipSuffix.Method
        elif self.uri.endswith("."):
            return SymbolDescriptor.ScipSuffix.Term
        elif self.uri.endswith(":"):
            return SymbolDescriptor.ScipSuffix.Meta
        elif self.uri.endswith(")"):
            return SymbolDescriptor.ScipSuffix.Parameter
        elif self.uri.endswith("]"):
            return SymbolDescriptor.ScipSuffix.TypeParameter
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.uri}")

    def parent(self) -> "Symbol":
        """Returns the parent symbol of the current symbol."""
        parent_descriptors = list(self.descriptors)[:-1]
        return Symbol(self.uri, self.scheme, self.package, tuple(parent_descriptors))

    @property
    def dotpath(self) -> str:
        """Returns the dotpath of the symbol."""
        return ".".join([ele.name for ele in self.descriptors])

    @property
    def module_name(self) -> str:
        """Returns the module name of the symbol."""
        return self.descriptors[0].name

    @staticmethod
    def is_local(symbol: "Symbol") -> bool:
        """Returns True if the symbol is local."""
        return symbol.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Local

    @staticmethod
    def is_meta(symbol: "Symbol") -> bool:
        """Returns True if the symbol is meta."""
        return symbol.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Meta

    @staticmethod
    def is_parameter(symbol: "Symbol") -> bool:
        """Returns True if the symbol is parameter."""
        return symbol.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Parameter

    @staticmethod
    def is_protobuf(symbol: "Symbol") -> bool:
        """Returns True if the symbol is a protobuf symbol."""
        return symbol.module_name.endswith("pb2")

    @classmethod
    def from_string(cls, symbol_str: str) -> "Symbol":
        """Creates a Symbol instance from a string representation."""
        # Assuming symbol_str is in the format: "Symbol({uri}, {scheme}, Package({manager} {name} {version}), [{Descriptor},...])"
        # Parse the symbol_str to extract the uri, scheme, package_str, and descriptors_str
        match = re.search(r"Symbol\((.*?), (.*?), Package\((.*?)\), \((.*?)\)\)", symbol_str)
        if not match:
            raise ValueError(f"Invalid symbol_str: {symbol_str}")
        uri, _, __, ___ = match.groups()
        # In current implementation, only the uri is used in re-construcing the symbol
        from automata.core.symbol.parser import parse_symbol

        return parse_symbol(uri)


@dataclass
class SymbolReference:
    """Represents a reference to a symbol in a file"""

    symbol: Symbol
    line_number: int
    column_number: int
    roles: Dict[str, Any]

    def __hash__(self) -> int:
        # This could cause collisions if the same symbol is referenced in different files at the same location
        return hash(f"{self.symbol.uri}-{self.line_number}-{self.column_number}")

    def __eq__(self, other) -> bool:
        if isinstance(other, SymbolReference):
            return (
                f"{self.symbol.uri}-{self.line_number}-{self.column_number}"
                == f"{other.symbol.uri}-{other.line_number}-{other.column_number}"
            )
        return False


@dataclass
class SymbolFile:
    """Represents a file that contains a symbol"""

    path: str
    occurrences: str

    def __hash__(self) -> int:
        return hash(self.path)

    def __eq__(self, other) -> bool:
        if isinstance(other, SymbolFile):
            return self.path == other.path
        elif isinstance(other, str):
            return self.path == other
        return False


class SymbolEmbedding(abc.ABC):
    """Abstract base class for different types of embeddings"""

    def __init__(self, symbol: Symbol, embedding_source: str, vector: np.ndarray):
        self.symbol = symbol
        self.embedding_source = embedding_source
        self.vector = vector


class SymbolCodeEmbedding(SymbolEmbedding):
    """A concrete class for symbol code embeddings"""

    def __init__(self, symbol: Symbol, source_code: str, vector: np.ndarray):
        super().__init__(symbol, source_code, vector)


class SymbolDocEmbedding(SymbolEmbedding):
    """A concrete class for symbol document embeddings"""

    def __init__(
        self,
        symbol: Symbol,
        document: str,
        vector: np.ndarray,
        source_code: Optional[str] = None,
        summary: Optional[str] = None,
        context: Optional[str] = None,
    ) -> None:
        super().__init__(symbol, document, vector)
        # begin additional meta data
        self.source_code = source_code
        self.summary = summary
        self.context = context
