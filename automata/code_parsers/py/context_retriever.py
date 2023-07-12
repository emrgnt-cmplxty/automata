import logging
from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, unparse, walk
from contextlib import contextmanager
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Union

from automata.code_parsers.py import (
    get_docstring_from_node,
    get_node_without_docstrings,
    get_node_without_imports,
)
from automata.symbol import Symbol

logger = logging.getLogger(__name__)


class PyContextRetrieverConfig:
    """The configuration for the PyContextRetriever"""

    def __init__(
        self,
        indent_level: int = 0,
        spacer: str = "  ",
    ) -> None:
        self.indent_level = indent_level
        self.spacer = spacer


class ContextComponent(Enum):
    HEADLINE = "headline"
    SOURCE_CODE = "source_code"
    INTERFACE = "interface"


class ContextComponentCallable(Protocol):
    def __call__(self, symbol: Symbol, ast_object: AST, **kwargs: Any) -> str:
        ...


class PyContextRetriever:
    """The PyContextRetriever is used to retrieve the context of a symbol in a Python project"""

    MAX_RECURSION_DEPTH = 2

    def __init__(
        self,
        config: PyContextRetrieverConfig = PyContextRetrieverConfig(),
        process_entry: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.spacer = config.spacer
        self.indent_level = config.indent_level
        self.process_entry = (
            process_entry if process_entry is not None else self._default_process_entry
        )
        self.context_components: Dict[ContextComponent, ContextComponentCallable] = {
            ContextComponent.HEADLINE: self._process_headline,
            ContextComponent.SOURCE_CODE: self._source_code,
            ContextComponent.INTERFACE: self._interface,
        }

    @contextmanager
    def increased_indentation(self):
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def _default_process_entry(self, message: str) -> str:
        spacer = self.spacer * self.indent_level
        indented_lines = [
            f"{spacer}{line}" if line.strip() else line for line in message.split("\n")
        ]
        return "\n".join(indented_lines) + "\n"

    def process_symbol(
        self,
        symbol: Symbol,
        ordered_active_components: Dict[ContextComponent, Dict],
    ) -> str:
        """
        Process the context of a specified `Symbol`. The caller has the responsibility
        to decide the indent level and context components to be processed.
        """
        from automata.symbol import convert_to_ast_object

        ast_object = convert_to_ast_object(symbol)

        if {ContextComponent.INTERFACE, ContextComponent.SOURCE_CODE}.issubset(
            ordered_active_components.keys()
        ):
            raise ValueError("Cannot retrieve both INTERFACE and SOURCE_CODE at the same time.")
        context = ""
        for component, kwargs in ordered_active_components.items():
            if component in self.context_components:
                context += self.process_entry(
                    self.context_components[component](symbol, ast_object, **kwargs)
                )
            else:
                logger.warn(f"Warning: {component} is not a valid context component.")
        return context

    def _process_headline(
        self,
        symbol: Symbol,
        ast_object: AST,
        headline_prefix="Building context for symbol - ",
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into a headline."""
        return f"{headline_prefix}{symbol.full_dotpath}\n"

    def _source_code(
        self,
        symbol: Symbol,
        ast_object: AST,
        include_imports: bool = False,
        include_docstrings: bool = True,
        max_length: Optional[int] = None,
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into underlying source code."""

        if not include_docstrings:
            ast_object = get_node_without_docstrings(ast_object)

        if not include_imports:
            ast_object = get_node_without_imports(ast_object)

        source = unparse(ast_object)

        return source[:max_length] if max_length else source

    def _interface(
        self,
        symbol: Optional[Symbol],
        ast_object: AST,
        skip_private: bool = True,
        include_docstrings: bool = True,
        header: str = "Interface:\n\n",
        class_header: str = "class ",
        recursion_depth: int = 0,
        processed_classes: Optional[Set[int]] = None,  # add this argument
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into an interface, skipping 'private' methods/classes if indicated."""
        if recursion_depth > self.MAX_RECURSION_DEPTH:
            raise RecursionError(f"Max recursion depth of {self.MAX_RECURSION_DEPTH} exceeded.")

        if processed_classes is None:
            processed_classes = set()

        if id(ast_object) in processed_classes:
            return ""

        # add the class so that we do not process it twice
        processed_classes.add(id(ast_object))

        # indent according to indent_level
        interface = self.process_entry(header)

        if include_docstrings:
            interface += self.process_entry(get_docstring_from_node(ast_object) + "\n")

        classes = self._get_all_classes(ast_object)
        with self.increased_indentation():
            for cls in classes:
                decorators = [f"@{unparse(dec)}" for dec in cls.decorator_list]
                class_header = f"{class_header}{cls.name}:\n\n"
                class_header = "\n".join(decorators + [class_header])
                interface += self._interface(
                    None,
                    cls,
                    skip_private,
                    include_docstrings,
                    header,
                    class_header,
                    recursion_depth=recursion_depth + 1,
                    processed_classes=processed_classes,
                )

        methods = sorted(self._get_all_methods(ast_object), key=lambda x: x.name)
        for method in methods:
            if not skip_private or not self._is_private_method(method):
                interface += self.process_entry(self._process_method(method))
                if include_docstrings:
                    interface += self.process_entry(get_docstring_from_node(method) + "\n")

        return interface

    def _is_private_method(self, method: Union[AsyncFunctionDef, FunctionDef]) -> bool:
        """Checks if a method is private, i.e., starts with '_'."""
        return method.name.startswith("_")

    def _process_method(self, method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        """
        Processes a specified method by printing its name, arguments, and return type.
        If we are processing the main symbol, we also print the method's code.
        """
        decorators = [f"@{unparse(dec)}" for dec in method.decorator_list]
        method_definition = f"{method.name}({self._get_method_arguments(method)})"
        return_annotation = self._get_method_return_annotation(method)
        return "\n".join(decorators + [f"{method_definition} -> {return_annotation}\n"])

    @staticmethod
    def _get_method_return_annotation(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        return unparse(method.returns) if method.returns is not None else "None"

    @staticmethod
    def _get_all_methods(ast: AST) -> List[Union[FunctionDef, AsyncFunctionDef]]:
        return [node for node in walk(ast) if isinstance(node, (FunctionDef, AsyncFunctionDef))]

    @staticmethod
    def _get_all_classes(ast: AST) -> List[ClassDef]:
        return [node for node in walk(ast) if isinstance(node, ClassDef)]

    @staticmethod
    def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        args = []
        defaults = dict(
            zip([arg.arg for arg in reversed(method.args.args)], reversed(method.args.defaults))
        )

        for arg in method.args.args:
            if arg.arg in defaults:
                args.append(f"{unparse(arg)}={unparse(defaults[arg.arg])}")
            else:
                args.append(unparse(arg))

        # Handle keyword-only arguments
        if method.args.kwonlyargs:
            for kwarg in method.args.kwonlyargs:
                default = next(
                    (
                        kw_default
                        for kw_default, kw_arg in zip(
                            method.args.kw_defaults, method.args.kwonlyargs
                        )
                        if kw_arg.arg == kwarg.arg
                    ),
                    None,
                )

                if default is not None:
                    args.append(f"{unparse(kwarg)}={unparse(default)}")
                else:
                    args.append(unparse(kwarg))

        return ", ".join(args)
