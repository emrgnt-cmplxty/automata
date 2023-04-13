import textwrap

# New Module Test Data
NEW_PACKAGE_PY_PATH = "new_sample_code"
NEW_MODULE_NAME = "new_sample"
NEW_MODULE_PY_PATH = f"{NEW_PACKAGE_PY_PATH}.{NEW_MODULE_NAME}"
NEW_FUNCTION_NAME = "new_function"
NEW_FUNCTION_PY_PATH = f"{NEW_MODULE_PY_PATH}.{NEW_FUNCTION_NAME}"

NEW_MODULE_CODE = textwrap.dedent(
    '''
    """This module defines a new function."""
    
    def new_function():
        """Returns a string that says 'New function!'"""
        return 'New function!'
    '''
)

NEW_FUNCTION_RAW_CODE = f"""def {NEW_FUNCTION_NAME}():\n    return 'New function!'"""
NEW_MODULE_DOCSTRING = f"{NEW_MODULE_NAME}:\nThis module defines a new function."
NEW_FUNCTION_DOCSTRING = f"{NEW_FUNCTION_NAME}:\nReturns a string that says 'New function!'"

# Old Module Test Data
OLD_PACKAGE_PY_PATH = "sample_code"
OLD_MODULE_NAME = "sample"
OLD_MODULE_PY_PATH = f"{OLD_PACKAGE_PY_PATH}.{OLD_MODULE_NAME}"

# Class Test Data
CLASS_NAME = "NewClass"
CLASS_PY_PATH = f"{NEW_MODULE_PY_PATH}.{CLASS_NAME}"

CLASS_CODE = textwrap.dedent(
    '''
    class NewClass:
        """ This is a new class. """
       
        def __init__(self, name):
            """ This is the constructor. """
            self.name = name
            
        def say_hello(self):
            return f"Hello, I am {self.name}."
    '''
)

CLASS_RAW_CODE = textwrap.dedent(
    f"""
    class NewClass:
        def __init__(self, name):
            self.name = name
            
        def say_hello(self):
            return f'Hello, I am {{self.name}}.'
    """
)

CLASS_MODULE_CODE = textwrap.dedent(
    '''
    class NewClass:
        """ This is a new class. """
       
        def __init__(self, name):
            """ This is the constructor. """
            self.name = name
            
        def say_hello(self):
            return f"Hello, I am {self.name}."
    '''
)

# Group test data into dictionaries
new_module_data = {
    "package_py_path": NEW_PACKAGE_PY_PATH,
    "module_name": NEW_MODULE_NAME,
    "module_py_path": NEW_MODULE_PY_PATH,
    "function_name": NEW_FUNCTION_NAME,
    "function_py_path": NEW_FUNCTION_PY_PATH,
    "module_code": NEW_MODULE_CODE,
    "function_raw_code": NEW_FUNCTION_RAW_CODE,
    "module_docstring": NEW_MODULE_DOCSTRING,
    "function_docstring": NEW_FUNCTION_DOCSTRING,
}

old_module_data = {
    "package_py_path": OLD_PACKAGE_PY_PATH,
    "module_name": OLD_MODULE_NAME,
    "module_py_path": OLD_MODULE_PY_PATH,
}

class_data = {
    "class_name": CLASS_NAME,
    "class_py_path": CLASS_PY_PATH,
    "class_code": CLASS_CODE,
    "class_raw_code": CLASS_RAW_CODE,
    "class_module_code": CLASS_MODULE_CODE,
}

# Module with Class and Function Test Data
MODULE_WITH_CLASS_AND_FUNCTION_NAME = "module_with_class_and_function"
MODULE_WITH_CLASS_AND_FUNCTION_PY_PATH = (
    f"{NEW_PACKAGE_PY_PATH}.{MODULE_WITH_CLASS_AND_FUNCTION_NAME}"
)

MODULE_WITH_CLASS_AND_FUNCTION_CODE = textwrap.dedent(
    f"""
    class {CLASS_NAME}:
        def __init__(self, name):
            self.name = name
            
        def say_hello(self):
            return f'Hello, I am {{self.name}}.'
    
    def {NEW_FUNCTION_NAME}():
        return 'New function!'
    """
)

module_with_class_and_function_data = {
    "module_name": MODULE_WITH_CLASS_AND_FUNCTION_NAME,
    "module_py_path": MODULE_WITH_CLASS_AND_FUNCTION_PY_PATH,
    "module_code": MODULE_WITH_CLASS_AND_FUNCTION_CODE,
}
