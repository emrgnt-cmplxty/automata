import ast
import os
import random
import string
import textwrap

import pytest

from automata.tools.python_tools.python_indexer import PythonIndexer
from automata.tools.python_tools.python_writer import PythonWriter


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

        # self.import_class_name = MockCodeGenerator.random_string(5)
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
        import_statement = f"import random\n" if self.has_import else ""

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

        return f"{module_docstring}{import_statement}{class_code}\n\n{function_code}"

    def _check_function_obj(self, function_obj=None):
        if function_obj is None:
            source_code = self.generate_code()
            function_obj = ast.parse(source_code).body[0]

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
            class_obj = ast.parse(source_code).body[0]

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
            module_obj = ast.parse(source_code)
        if self.has_module_docstring:
            assert isinstance(module_obj.body[0], ast.Expr)
            assert isinstance(module_obj.body[1], ast.ClassDef)
        else:
            assert isinstance(module_obj.body[0], ast.ClassDef)

    @staticmethod
    def random_string(length: int):
        return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.fixture
def python_writer():
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    indexer = PythonIndexer(sample_dir)

    return PythonWriter(indexer)


def test_create_function_source_function():
    mock_generator = MockCodeGenerator(has_function=True)
    mock_generator._check_function_obj()

    mock_generator = MockCodeGenerator(has_function=True, has_function_docstring=True)
    mock_generator._check_function_obj()


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


def test_find_object(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()

    module_obj = python_writer._create_module_from_source_code("test_module_2", source_code)
    function_obj = PythonWriter._find_function_class_or_method(
        module_obj, mock_generator.function_name
    )

    mock_generator._check_function_obj(function_obj)

    class_obj = PythonWriter._find_function_class_or_method(module_obj, mock_generator.class_name)
    mock_generator._check_class_obj(class_obj)


def test_extend_module(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    module_obj = python_writer._create_module_from_source_code("test_module_2", source_code)
    mock_generator._check_module_obj(module_obj)

    mock_generator_2 = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code_2 = mock_generator_2.generate_code()

    python_writer.update_module(
        source_code=source_code_2, module_obj=module_obj, extending_module=True
    )

    # Check module 2 is merged into module 1
    mock_generator._check_module_obj(module_obj)
    mock_generator._check_class_obj(module_obj.body[0])
    mock_generator._check_function_obj(module_obj.body[1])
    mock_generator_2._check_class_obj(module_obj.body[2])
    mock_generator_2._check_function_obj(module_obj.body[3])


def test_reduce_module(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    module_obj = python_writer._create_module_from_source_code("test_module_2", source_code)
    class_obj = module_obj.body[0]
    function_obj = module_obj.body[1]
    python_writer.update_module(
        source_code=ast.unparse(class_obj), module_obj=module_obj, extending_module=False
    )
    assert module_obj.body[0] == function_obj


def test_create_update_write_module(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    python_writer.update_module(
        source_code=source_code, module_path="test_module_2", extending_module=False
    )
    python_writer.write_module("test_module_2")
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    os.remove(os.path.join(root_dir, "test_module_2.py"))


def test_create_function_with_arguments():
    mock_generator = MockCodeGenerator(has_function=True, has_function_docstring=True)
    source_code = mock_generator.generate_code()
    # Add a function with different types of arguments
    source_code += textwrap.dedent(
        f"""
        def {mock_generator.function_name}_with_args(pos_arg, kw_arg=None, *args, **kwargs):
            pass
        """
    )
    module_obj = ast.parse(source_code)
    function_obj = PythonWriter._find_function_class_or_method(
        module_obj, f"{mock_generator.function_name}_with_args"
    )
    assert function_obj.name == f"{mock_generator.function_name}_with_args"
    assert len(function_obj.args.args) == 2
    assert function_obj.args.args[0].arg == "pos_arg"
    assert function_obj.args.args[1].arg == "kw_arg"
    assert not function_obj.args.defaults[0].value
    assert function_obj.args.vararg.arg == "args"
    assert function_obj.args.kwarg.arg == "kwargs"


def test_create_class_with_multiple_methods_properties_attributes():
    mock_generator = MockCodeGenerator(has_class=True, has_class_docstring=True)
    source_code = mock_generator.generate_code()
    # Add class attributes, multiple methods, and a property
    source_code += textwrap.dedent(
        f"""
        class {mock_generator.class_name}_extended:
            class_attribute = "Some value"

            def method_1(self):
                pass

            def method_2(self, arg):
                pass

            @property
            def some_property(self):
                return self.class_attribute
        """
    )
    module_obj = ast.parse(source_code)
    class_obj = PythonWriter._find_function_class_or_method(
        module_obj, f"{mock_generator.class_name}_extended"
    )
    assert len(class_obj.body) == 4  # class_attribute, method_1, method_2, some_property


def test_create_class_inheritance():
    mock_generator = MockCodeGenerator(has_class=True)
    source_code = mock_generator.generate_code()
    # Add a subclass that inherits from the parent class
    source_code += textwrap.dedent(
        f"""
        class {mock_generator.class_name}_child({mock_generator.class_name}):
            pass
        """
    )
    module_obj = ast.parse(source_code)
    class_obj = PythonWriter._find_function_class_or_method(
        module_obj, f"{mock_generator.class_name}_child"
    )
    assert class_obj.bases[0].id == mock_generator.class_name


def test_reduce_module_remove_function(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()

    module_obj = python_writer._create_module_from_source_code("test_module_2", source_code)

    class_obj = module_obj.body[0]
    function_obj = module_obj.body[1]
    python_writer.update_module(
        source_code=ast.unparse(function_obj), module_obj=module_obj, extending_module=False
    )
    assert module_obj.body[0] == class_obj
    assert len(module_obj.body) == 1


def test_update_existing_function(python_writer):
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    # Create a new version of the function with a different body
    source_code_updated = textwrap.dedent(
        f"""
        def {mock_generator.function_name}():
            return "Updated"
        """
    )
    module_obj = python_writer._create_module_from_source_code("test_module_2", source_code)
    python_writer.update_module(
        source_code=source_code_updated, module_obj=module_obj, extending_module=True
    )
    updated_function_obj = PythonWriter._find_function_class_or_method(
        module_obj, mock_generator.function_name
    )
    assert len(updated_function_obj.body) == 1
    assert isinstance(updated_function_obj.body[0], ast.Return)


def test_write_and_retrieve_mock_code(python_writer):
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_method=True,
        has_function=True,
        has_import=True,
        has_module_docstring=True,
        has_class_docstring=True,
        has_method_docstring=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()
    python_writer._create_module_from_source_code("test_module_2", source_code)

    python_writer.write_module("test_module_2")

    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    indexer = PythonIndexer(sample_dir)

    module_docstring = indexer.retrieve_docstring("test_module_2", None)
    assert module_docstring == mock_generator.module_docstring
