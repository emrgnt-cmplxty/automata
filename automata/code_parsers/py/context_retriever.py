import logging
from abc import ABC, abstractmethod
from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, unparse, walk
from contextlib import contextmanager
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    Set,
    Union,
)

from automata.code_parsers.py import (
    AST_NO_RESULT_FOUND,
    get_docstring_from_node,
    get_node_without_docstrings,
    get_node_without_imports,
)

if TYPE_CHECKING:
    from automata.symbol.base import Symbol  # avoid circular dependencies

logger = logging.getLogger(__name__)


def _is_private_method(method: Union[AsyncFunctionDef, FunctionDef]) -> bool:
    """Checks if a method is private, i.e., starts with '_'."""
    return method.name.startswith("_")


def _get_method_return_annotation(
    method: Union[AsyncFunctionDef, FunctionDef]
) -> str:
    return unparse(method.returns) if method.returns is not None else "None"


def _get_all_methods(ast: AST) -> List[Union[FunctionDef, AsyncFunctionDef]]:
    return [
        node
        for node in walk(ast)
        if isinstance(node, (FunctionDef, AsyncFunctionDef))
    ]


def _get_all_classes(ast: AST) -> List[ClassDef]:
    return [node for node in walk(ast) if isinstance(node, ClassDef)]


def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
    args = []
    defaults = dict(
        zip(
            [arg.arg for arg in reversed(method.args.args)],
            reversed(method.args.defaults),
        )
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


def _process_method(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
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


class ContextComponent(Enum):
    HEADLINE = "headline"
    SOURCE_CODE = "source_code"
    INTERFACE = "interface"


class ContextComponentCallable(Protocol):
    def __call__(
        self, symbol: "Symbol", ast_object: AST, **kwargs: Any
    ) -> str:
        ...


class BaseContextComponent(ABC):
    def __init__(self, spacer: str = "  ", indent_level: int = 0):
        self.spacer = spacer
        self.indent_level = indent_level

    @contextmanager
    def increased_indentation(self):
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def process_entry(self, message: str, include_newline=True) -> str:
        spacer = self.spacer * self.indent_level
        return "".join(
            f"{spacer}{line.strip()}\n" for line in message.split("\n")
        )

    @abstractmethod
    def generate(
        self, symbol: "Symbol", ast_object: AST, **kwargs: Any
    ) -> str:
        pass


class HeadlineContextComponent(BaseContextComponent):
    def generate(
        self,
        symbol: "Symbol",
        ast_object: AST,
        # headline="Building symbol context: ",
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into a headline."""
        return self.process_entry(symbol.full_dotpath)


class SourceCodeContextComponent(BaseContextComponent):
    def generate(
        self,
        symbol: "Symbol",
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

        print("ast_object = ", ast_object)
        if not include_imports:
            ast_object = get_node_without_imports(ast_object)

        source = unparse(ast_object)

        return source[:max_length] if max_length else source


class InterfaceContextComponent(BaseContextComponent):
    MAX_RECURSION_DEPTH = 2

    def generate(
        self,
        symbol: Optional["Symbol"],
        ast_object: AST,
        skip_private: bool = True,
        include_docstrings: bool = True,
        interface_header: str = "Interface:",
        class_header: str = "class ",
        recursion_depth: int = 0,
        processed_objects: Optional[Set[int]] = None,
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into an interface, skipping 'private' methods/classes if indicated."""
        if recursion_depth > self.MAX_RECURSION_DEPTH:
            raise RecursionError(
                f"Max recursion depth of {self.MAX_RECURSION_DEPTH} exceeded."
            )

        if processed_objects is None:
            processed_objects = set()
        interface = ""
        if symbol:
            interface += self.process_entry(f"\n{interface_header}")

        with self.increased_indentation():
            interface += self._process_classes_and_methods(
                ast_object,
                skip_private,
                include_docstrings,
                interface_header,
                class_header,
                recursion_depth,
                processed_objects,
            )

        return interface

    def _process_classes_and_methods(
        self,
        ast_object: AST,
        skip_private: bool,
        include_docstrings: bool,
        class_header_suffix: str,
        class_header: str,
        recursion_depth: int,
        processed_objects: Set[int],
    ) -> str:
        """Process all classes and methods in the ast_object."""
        interface = ""
        obj_docstring = get_docstring_from_node(ast_object)
        if include_docstrings and obj_docstring != AST_NO_RESULT_FOUND:
            interface += self.process_entry(f'"""{obj_docstring}"""' + "\n")

        classes = _get_all_classes(ast_object)

        for cls in classes:
            if id(cls) in processed_objects:
                continue
            processed_objects.add(id(cls))

            decorators = [f"@{unparse(dec)}" for dec in cls.decorator_list]
            class_header = f"{class_header}{cls.name}:"
            class_header = "\n".join(decorators + [class_header])
            interface += self.process_entry(f"{class_header}")

            with self.increased_indentation():
                interface += self.generate(
                    None,
                    cls,
                    skip_private,
                    include_docstrings,
                    class_header_suffix,
                    class_header,
                    recursion_depth=recursion_depth + 1,
                    processed_objects=processed_objects,
                )

        methods = sorted(_get_all_methods(ast_object), key=lambda x: x.name)
        for method in methods:
            if id(method) in processed_objects:
                continue
            processed_objects.add(id(method))

            if not skip_private or not _is_private_method(method):
                interface += self.process_entry(_process_method(method))
                method_docstring = get_docstring_from_node(method)
                if (
                    include_docstrings
                    and method_docstring != AST_NO_RESULT_FOUND
                ):
                    with self.increased_indentation():
                        interface += self.process_entry(
                            f'"""{method_docstring}"""' + "\n"
                        )
        return interface


class PyContextRetriever:
    """The PyContextRetriever is used to retrieve the context of a symbol in a Python project"""

    MAX_RECURSION_DEPTH = 2

    def __init__(
        self,
        spacer: str = "  ",
    ) -> None:
        self.spacer = spacer
        self.context_components: Dict[
            ContextComponent, BaseContextComponent
        ] = {
            ContextComponent.HEADLINE: HeadlineContextComponent(spacer),
            ContextComponent.SOURCE_CODE: SourceCodeContextComponent(spacer),
            ContextComponent.INTERFACE: InterfaceContextComponent(spacer),
        }

    def process_symbol(
        self,
        symbol: "Symbol",
        ordered_active_components: Dict[ContextComponent, Dict],
        indent_level=0,
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
            raise ValueError(
                "Cannot retrieve both INTERFACE and SOURCE_CODE at the same time."
            )

        context = ""
        for component, kwargs in ordered_active_components.items():
            if component in self.context_components:
                self.context_components[component].indent_level = indent_level
                context += self.context_components[component].generate(
                    symbol, ast_object, **kwargs
                )
            else:
                logger.warn(
                    f"Warning: {component} is not a valid context component."
                )
        return context
