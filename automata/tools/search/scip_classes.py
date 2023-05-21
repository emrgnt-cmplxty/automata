import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, NewType, Optional

from automata.tools.search.scip_pb2 import Descriptor as DescriptorProto

"""
SCIP produces symbol URI, it identifies a class, method, or a local variable, along with the entire AST path to it.
Full spec: https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/docs/scip.md#symbol
The classes and functions in this file are used to convert the symbol URI into a human-readable form that can be used to query the index.
"""


class Descriptor:
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

    def __init__(self, name: str, suffix: ScipSuffix, disambiguator: Optional[str] = None):
        self.name = name
        self.suffix = suffix
        self.disambiguator = disambiguator

    def __repr__(self):
        return f"Descriptor({self.name}, {self.ScipSuffix.Name(self.suffix)}" + (
            f", {self.disambiguator})" if self.disambiguator else ")"
        )

    def unparse(self):
        """Converts back into URI string"""
        escaped_name = Descriptor.get_escaped_name(self.name)
        if self.suffix == Descriptor.ScipSuffix.Namespace:
            return f"{escaped_name}/"
        elif self.suffix == Descriptor.ScipSuffix.Type:
            return f"{escaped_name}#"
        elif self.suffix == Descriptor.ScipSuffix.Term:
            return f"{escaped_name}."
        elif self.suffix == Descriptor.ScipSuffix.Meta:
            return f"{escaped_name}:"
        elif self.suffix == Descriptor.ScipSuffix.Method:
            return f"{escaped_name}({self.disambiguator})."
        elif self.suffix == Descriptor.ScipSuffix.Parameter:
            return f"({escaped_name})"
        elif self.suffix == Descriptor.ScipSuffix.TypeParameter:
            return f"[{escaped_name}]"
        elif self.suffix == Descriptor.ScipSuffix.Local:
            return f"local {escaped_name}"
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.suffix}")

    @staticmethod
    def symbol_kind_by_suffix(uri: str):
        if uri.startswith("local"):
            return Descriptor.ScipSuffix.Local
        if uri.endswith("/"):
            return Descriptor.ScipSuffix.Namespace
        elif uri.endswith("#"):
            return Descriptor.ScipSuffix.Type
        elif uri.endswith(")."):
            return Descriptor.ScipSuffix.Method
        elif uri.endswith("."):
            return Descriptor.ScipSuffix.Term
        elif uri.endswith(":"):
            return Descriptor.ScipSuffix.Meta
        elif uri.endswith(")"):
            return Descriptor.ScipSuffix.Parameter
        elif uri.endswith("]"):
            return Descriptor.ScipSuffix.TypeParameter
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
        if descriptor.suffix == Descriptor.ScipSuffix.Local:
            return Descriptor.PythonTypes.Local

        elif descriptor.suffix == Descriptor.ScipSuffix.Namespace:
            return Descriptor.PythonTypes.Module

        elif descriptor.suffix == Descriptor.ScipSuffix.Type:
            return Descriptor.PythonTypes.Class

        elif descriptor.suffix == Descriptor.ScipSuffix.Method:
            return Descriptor.PythonTypes.Method

        elif descriptor.suffix == Descriptor.ScipSuffix.Term:
            return Descriptor.PythonTypes.Value

        elif descriptor.suffix == Descriptor.ScipSuffix.Macro:
            return Descriptor.PythonTypes.Macro

        elif descriptor.suffix == Descriptor.ScipSuffix.Parameter:
            return Descriptor.PythonTypes.Parameter

        elif descriptor.suffix == Descriptor.ScipSuffix.TypeParameter:
            return Descriptor.PythonTypes.TypeParameter

        else:
            return Descriptor.PythonTypes.Meta


class Package:
    def __init__(self, manager: str, name: str, version: str):
        self.manager = manager
        self.name = name
        self.version = version

    def unparse(self):
        """Converts back into URI string"""
        return f"{self.manager} {self.name} {self.version}"

    def __repr__(self):
        return f"Package({self.unparse()})"


class Symbol:
    def __init__(self, scheme: str, package: Package, descriptors: List[Descriptor]):
        self.scheme = scheme
        self.package = package
        self.descriptors = tuple(descriptors)

    def __repr__(self):
        return f"Symbol({self.uri}, {self.scheme}, {self.package}, {self.descriptors})"

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
        return Symbol(self.scheme, self.package, parent_descriptors)

    def __hash__(self) -> int:
        return hash(self.uri)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other
        return False


@dataclass
class SymbolReference:
    symbol: Symbol
    line_number: int
    column_number: int
    details: Dict[str, Any]


File = NewType("File", str)
