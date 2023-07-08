from ast import AsyncFunctionDef, ClassDef, FunctionDef, Module
from typing import Union

ASTNode = Union[AsyncFunctionDef, ClassDef, FunctionDef, Module]
