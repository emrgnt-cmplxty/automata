import inspect
import os
import shutil
import textwrap

import pytest
from test_data import (
    class_data,
    module_with_class_and_function_data,
    new_module_data,
    old_module_data,
)

from spork.tools.python_tools.python_parser import PythonParser
from spork.tools.python_tools.python_writer import PythonWriter


@pytest.fixture
def python_writer():
    python_parser = PythonParser(
        relative_dir=f"spork/tools/python_tools/tests/{old_module_data['package_py_path']}"
    )
    return PythonWriter(python_parser)


@pytest.fixture
def python_new_writer():
    python_parser = PythonParser(
        relative_dir=f"spork/tools/python_tools/tests/{new_module_data['package_py_path']}"
    )
    return PythonWriter(python_parser)


def test_add_old_module_no_existing_package(python_writer):
    with pytest.raises(AssertionError):
        python_writer._create_new_module(
            old_module_data["module_py_path"], new_module_data["module_code"]
        )


def test_create_new_module_old_writer(python_writer):
    python_writer._create_new_module(
        new_module_data["module_py_path"], new_module_data["module_code"]
    )
    parser = python_writer.python_parser

    assert new_module_data["package_py_path"] in parser.package_dict
    assert new_module_data["module_py_path"] in parser.module_dict
    assert new_module_data["function_py_path"] in parser.function_dict
    assert list(parser.class_dict.keys()) == ["sample_code.sample.Person"]
    assert list(parser.package_dict.keys()) == ["sample_code", "new_sample_code"]
    assert (
        parser.get_raw_code(new_module_data["module_py_path"]).strip()
        == new_module_data["function_raw_code"]
    )
    assert (
        parser.get_docstring(new_module_data["module_py_path"])
        == new_module_data["module_docstring"]
    )
    assert (
        parser.get_raw_code(new_module_data["function_py_path"])
        == new_module_data["function_raw_code"]
    )
    assert (
        parser.get_docstring(new_module_data["function_py_path"])
        == new_module_data["function_docstring"]
    )
    assert (
        parser.get_docstring(new_module_data["package_py_path"])
        == new_module_data["module_docstring"]
    )


def test_create_new_module_new_writer(python_new_writer):
    python_new_writer._create_new_module(
        new_module_data["module_py_path"], new_module_data["module_code"]
    )
    parser = python_new_writer.python_parser

    assert new_module_data["package_py_path"] in parser.package_dict
    assert new_module_data["module_py_path"] in parser.module_dict
    assert new_module_data["function_py_path"] in parser.function_dict
    assert list(parser.class_dict.keys()) == []
    assert list(parser.package_dict.keys()) == ["new_sample_code"]
    assert (
        parser.get_raw_code(new_module_data["module_py_path"]).strip()
        == new_module_data["function_raw_code"]
    )
    assert (
        parser.get_docstring(new_module_data["module_py_path"])
        == new_module_data["module_docstring"]
    )
    assert (
        parser.get_raw_code(new_module_data["function_py_path"])
        == new_module_data["function_raw_code"]
    )
    assert (
        parser.get_docstring(new_module_data["function_py_path"])
        == new_module_data["function_docstring"]
    )
    assert (
        parser.get_docstring(new_module_data["package_py_path"])
        == new_module_data["module_docstring"]
    )


def test_create_new_class_no_existing_module(python_writer):
    with pytest.raises(AssertionError):
        python_writer._create_new_class(
            new_module_data["module_py_path"],
            class_data["class_py_path"],
            class_data["class_code"],
        )


def test_create_new_class_new_writer(python_new_writer):
    parser = python_new_writer.python_parser
    print("parser.module_dict = ", parser.module_dict)
    python_new_writer._create_new_class(
        new_module_data["module_py_path"],
        class_data["class_py_path"],
        class_data["class_code"],
        module_code=class_data["class_module_code"],
    )
    parser = python_new_writer.python_parser

    assert new_module_data["package_py_path"] in parser.package_dict
    assert new_module_data["module_py_path"] in parser.module_dict
    assert class_data["class_py_path"] in parser.class_dict
    assert f"{class_data['class_py_path']}.say_hello" in parser.function_dict
    assert parser.get_raw_code(class_data["class_py_path"]).replace(" ", "").replace(
        "\n", ""
    ) == class_data["class_raw_code"].replace(" ", "").replace("\n", "")


