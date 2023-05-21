import re
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import Any, Dict, Optional, Tuple, Union

from automata.tools.search.scip_pb2 import Descriptor as DescriptorProto

"""
SCIP produces symbol URI, it identifies a class, method, or a local variable, along with the entire AST path to it.
Full spec: https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/docs/scip.md#symbol
The classes and functions in this file are used to convert the symbol URI into a human-readable form that can be used to query the index.
"""

ScipSuffix = DescriptorProto.Suffix


class PythonTypes(Enum):
    Local = "local"
    Module = "module"
    Class = "class"
    Method = "method"
    Value = "value"
    Meta = "meta"
    Macro = "macro"
    Parameter = "parameter"
    TypeParameter = "type_parameter"


@dataclass(frozen=True)
class Descriptor:
    name: str
    suffix: ScipSuffix
    disambiguator: Optional[str] = None

    def unparse(self):
        """Converts back into URI string"""
        escaped_name = Descriptor.get_escaped_name(self.name)
        if self.suffix == ScipSuffix.Namespace:
            return f"{escaped_name}/"
        elif self.suffix == ScipSuffix.Type:
            return f"{escaped_name}#"
        elif self.suffix == ScipSuffix.Term:
            return f"{escaped_name}."
        elif self.suffix == ScipSuffix.Meta:
            return f"{escaped_name}:"
        elif self.suffix == ScipSuffix.Method:
            return f"{escaped_name}({self.disambiguator})."
        elif self.suffix == ScipSuffix.Parameter:
            return f"({escaped_name})"
        elif self.suffix == ScipSuffix.TypeParameter:
            return f"[{escaped_name}]"
        elif self.suffix == ScipSuffix.Local:
            return f"local {escaped_name}"
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.suffix}")

    @staticmethod
    def symbol_kind_by_suffix(uri: str):
        if uri.startswith("local"):
            return ScipSuffix.Local
        if uri.endswith("/"):
            return ScipSuffix.Namespace
        elif uri.endswith("#"):
            return ScipSuffix.Type
        elif uri.endswith(")."):
            return ScipSuffix.Method
        elif uri.endswith("."):
            return ScipSuffix.Term
        elif uri.endswith(":"):
            return ScipSuffix.Meta
        elif uri.endswith(")"):
            return ScipSuffix.Parameter
        elif uri.endswith("]"):
            return ScipSuffix.TypeParameter
        else:
            raise ValueError(f"Invalid descriptor suffix: {uri}")

    @staticmethod
    def get_escaped_name(name):
        def is_simple_identifier(name):
            return re.match(r"^[\w$+-]+$", name) is not None

        if not name:
            return ""
        if is_simple_identifier(name):
            return name
        return "`" + re.sub("`", "``", name) + "`"

    @staticmethod
    def convert_scip_to_python_suffix(descriptor: "Descriptor") -> PythonTypes:
        if descriptor.suffix == ScipSuffix.Local:
            return PythonTypes.Local

        elif descriptor.suffix == ScipSuffix.Namespace:
            return PythonTypes.Module

        elif descriptor.suffix == ScipSuffix.Type:
            return PythonTypes.Class

        elif descriptor.suffix == ScipSuffix.Method:
            return PythonTypes.Method

        elif descriptor.suffix == ScipSuffix.Term:
            return PythonTypes.Value

        elif descriptor.suffix == ScipSuffix.Macro:
            return PythonTypes.Macro

        elif descriptor.suffix == ScipSuffix.Parameter:
            return PythonTypes.Parameter

        elif descriptor.suffix == ScipSuffix.TypeParameter:
            return PythonTypes.TypeParameter

        else:
            return PythonTypes.Meta


@dataclass(frozen=True)
class Package:
    manager: str
    name: str
    version: str

    def unparse(self):
        """Converts back into URI string"""
        return f"{self.manager} {self.name} {self.version}"


@dataclass(frozen=True, eq=False)
class Symbol:
    scheme: str
    package: Package
    descriptors: Tuple[Descriptor, ...]

    def unparse(self) -> str:
        """Converts back into URI string"""
        return f"{self.scheme} {self.package.unparse()} {''.join([descriptor.unparse() for descriptor in self.descriptors])}"

    @property
    def uri(self) -> str:
        return self.unparse()

    @property
    def module_name(self) -> str:
        return self.descriptors[0].name

    def parent(self) -> "Symbol":
        parent_descriptors = list(self.descriptors)[:-1]
        return Symbol(self.scheme, self.package, tuple(parent_descriptors))

    def __hash__(self) -> int:
        return hash(self.uri)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other
        return False


@dataclass(frozen=True)
class SymbolReference:
    symbol: Symbol
    line_number: int
    column_number: int
    roles: Dict[str, Any]


@dataclass(frozen=True)
class File:
    path: str
    occurrences: str

    def __hash__(self) -> int:
        return hash(self.path)

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        elif isinstance(other, str):
            return self.path == other
        return False


StrPath = Union[str, PathLike]
PyPath = str
