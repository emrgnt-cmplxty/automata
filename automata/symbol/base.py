import abc
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from automata.symbol.scip_pb2 import Descriptor as DescriptorProto  # type: ignore # isort:skip


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
        self,
        name: str,
        suffix: DescriptorProto,
        disambiguator: Optional[str] = None,
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
        """Gets the escaped name of the symbol."""

        def is_simple_identifier(name):
            return re.match(r"^[\w$+-]+$", name) is not None

        if not name:
            return ""
        if is_simple_identifier(name):
            return name
        return "`" + re.sub("`", "``", name) + "`"

    @staticmethod
    def convert_scip_to_python_kind(
        descriptor_suffix: DescriptorProto,
    ) -> PyKind:
        """
        Converts a scip suffix to a python kind,
        e.g. a symbol ending with a `ScipSuffix.Method` descriptor will
        have a scip suffix of `Pykind.Method`.
        """
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

    symbol_class = parse_symbol(
        "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#"
    )

    symbol_method = parse_symbol(
        "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.base`/ToolNotFoundError#__init__()."
    )
    """

    uri: str
    scheme: str
    package: SymbolPackage
    descriptors: Tuple[SymbolDescriptor, ...]

    def __repr__(self) -> str:
        return f"Symbol({self.uri}, {self.scheme}, {self.package}, {self.descriptors})"

    def __str__(self) -> str:
        return self.uri

    def __hash__(self) -> int:
        return hash(self.uri)

    def __eq__(self, other) -> bool:
        if isinstance(other, Symbol):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other
        return False

    @property
    def parent(self) -> "Symbol":
        parent_descriptors = list(self.descriptors)[:-1]
        return Symbol(
            self.uri, self.scheme, self.package, tuple(parent_descriptors)
        )

    @property
    def py_kind(self) -> SymbolDescriptor.PyKind:
        return SymbolDescriptor.convert_scip_to_python_kind(
            self.descriptors[-1].suffix
        )

    @property
    def full_dotpath(self) -> str:
        return ".".join([ele.name for ele in self.descriptors])

    @property
    def module_path(self) -> str:
        return self.descriptors[0].name

    @property
    def is_local(self) -> bool:
        return self.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Local

    @property
    def is_meta(self) -> bool:
        return self.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Meta

    @property
    def is_parameter(self) -> bool:
        return (
            self.descriptors[0].suffix == SymbolDescriptor.ScipSuffix.Parameter
        )

    @property
    def is_protobuf(self) -> bool:
        return self.module_path.endswith("pb2")

    @classmethod
    def from_string(cls, symbol_str: str) -> "Symbol":
        """Creates a Symbol instance from a string representation."""
        # Assuming symbol_str is in the format: "Symbol({uri}, {scheme}, Package({manager} {name} {version}), [{Descriptor},...])"
        # Parse the symbol_str to extract the uri, scheme, package_str, and descriptors_str
        match = re.search(
            r"Symbol\((.*?), (.*?), Package\((.*?)\), \((.*?)\)\)", symbol_str
        )
        if not match:
            raise ValueError(f"Invalid symbol_str: {symbol_str}")
        uri, _, __, ___ = match.groups()
        # In current implementation, only the uri is used in re-construcing the symbol
        from automata.symbol.parser import parse_symbol

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
        return hash(
            f"{self.symbol.uri}-{self.line_number}-{self.column_number}"
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, SymbolReference):
            return (
                f"{self.symbol.uri}-{self.line_number}-{self.column_number}"
                == f"{other.symbol.uri}-{other.line_number}-{other.column_number}"
            )
        return False


class ISymbolProvider(abc.ABC):
    def __init__(self):
        self.is_synchronized = False

    @abc.abstractmethod
    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        """Gets the sorted list of supported symbols."""
        pass

    @abc.abstractmethod
    def filter_symbols(self, sorted_supported_symbols: List[Symbol]) -> None:
        """Filters the sorted list of supported symbols."""
        pass

    def get_sorted_supported_symbols(self) -> List[Symbol]:
        """Gets the sorted list of supported symbols."""
        from automata.core.utils import is_sorted

        if not self.is_synchronized:
            raise RuntimeError("Cannot get symbols before synchronization")

        sorted_symbols = self._get_sorted_supported_symbols()

        if not is_sorted([symbol.full_dotpath for symbol in sorted_symbols]):
            raise ValueError("sorted_supported_symbols must be sorted")

        return sorted_symbols

    def set_synchronized(self, value: bool):
        """Sets the synchronized flag."""
        self.is_synchronized = value
