import re
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import Any, Dict, List, Optional, Union

import numpy as np

from automata.tools.search.scip_pb2 import Descriptor as DescriptorProto

"""
SCIP produces symbol URI, it identifies a class, method, or a local variable, along with the entire AST path to it.
Full spec: https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/docs/scip.md#symbol
The classes and functions in this file are used to convert the symbol URI into a human-readable form that can be used to query the index.
"""


# Symbol Related Types
class Descriptor:
    ScipSuffix = DescriptorProto

    class PythonKinds(Enum):
        Local = "local"
        Module = "module"
        Class = "class"
        Method = "method"
        Value = "value"
        Meta = "meta"
        Macro = "macro"
        Parameter = "parameter"
        TypeParameter = "type_parameter"

    def __init__(self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None):
        self.name = name
        self.suffix = suffix
        self.disambiguator = disambiguator

    def __repr__(self):
        return f"Descriptor({self.name}, {self.suffix}" + (
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
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.suffix}")

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
    def convert_scip_to_python_suffix(descriptor_suffix: DescriptorProto) -> PythonKinds:
        if descriptor_suffix == Descriptor.ScipSuffix.Local:
            return Descriptor.PythonKinds.Local

        elif descriptor_suffix == Descriptor.ScipSuffix.Namespace:
            return Descriptor.PythonKinds.Module

        elif descriptor_suffix == Descriptor.ScipSuffix.Type:
            return Descriptor.PythonKinds.Class

        elif descriptor_suffix == Descriptor.ScipSuffix.Method:
            return Descriptor.PythonKinds.Method

        elif descriptor_suffix == Descriptor.ScipSuffix.Term:
            return Descriptor.PythonKinds.Value

        elif descriptor_suffix == Descriptor.ScipSuffix.Macro:
            return Descriptor.PythonKinds.Macro

        elif descriptor_suffix == Descriptor.ScipSuffix.Parameter:
            return Descriptor.PythonKinds.Parameter

        elif descriptor_suffix == Descriptor.ScipSuffix.TypeParameter:
            return Descriptor.PythonKinds.TypeParameter

        else:
            return Descriptor.PythonKinds.Meta


@dataclass
class Package:
    manager: str
    name: str
    version: str

    def __repr__(self):
        return f"Package({self.unparse()})"

    def unparse(self):
        """Converts back into URI string"""
        return f"{self.manager} {self.name} {self.version}"


@dataclass
class Symbol:
    uri: str
    scheme: str
    package: Package
    descriptors: List[Descriptor]

    def __repr__(self):
        return f"Symbol({self.uri}, {self.scheme}, {self.package}, {self.descriptors})"

    def __hash__(self) -> int:
        return hash(self.uri)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other
        return False

    def symbol_kind_by_suffix(self) -> Descriptor.PythonKinds:
        return Descriptor.convert_scip_to_python_suffix(self.symbol_raw_kind_by_suffix())

    def symbol_raw_kind_by_suffix(self) -> DescriptorProto:
        if self.uri.startswith("local"):
            return Descriptor.ScipSuffix.Local
        if self.uri.endswith("/"):
            return Descriptor.ScipSuffix.Namespace
        elif self.uri.endswith("#"):
            return Descriptor.ScipSuffix.Type
        elif self.uri.endswith(")."):
            return Descriptor.ScipSuffix.Method
        elif self.uri.endswith("."):
            return Descriptor.ScipSuffix.Term
        elif self.uri.endswith(":"):
            return Descriptor.ScipSuffix.Meta
        elif self.uri.endswith(")"):
            return Descriptor.ScipSuffix.Parameter
        elif self.uri.endswith("]"):
            return Descriptor.ScipSuffix.TypeParameter
        else:
            raise ValueError(f"Invalid descriptor suffix: {self.uri}")

    @classmethod
    def from_string(cls, symbol_str: str) -> "Symbol":
        """
        Creates a Symbol instance from a string representation

        :param symbol_str: The string representation of the Symbol
        :return: A Symbol instance
        """
        # Assuming symbol_str is in the format: "Symbol({uri}, {scheme}, Package({manager} {name} {version}), [{Descriptor},...])"
        # Parse the symbol_str to extract the uri, scheme, and package_str
        match = re.search(r"Symbol\((.*?), (.*?), Package\((.*?)\), \[(.*?)\]\)", symbol_str)
        if not match:
            raise ValueError(f"Invalid symbol_str: {symbol_str}")
        uri, _, __, ___ = match.groups()
        from automata.tools.search.symbol_parser import parse_uri_to_symbol

        return parse_uri_to_symbol(uri)


@dataclass
class SymbolReference:
    symbol: Symbol
    line_number: int
    roles: Dict[str, Any]


@dataclass
class SymbolEmbedding:
    symbol: Symbol
    vector: np.ndarray
    source_code: str


# Path and os related variables
StrPath = Union[str, PathLike]
PyPath = str


@dataclass
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
