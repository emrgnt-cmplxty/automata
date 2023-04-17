import itertools
import random
import string

import pytest

from spork.tools.python_tools.python_parser import PythonParser
from spork.tools.python_tools.python_writer import PythonWriter


class MockCodeGenerator:
    def __init__(self):
        self.class_name = MockCodeGenerator.random_string(5)
        self.function_name = MockCodeGenerator.random_string(5)
        self.module_docstring = MockCodeGenerator.random_string(20)
        self.module_class_docstring = MockCodeGenerator.random_string(20)
        self.function_docstring = MockCodeGenerator.random_string(20)

    def generate_code(
        self,
        has_class: bool = False,
        has_function: bool = False,
        has_class_docstring: bool = False,
        has_function_docstring: bool = False,
        has_module_docstring: bool = False,
    ):
        if not has_class:
            has_class_docstring = False
        if not has_function:
            has_function_docstring = False

        module_class_docstring = (
            f'"""{self.module_class_docstring}"""\n' if has_class_docstring else ""
        )

        class_code = (
            f'''class {self.class_name}:
                {module_class_docstring}
                def method(self):
                    """ This is a method """
                    pass'''
            if has_class
            else ""
        )

        module_docstring = f'"""{self.module_docstring}"""\n' if has_module_docstring else ""
        function_docstring_code = (
            f'"""{self.function_docstring}"""\n' if has_function_docstring else ""
        )
        function_code = (
            f"def {self.function_name}():\n    {function_docstring_code}\n    pass"
            if has_function
            else ""
        )

        return f"{module_docstring}{class_code}\n\n{function_code}"

    @staticmethod
    def random_string(length: int):
        return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.fixture
def python_writer():
    python_parser = PythonParser(
        relative_dir=f"spork/tools/python_tools/tests/{MockCodeGenerator.random_string(5)}"
    )
    return PythonWriter(python_parser)


@pytest.fixture
def python_new_writer():
    python_parser = PythonParser(
        relative_dir=f"spork/tools/python_tools/tests/{MockCodeGenerator.random_string(5)}"
    )
    return PythonWriter(python_parser)


@pytest.fixture
def mock_generator():
    return MockCodeGenerator()


def generate_code():
    all_permutations = list(itertools.product([True, False], repeat=5))
    mock_codes = []

    for (
        has_class,
        has_function,
        has_class_docstring,
        has_function_docstring,
        has_module_docstring,
    ) in all_permutations:
        if not has_class and not has_function:
            continue
        generator = MockCodeGenerator()
        code = generator.generate_code(
            has_class,
            has_function,
            has_class_docstring,
            has_function_docstring,
            has_module_docstring,
        )
        mock_codes.append([generator, code])

    return mock_codes


if __name__ == "__main__":
    all_mock_codes = generate_code()
    for idx, mock_code in enumerate(all_mock_codes, start=1):
        print(f"Mock Code {idx}:\n{mock_code}\n")

EXISTING_MODULE_PATH = "sample_code.sample"
NEW_MODULE_PATH = "sample_code.new_sample"


def test_create_new_module(python_writer, mock_generator):
    mock_code = mock_generator.generate_code(True, True, True, True)
    python_writer._create_new_module(
        NEW_MODULE_PATH,
        mock_code,
    )
    parser = python_writer.python_parser
    assert NEW_MODULE_PATH in parser.module_dict
    assert (
        f"{NEW_MODULE_PATH}.{mock_generator.class_name}"
        in parser.module_dict[NEW_MODULE_PATH].classes
    )


# Test the modify_code_state method with all permutations of the MockCodeGenerator
def test_modify_code_state(python_writer, mock_generator):
    for permutation in list(itertools.product([True, False], repeat=5)):
        (
            has_class,
            has_function,
            has_class_docstring,
            has_function_docstring,
            has_module_docstring,
        ) = permutation
        mock_code = mock_generator.generate_code(*permutation)
        parser = python_writer.python_parser
        result = python_writer.modify_code_state(NEW_MODULE_PATH, mock_code)

        module_obj = parser.module_dict[NEW_MODULE_PATH]

        class_name = f"{NEW_MODULE_PATH}.{mock_generator.class_name}"
        class_obj = module_obj.classes.get(class_name) if module_obj else None
        method_name = f"{NEW_MODULE_PATH}.{mock_generator.class_name}.method"
        method_obj = class_obj.methods.get(method_name)

        function_name = f"{NEW_MODULE_PATH}.{mock_generator.function_name}"
        function_obj = module_obj.standalone_functions.get(function_name)

        if has_module_docstring and not has_class_docstring and not has_function_docstring:
            module_name = NEW_MODULE_PATH.split(".")[-1]
            module_docstring = f"{module_name}:\n{mock_generator.module_docstring}\n{mock_generator.class_name}:\n{mock_generator.module_class_docstring}"
            assert module_obj.get_docstring().strip() == module_docstring

        if has_class:
            assert module_obj is not None
            assert class_obj is not None
            assert method_obj is not None

        if has_function:
            assert function_obj is not None

        if has_class and has_class_docstring:
            assert (
                class_obj.get_docstring().strip()
                == f"{mock_generator.class_name}:\n{mock_generator.module_class_docstring}\nmethod:\nThis is a method".strip()
            )
        function_single_name = mock_generator.function_name.split(".")[-1]
        if has_function and has_function_docstring:
            assert (
                function_obj.get_docstring().strip()
                == f"{function_single_name}:\n{mock_generator.function_docstring}".strip()
            )

        assert result == "Success"
