import textwrap
import ast
import random
import string

import pytest
from spork.tools.python_tools.python_ast_manipulator import PythonASTManipulator


class MockCodeGenerator:
    def __init__(
        self,
        has_class: bool = False,
        has_method: bool = False,
        has_function: bool = False,
        has_import: bool = False,
        has_module_docstring: bool = False,
        has_class_docstring: bool = False,
        has_method_docstring: bool = False,
        has_function_docstring: bool = False,
    ):
        self.has_class = has_class
        self.has_method = has_method
        self.has_function = has_function
        self.has_import = has_import
        self.has_module_docstring = has_module_docstring
        self.has_class_docstring = has_class_docstring
        self.has_method_docstring = has_method_docstring
        self.has_function_docstring = has_function_docstring

        self.import_class_name = MockCodeGenerator.random_string(5)
        self.class_name = MockCodeGenerator.random_string(5)
        self.method_name = MockCodeGenerator.random_string(5)
        self.function_name = MockCodeGenerator.random_string(5)
        self.module_docstring = MockCodeGenerator.random_string(20)
        self.class_docstring = MockCodeGenerator.random_string(20)
        self.method_docstring = MockCodeGenerator.random_string(20)
        self.function_docstring = MockCodeGenerator.random_string(20)

    def generate_code(self):
        module_docstring = f'"""{self.module_docstring}"""\n' if self.has_module_docstring else ""
        class_docstring = f'"""{self.class_docstring}"""\n' if self.has_class_docstring else ""
        method_docstring = f'"""{self.method_docstring}"""\n' if self.has_method_docstring else ""
        function_docstring = (
            f'"""{self.function_docstring}"""\n' if self.has_function_docstring else ""
        )
        import_statement = f"import {self.import_class_name}\n" if self.has_import else ""

        method_code = textwrap.dedent(
            f"""def method(self):
                    {method_docstring}
                    pass
                """
            if self.has_class and self.has_method
            else ""
        )
        class_code = textwrap.dedent(
            f"""
            class {self.class_name}:
                {class_docstring}
                def __init__(self):
                    pass
                {method_code}
            """
            if self.has_class
            else ""
        )

        function_code = (
            textwrap.dedent(
                f"""
            def {self.function_name}():
                {function_docstring}
                pass
            """
            )
            if self.has_function
            else ""
        )

        return f"{import_statement}{module_docstring}{class_code}\n\n{function_code}"

    def _check_function_obj(self, function_obj=None):
        if function_obj is None:
            source_code = self.generate_code()
            function_obj = PythonASTManipulator._create_function_from_source(source_code)

        assert function_obj.name == self.function_name
        if self.has_function_docstring:
            assert function_obj.body[0].value.s == self.function_docstring
            assert isinstance(function_obj.body[0], ast.Expr)
            assert isinstance(function_obj.body[1], ast.Pass)
        else:
            assert isinstance(function_obj.body[0], ast.Pass)

    def _check_class_obj(self, class_obj=None):
        if class_obj is None:
            source_code = self.generate_code()
            class_obj = PythonASTManipulator._create_class_from_source(source_code)

        assert class_obj.name == self.class_name
        if self.has_class_docstring:
            assert isinstance(class_obj, ast.ClassDef)
            assert isinstance(class_obj.body[0], ast.Expr)
            assert isinstance(class_obj.body[1], ast.FunctionDef)
        else:
            assert isinstance(class_obj, ast.ClassDef)
            assert isinstance(class_obj.body[0], ast.FunctionDef)

        if self.has_method:
            method_obj = class_obj.body[2] if self.has_class_docstring else class_obj.body[1]
            assert method_obj.name == "method"
            if self.has_method_docstring:
                assert isinstance(method_obj.body[0], ast.Expr)  # docstring
                assert isinstance(method_obj.body[1], ast.Pass)  # pass
            else:
                assert isinstance(method_obj.body[0], ast.Pass)

    def _check_module_obj(self, module_obj=None):
        if module_obj is None:
            source_code = self.generate_code()
            module_obj = PythonASTManipulator._create_class_from_source(source_code)
        if self.has_module_docstring:
            assert isinstance(module_obj.body[0], ast.Expr)
            assert isinstance(module_obj.body[1], ast.ClassDef)
        else:
            assert isinstance(module_obj.body[0], ast.ClassDef)

    @staticmethod
    def random_string(length: int):
        return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.fixture
def python_ast_parser():
    return PythonASTManipulator()


def test_create_function_source_function():
    mock_generator = MockCodeGenerator(has_function=True)
    mock_generator._check_function_obj()

    mock_generator = MockCodeGenerator(has_function=True, has_function_docstring=True)
    mock_generator._check_function_obj()


def test_create_class_source_function():
    source_code = MockCodeGenerator(has_function=True).generate_code()
    with pytest.raises(ValueError):
        PythonASTManipulator._create_class_from_source(source_code)


def test_create_class_source_class():
    mock_generator = MockCodeGenerator(has_class=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(has_class=True, has_class_docstring=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(has_class=True, has_method=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(has_class=True, has_class_docstring=True, has_method=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_method=True, has_method_docstring=True
    )
    mock_generator._check_class_obj()


def test_create_function_source_class():
    mock_generator = MockCodeGenerator(has_class=True)
    source_code = mock_generator.generate_code()
    with pytest.raises(ValueError):
        PythonASTManipulator._create_function_from_source(source_code)


def test_find_object():
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()

    module_obj = PythonASTManipulator._create_module_from_source(source_code)
    function_obj = PythonASTManipulator._find_class_or_function(
        module_obj, mock_generator.function_name
    )

    mock_generator._check_function_obj(function_obj)

    class_obj = PythonASTManipulator._find_class_or_function(module_obj, mock_generator.class_name)
    mock_generator._check_class_obj(class_obj)


def test_extend_module():
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    module_obj = PythonASTManipulator._create_module_from_source(source_code)
    mock_generator._check_module_obj(module_obj)

    mock_generator_2 = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code_2 = mock_generator_2.generate_code()

    PythonASTManipulator().update_module(
        code=source_code_2, module_obj=module_obj, extending_module=True
    )

    # Check module 2 is merged into module 1
    mock_generator._check_module_obj(module_obj)
    mock_generator._check_class_obj(module_obj.body[0])
    mock_generator._check_function_obj(module_obj.body[1])
    mock_generator_2._check_class_obj(module_obj.body[2])
    mock_generator_2._check_function_obj(module_obj.body[3])


def test_reduce_module():
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    module_obj = PythonASTManipulator._create_module_from_source(source_code)
    class_obj = module_obj.body[0]
    function_obj = module_obj.body[1]
    PythonASTManipulator().update_module(
        code=ast.unparse(class_obj), module_obj=module_obj, extending_module=False
    )
    assert module_obj.body[0] == function_obj