def test_create_new_class(python_writer):
    python_writer._create_new_class(
        old_module_data["module_py_path"],
        class_data["class_py_path"],
        class_data["class_code"],
        module_code=class_data["class_module_code"],
    )
    parser = python_writer.python_parser
    assert class_data["class_py_path"] in parser.class_dict
    assert parser.get_raw_code(class_data["class_py_path"]).replace(" ", "").replace(
        "\n", ""
    ) == class_data["class_raw_code"].replace(" ", "").replace("\n", "")


def test_add_module_with_class_and_function(python_writer):
    python_writer._create_new_module(
        module_with_class_and_function_data["module_py_path"],
        module_with_class_and_function_data["module_code"],
    )
    parser = python_writer.python_parser

    assert module_with_class_and_function_data["module_py_path"] in parser.module_dict
    assert (
        f"{module_with_class_and_function_data['module_py_path']}.{class_data['class_name']}"
        in parser.class_dict
    )
    assert (
        f"{module_with_class_and_function_data['module_py_path']}.{new_module_data['function_name']}"
        in parser.function_dict
    )


def test_create_new_function_existing_module(python_writer):
    # Add the test module
    module_py_path = new_module_data["module_py_path"]
    python_writer._create_new_module(
        module_py_path=module_py_path,
        module_code=new_module_data["module_code"],
    )

    # Add a new function to the module
    function_name = new_module_data["function_name"]
    function_docstring = "New function docstring"
    new_function_code = textwrap.dedent(
        f'''
        def {function_name}():
            """{function_docstring}"""
            return 'New function!'
        '''
    )

    python_writer._create_new_function(
        function_py_path=f"{module_py_path}.{function_name}",
        function_code=new_function_code,
        has_class=False,
    )

    # Check if the function is added to the function_dict
    new_function_obj = python_writer.python_parser.function_dict[
        f"{module_py_path}.{function_name}"
    ]
    assert new_function_obj.get_raw_code() == f"def {function_name}():\n    return 'New function!'"
    assert new_function_obj.get_docstring() == f"{function_name}:\n{function_docstring}"


def test_modify_existing_function(python_writer):
    # Add the test module with a class and a function
    module_py_path = module_with_class_and_function_data["module_py_path"]
    function_name = new_module_data["function_name"]

    python_writer._create_new_module(
        module_py_path=module_py_path,
        module_code=module_with_class_and_function_data["module_code"],
    )

    # Modify the existing function
    function_name = new_module_data["function_name"]
    function_docstring = "Modified new function docstring"
    modified_function_code = textwrap.dedent(
        f'''
        def {function_name}():
            """{function_docstring}"""
            return 'Modified new function!'
        '''
    )

    python_writer._modify_existing_function(
        function_py_path=f"{module_py_path}.{function_name}",
        function_code=modified_function_code,
    )
    modified_function_raw_code = f"def {function_name}():\n    return 'Modified new function!'"

    # Check if the function is modified in the function_dict
    modified_function_obj = python_writer.python_parser.function_dict[
        f"{module_py_path}.{function_name}"
    ]
    assert modified_function_obj.get_raw_code() == modified_function_raw_code
    assert modified_function_obj.get_docstring() == f"{function_name}:\n{function_docstring}"


