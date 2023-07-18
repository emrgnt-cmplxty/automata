import ast
import os
import random
import string
import textwrap

import pytest

from automata.code_parsers.py import PyReader
from automata.code_writers.py.code_writer import PyCodeWriter
from automata.core import find_syntax_tree_node
from automata.singletons.py_module_loader import py_module_loader


@pytest.fixture(autouse=True)
def module_loader():
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
        "sample_modules",
    )
    yield py_module_loader


@pytest.fixture
def py_writer():
    retriever = PyReader()
    return PyCodeWriter(retriever)


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
        module_docstring = (
            f'"""{self.module_docstring}"""\n'
            if self.has_module_docstring
            else ""
        )
        class_docstring = (
            f'"""{self.class_docstring}"""\n'
            if self.has_class_docstring
            else ""
        )
        method_docstring = (
            f'"""{self.method_docstring}"""\n'
            if self.has_method_docstring
            else ""
        )
        function_docstring = (
            f'"""{self.function_docstring}"""\n'
            if self.has_function_docstring
            else ""
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
            assert isinstance(class_obj.body[0], ast.Expr)
            assert isinstance(class_obj.body[1], ast.FunctionDef)
        else:
            assert isinstance(class_obj.body[0], ast.FunctionDef)

        assert isinstance(class_obj, ast.ClassDef)
        if self.has_method:
            method_obj = (
                class_obj.body[2]
                if self.has_class_docstring
                else class_obj.body[1]
            )
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
        return "".join(
            random.choice(string.ascii_letters) for _ in range(length)
        )


def test_create_function_source_function():
    mock_generator = MockCodeGenerator(has_function=True)
    mock_generator._check_function_obj()

    mock_generator = MockCodeGenerator(
        has_function=True, has_function_docstring=True
    )
    mock_generator._check_function_obj()


def test_create_class_source_class():
    mock_generator = MockCodeGenerator(has_class=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True
    )
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(has_class=True, has_method=True)
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_method=True
    )
    mock_generator._check_class_obj()

    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_method=True,
        has_method_docstring=True,
    )
    mock_generator._check_class_obj()


def test_upsert_to_module(py_writer, module_loader):
    # Arrange
    # create module
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("sample_module_22", ast.parse(source_code))
    mock_generator_2 = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code_2 = mock_generator_2.generate_code()
    module_obj = module_loader.fetch_ast_module("sample_module_22")
    py_writer.upsert_to_module(module_obj, ast.parse(source_code_2))

    # Check module 2 is merged into module 1
    mock_generator._check_module_obj(module_obj)
    mock_generator._check_class_obj(module_obj.body[0])
    mock_generator._check_function_obj(module_obj.body[1])
    mock_generator_2._check_class_obj(module_obj.body[2])
    mock_generator_2._check_function_obj(module_obj.body[3])


def test_create_delete_module(py_writer, module_loader):
    # Arrange
    # create module
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module(
        "sample_module_22", ast.parse(source_code), do_write=True
    )
    assert os.path.exists(
        os.path.join(py_module_loader.root_fpath, "sample_module_22.py")
    )
    py_writer.delete_module("sample_module_22")
    assert not os.path.exists(
        os.path.join(py_module_loader.root_fpath, "sample_module_22.py")
    )


