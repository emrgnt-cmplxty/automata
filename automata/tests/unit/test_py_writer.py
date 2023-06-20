import os
import random
import string
import textwrap

import pytest
from redbaron import (
    ClassNode,
    DefNode,
    EndlNode,
    PassNode,
    RedBaron,
    ReturnNode,
    StringNode,
)

from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap
from automata.core.coding.py_coding.navigation import find_syntax_tree_node
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.coding.py_coding.writer import PyCodeWriter


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
            function_obj = RedBaron(source_code).find("def")
        assert function_obj.name == self.function_name
        if self.has_function_docstring:
            assert function_obj[0].value.replace('"""', "") == self.function_docstring
            assert isinstance(function_obj[0], StringNode)
            assert isinstance(function_obj[1], EndlNode)
            assert isinstance(function_obj[2], PassNode)
        else:
            assert isinstance(function_obj[0], EndlNode)
            assert isinstance(function_obj[1], PassNode)

    def _check_class_obj(self, class_obj=None):
        if class_obj is None:
            source_code = self.generate_code()
            class_obj = RedBaron(source_code).find("class")

        assert class_obj.name == self.class_name
        if self.has_class_docstring:
            assert isinstance(class_obj, ClassNode)
            assert isinstance(class_obj[0], StringNode)
            assert isinstance(class_obj[1], EndlNode)
            assert isinstance(class_obj[2], DefNode)
        else:
            assert isinstance(class_obj, ClassNode)
            assert isinstance(class_obj[0], EndlNode)
            assert isinstance(class_obj[1], DefNode)

        if self.has_method:
            method_obj = class_obj[3] if self.has_class_docstring else class_obj[2]
            assert method_obj.name == "method"
            if self.has_method_docstring:
                assert isinstance(method_obj[0], StringNode)  # docstring
                assert isinstance(method_obj[1], EndlNode)  # pass
                assert isinstance(method_obj[2], PassNode)  # pass
            else:
                assert isinstance(method_obj[0], EndlNode)
                assert isinstance(method_obj[1], PassNode)

    def _check_module_obj(self, module_obj=None):
        if module_obj is None:
            source_code = self.generate_code()
            module_obj = RedBaron(source_code)
        if self.has_module_docstring:
            assert isinstance(module_obj[0], StringNode)
            assert isinstance(module_obj[1], ClassNode)
        else:
            if isinstance(module_obj[0], EndlNode):
                assert isinstance(module_obj[1], ClassNode)
            else:
                assert isinstance(module_obj[0], ClassNode)

    @staticmethod
    def random_string(length: int):
        return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.fixture
def py_writer():
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    module_map = LazyModuleTreeMap(sample_dir)
    retriever = PyCodeRetriever(module_map)
    return PyCodeWriter(retriever)


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


def test_extend_module(py_writer):
    # Arrange
    # create module
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("sample_module_22", source_code)
    mock_generator_2 = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code_2 = mock_generator_2.generate_code()

    py_writer.update_existing_module("sample_module_22", source_code_2)

    # Check module 2 is merged into module 1
    module_obj = py_writer.code_retriever.module_tree_map.fetch_module("sample_module_22")
    mock_generator._check_module_obj(module_obj)
    mock_generator._check_class_obj(module_obj[0])
    mock_generator._check_function_obj(module_obj[1])
    mock_generator_2._check_class_obj(module_obj[2])
    mock_generator_2._check_function_obj(module_obj[3])


def test_reduce_module(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("sample_module_2", source_code)
    module_obj = py_writer.code_retriever.module_tree_map.fetch_module("sample_module_2")
    class_obj = module_obj.find("class")

    function_obj = module_obj.find_all("def")[-1]
    py_writer.delete_from_existing__module("sample_module_2", class_obj.name)
    assert module_obj[0] == function_obj


def assert_code_lines_equal(code_1: str, code_2: str):
    code_1_lines = [line for line in code_1.splitlines() if line.strip()]
    code_2_lines = [line for line in code_2.splitlines() if line.strip()]
    assert all(line_1 == line_2 for line_1, line_2 in zip(code_1_lines, code_2_lines))


def test_create_update_write_module(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()
    py_writer.create_new_module("sample_module_write", source_code, do_write=True)
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    fpath = os.path.join(root_dir, "sample_module_write.py")
    assert os.path.exists(fpath)
    with open(fpath, "r") as f:
        contents = f.read()
        assert_code_lines_equal(source_code, contents)

    mock_generator_2 = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code_2 = mock_generator_2.generate_code()

    assert source_code != source_code_2
    py_writer.update_existing_module(
        source_code=source_code_2, module_dotpath="sample_module_write", do_write=True
    )

    with open(fpath, "r") as f:
        contents = f.read()
        assert_code_lines_equal("\n".join([source_code, source_code_2]), contents)

    os.remove(fpath)


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
    module_obj = RedBaron(source_code)
    function_obj = find_syntax_tree_node(module_obj, f"{mock_generator.function_name}_with_args")
    assert function_obj.name == f"{mock_generator.function_name}_with_args"
    def_arg_nodes = module_obj.find_all("def_argument")
    assert len(def_arg_nodes) == 2
    assert def_arg_nodes[0].name.value == "pos_arg"
    assert def_arg_nodes[1].name.value == "kw_arg"
    assert def_arg_nodes[1].value.value == "None"
    list_arg_nodes = module_obj.find_all("list_argument")
    assert len(list_arg_nodes) == 1
    assert list_arg_nodes[0].name.value == "args"
    dict_arg_nodes = module_obj.find_all("dict_argument")
    assert len(dict_arg_nodes) == 1
    assert dict_arg_nodes[0].name.value == "kwargs"


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
    module_obj = RedBaron(source_code)
    class_obj = find_syntax_tree_node(module_obj, f"{mock_generator.class_name}_extended")
    assert len(class_obj.filtered()) == 4  # class_attribute, method_1, method_2, some_property


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
    module_obj = RedBaron(source_code)
    class_obj = find_syntax_tree_node(module_obj, f"{mock_generator.class_name}_child")
    assert class_obj.inherit_from.name.value == mock_generator.class_name


def test_reduce_module_remove_function(py_writer):
    mock_generator = MockCodeGenerator(
        has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
    )
    source_code = mock_generator.generate_code()

    module_obj = py_writer._create_module_from_source_code("sample_module_2", source_code)
    class_obj = module_obj[1]
    function_obj = module_obj[2]

    py_writer.delete_from_existing__module("sample_module_2", function_obj.name)

    assert module_obj[0] == class_obj
    assert len(module_obj.filtered()) == 1


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
    module_obj = py_writer._create_module_from_source_code("sample_module_2", source_code)
    py_writer.update_existing_module(
        source_code=source_code_updated, module_dotpath="sample_module_2"
    )
    updated_function_obj = find_syntax_tree_node(module_obj, mock_generator.function_name)
    assert len(updated_function_obj) == 1
    assert isinstance(updated_function_obj[0], ReturnNode)


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
    py_writer._create_module_from_source_code("sample_module_2", source_code)

    py_writer._write_module_to_disk("sample_module_2")

    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    module_map = LazyModuleTreeMap(sample_dir)
    retriever = PyCodeRetriever(module_map)
    module_docstring = retriever.get_docstring("sample_module_2", None)
    assert module_docstring == mock_generator.module_docstring

    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    fpath = os.path.join(root_dir, "sample_module_2.py")
    os.remove(fpath)