def test_modify_existing_class(python_writer):
    # Add the test module with a class and a function
    module_py_path = module_with_class_and_function_data["module_py_path"]
    class_name = class_data["class_name"]

    python_writer._create_new_module(
        module_py_path=module_py_path,
        module_code=module_with_class_and_function_data["module_code"],
    )

    # Modify the existing class
    class_docstring = "Modified class docstring"
    modified_class_code = textwrap.dedent(
        f'''
        class {class_name}:
            """{class_docstring}"""
            def modified_class_method(self):
                """Modified class method docstring"""
                return "Modified class method"
        '''
    )

    python_writer._modify_existing_class(
        class_py_path=f"{module_py_path}.{class_name}",
        class_code=modified_class_code,
    )

    # Check if the class is modified in the class_dict
    modified_class_obj = python_writer.python_parser.class_dict[f"{module_py_path}.{class_name}"]
    assert (
        modified_class_obj.get_docstring()
        == f"{class_name}:\n{class_docstring}\nmodified_class_method:\nModified class method docstring"
    )
    assert (
        modified_class_obj.get_docstring(exclude_methods=True)
        == f"{class_name}:\n{class_docstring}"
    )

    assert (
        "new_sample_code.module_with_class_and_function.NewClass.modified_class_method"
        in modified_class_obj.methods
    )


def test_modify_code_state_create_new_function(python_writer):
    old_module_path = old_module_data["module_py_path"]
    new_function_name = new_module_data["function_name"]
    new_path = f"{old_module_path}.{new_function_name}"
    python_writer.modify_code_state(new_path, new_module_data["function_code"])

    parser = python_writer.python_parser
    assert new_path in parser.function_dict
    assert parser.get_raw_code(new_path).replace(" ", "").replace("\n", "") == new_module_data[
        "function_raw_code"
    ].replace(" ", "").replace("\n", "")
    assert parser.get_docstring(new_path).replace(" ", "").replace("\n", "") == new_module_data[
        "function_docstring"
    ].replace(" ", "").replace("\n", "")


def test_modify_code_state_create_new_class(python_writer):
    old_module_path = old_module_data["module_py_path"]
    new_class_name = class_data["class_name"]
    new_path = f"{old_module_path}.{new_class_name}"
    python_writer.modify_code_state(new_path, class_data["class_code"])

    parser = python_writer.python_parser
    assert new_path in parser.class_dict
    assert parser.get_raw_code(new_path).replace(" ", "").replace("\n", "") == class_data[
        "class_raw_code"
    ].replace(" ", "").replace("\n", "")
    assert parser.get_docstring(new_path).replace(" ", "").replace("\n", "") == class_data[
        "class_docstring"
    ].replace(" ", "").replace("\n", "")


def test_modify_code_state_create_new_module(python_writer):
    python_writer.modify_code_state(
        new_module_data["module_py_path"], new_module_data["module_code"]
    )

    parser = python_writer.python_parser
    assert new_module_data["module_py_path"] in parser.module_dict


def test_modify_code_state_create_new_package(python_writer):
    package_path = new_module_data["package_py_path"]
    python_writer.modify_code_state(f"{package_path}.__init__", "")

    parser = python_writer.python_parser
    assert f"{package_path}.__init__" in parser.package_dict


# TODO - Why is this test not creating an __init__.py in the new package?
def test_write_new_package(python_writer):
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])

    prev_text = None
    with open(os.path.join(absolute_path, "sample_code", "sample.py"), "r", encoding="utf-8") as f:
        prev_text = f.read()

    python_writer.modify_code_state(
        new_module_data["module_py_path"], new_module_data["module_code"]
    )
    # Write the changes to disk and ensure the file exists.
    python_writer.write_to_disk()
    new_file_path = os.path.join(
        absolute_path, new_module_data["package_py_path"], new_module_data["module_name"]
    )

    assert new_module_data["module_py_path"] in python_writer.python_parser.module_dict

    assert os.path.isfile(f"{new_file_path}.py")

    # Clean up after the check
    shutil.rmtree(os.sep.join(new_file_path.split(os.sep)[:-1]), ignore_errors=True)

    with open(os.path.join(absolute_path, "sample_code", "sample.py"), "r", encoding="utf-8") as f:
        new_text = f.read()
    # Check that the original sample.py has not been modified by the recreation process.
    assert prev_text == new_text