def test_delete_from_module(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("test_module_2", ast.parse(source_code))
    module_obj = py_module_loader.fetch_ast_module("test_module_2")
    function_obj = module_obj.body[1]
    new_module_obj = ast.Module(body=[function_obj], type_ignores=[])
    assert len(module_obj.body) == 2
    py_writer.delete_from_module(module_obj, new_module_obj)
    mock_generator._check_class_obj(module_obj.body[0])
    assert len(module_obj.body) == 1


def assert_code_lines_equal(code_1: str, code_2: str):
    code_1_lines = [line for line in code_1.splitlines() if line.strip()]
    code_2_lines = [line for line in code_2.splitlines() if line.strip()]
    assert all(
        line_1 == line_2 for line_1, line_2 in zip(code_1_lines, code_2_lines)
    )


def test_create_write_update_delete_module(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()
    # TODO - Find a real fix to this hacky workaround for file persistence
    if "sample_modules.sample_module_write" in py_module_loader:
        py_writer.delete_module("sample_modules.sample_module_write")

    py_writer.create_new_module(
        "sample_modules.sample_module_write",
        ast.parse(source_code),
        do_write=True,
    )
    fpath = os.path.join(
        py_module_loader.root_fpath, "sample_modules", "sample_module_write.py"
    )
    assert os.path.exists(fpath)
    with open(fpath, "r") as f:
        contents = f.read()
        assert_code_lines_equal(source_code, contents)

    mock_generator_2 = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code_2 = mock_generator_2.generate_code()

    assert source_code != source_code_2
    py_writer.upsert_to_module(
        ast.parse(source_code), ast.parse(source_code_2)
    )

    assert os.path.exists(fpath)
    with open(fpath, "r") as f:
        contents = f.read()
        assert_code_lines_equal(
            "\n".join([source_code, source_code_2]), contents
        )

    py_writer.delete_module("sample_modules.sample_module_write")
    # check deletion succeeded
    assert not os.path.exists(fpath)


def test_create_function_with_arguments():
    mock_generator = MockCodeGenerator(
        has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    # Add a function with different types of arguments
    source_code += textwrap.dedent(
        f"""
        def {mock_generator.function_name}_with_args(pos_arg, kw_arg=None, *args, **kwargs):
            pass
        """
    )
    module_obj = ast.parse(source_code)
    function_obj = find_syntax_tree_node(
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
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True
    )
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
    class_obj = find_syntax_tree_node(
        module_obj, f"{mock_generator.class_name}_extended"
    )
    assert (
        len(class_obj.body) == 4
    )  # class_attribute, method_1, method_2, some_property


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
    class_obj = find_syntax_tree_node(
        module_obj, f"{mock_generator.class_name}_child"
    )
    assert class_obj.bases[0].id == mock_generator.class_name


def test_reduce_module_remove_function(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True,
        has_class_docstring=True,
        has_function=True,
        has_function_docstring=True,
    )
    source_code = mock_generator.generate_code()

    module_obj = ast.parse(source_code)
    assert len(module_obj.body) == 2
    py_writer.create_new_module("test_module_2", module_obj)

    class_obj = module_obj.body[0]
    function_obj = ast.Module(body=[module_obj.body[1]], type_ignores=[])
    py_writer.delete_from_module(module_obj, function_obj)
    module_obj = py_module_loader.fetch_ast_module("test_module_2")
    assert module_obj.body[0] == class_obj
    assert len(module_obj.body) == 1


def test_update_existing_function(py_writer):
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    # Create a new config of the function with a different body
    source_code_updated = textwrap.dedent(
        f"""
        def {mock_generator.function_name}():
            return "Updated"
        """
    )
    py_writer.create_new_module("sample_module_2", ast.parse(source_code))
    module_obj = py_module_loader.fetch_ast_module("sample_module_2")
    py_writer.upsert_to_module(module_obj, ast.parse(source_code_updated))
    assert len(module_obj.body) == 1
    assert isinstance(module_obj.body[0], ast.FunctionDef)


def test_write_and_retrieve_mock_code(py_writer):
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
    py_writer.create_new_module("sample_module_2", ast.parse(source_code))

    retriever = PyReader()
    module_docstring = retriever.get_docstring("sample_module_2", None)
    assert module_docstring == mock_generator.module_docstring


def test_create_new_module(py_writer):
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("test_module_3", ast.parse(source_code))
    module_obj = py_module_loader.fetch_ast_module("test_module_3")
    assert module_obj is not None
    with pytest.raises(PyCodeWriter.InvalidArguments):
        py_writer.create_new_module("test_module_3", ast.parse(source_code))


def test_write_module_to_disk(py_writer):
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("test_module_4", ast.parse(source_code))
    py_writer.write_module_to_disk("test_module_4")
    assert os.path.exists(
        os.path.join(py_module_loader.root_fpath, "test_module_4.py")
    )
    py_writer.delete_module("test_module_4")
    with pytest.raises(PyCodeWriter.ModuleNotFound):
        py_writer.write_module_to_disk("non_existent_module")


def test_write_to_disk_and_format(py_writer):
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    module_fpath = os.path.join(
        py_module_loader.root_fpath, "test_module_5.py"
    )
    py_writer.create_new_module("test_module_5", ast.parse(source_code))
    py_writer._write_to_disk_and_format(module_fpath, source_code)
    with open(module_fpath, "r") as f:
        content = f.read()
    py_writer.delete_module("test_module_5")

    assert content.strip().replace("\n", "") == source_code.strip().replace(
        "\n", ""
    )


def test_upsert_to_module_update_existing_nodes(py_writer):
    # Arrange
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("test_module_update", ast.parse(source_code))

    # Modify the function and create a new ast module with the modified function
    source_code_modified = source_code.replace("pass", 'return "Updated"')
    module_modified = ast.parse(source_code_modified)

    # Act: Update the existing module with the modified function
    module = py_module_loader.fetch_ast_module("test_module_update")
    py_writer.upsert_to_module(module, module_modified)

    # Assert: Check if the function is updated correctly
    module_updated = py_module_loader.fetch_ast_module("test_module_update")
    function_node = module_updated.body[
        0
    ]  # assuming function is the first node in the module
    assert isinstance(function_node, ast.FunctionDef)
    assert isinstance(function_node.body[0], ast.Return)
    assert function_node.body[0].value.s == "Updated"


def test_delete_from_module_non_existent_node(py_writer):
    # Arrange
    mock_generator = MockCodeGenerator(has_function=True)
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("test_module_delete", ast.parse(source_code))

    # Create an AST module with a non-existent function
    non_existent_function_code = "def non_existent_function(): pass"
    deletion_module = ast.parse(non_existent_function_code)

    # Act & Assert: Attempt to delete a non-existent node should raise an exception
    module = py_module_loader.fetch_ast_module("test_module_delete")
    with pytest.raises(PyCodeWriter.StatementNotFound):
        py_writer.delete_from_module(module, deletion_module)


def test_delete_module_non_existent_module(py_writer):
    # Act & Assert: Attempt to delete a non-existent module should raise an exception
    with pytest.raises(PyCodeWriter.InvalidArguments):
        py_writer.delete_module("non_existent_module")
