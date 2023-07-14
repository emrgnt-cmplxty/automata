from ast import (
    AST,
    AnnAssign,
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    iter_child_nodes,
    unparse,
    walk,
)
from typing import List, Union


def is_private_method(method: Union[AsyncFunctionDef, FunctionDef]) -> bool:
    """Checks if a method is private, i.e., starts with '_'."""
    return method.name.startswith("_") and not method.name.startswith("__")


def process_method(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
    """
    Processes a specified method by printing its name, arguments, and return type.
    If we are processing the main symbol, we also print the method's code.
    """
    decorators = [f"@{unparse(dec)}" for dec in method.decorator_list]
    method_definition = f"{method.name}({_get_method_arguments(method)})"
    return_annotation = _get_method_return_annotation(method)
    return "\n".join(
        decorators + [f"{method_definition} -> {return_annotation}"]
    )


def get_all_methods(ast: AST) -> List[Union[FunctionDef, AsyncFunctionDef]]:
    return [
        node
        for node in walk(ast)
        if isinstance(node, (FunctionDef, AsyncFunctionDef))
    ]


def get_all_classes(ast: AST) -> List[ClassDef]:
    return [node for node in walk(ast) if isinstance(node, ClassDef)]


def get_all_attributes(cls: ClassDef):
    return [
        node for node in iter_child_nodes(cls) if isinstance(node, AnnAssign)
    ]


def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
    args = []
    defaults = {
        arg.arg: default
        for arg, default in zip(
            reversed(method.args.args), reversed(method.args.defaults)
        )
    }

    for arg in method.args.args:
        if arg.arg in defaults:
            args.append(f"{unparse(arg)}={unparse(defaults[arg.arg])}")
        else:
            args.append(unparse(arg))

    # Handle keyword-only arguments
    if method.args.kwonlyargs:
        for kwarg, default in zip(
            method.args.kwonlyargs, method.args.kw_defaults
        ):
            if default is not None:
                args.append(f"{unparse(kwarg)}={unparse(default)}")
            else:
                args.append(unparse(kwarg))

    return ", ".join(args)


def _get_method_return_annotation(
    method: Union[AsyncFunctionDef, FunctionDef]
) -> str:
    return unparse(method.returns) if method.returns is not None else "None"
