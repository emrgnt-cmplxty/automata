# AutomataTools Documentation

## Overview

The AutomataTools provide capabilities to index, write, and search Python codebases. This documentation covers PythonIndexer, PythonWriter, and CodeBaseOracle classes, which are part of the AutomataTools.

## Usage

- PythonIndexer: Use this class to index Python source code files in a directory and retrieve code and docstrings.
- PythonWriter: A utility class to work with Python AST nodes.
- CodeBaseOracle: Provides methods to interact with other tools of the AutomataTools.

## Examples

### PythonIndexer

```python
from automata.tools.python_tools.python_inspector import PythonIndexer

indexer = PythonIndexer("/path/to/your/codebase")
code = indexer.retrieve_code("package.module", "ClassName.method_name")
docstring = indexer.retrieve_docstring("package.module", "ClassName.method_name")
```

### PythonWriter

```python
from automata.tools.python_tools.python_writer import PythonWriter
from automata.tools.python_tools.python_inspector import PythonIndexer

indexer = PythonIndexer("/path/to/your/codebase")
writer = PythonWriter(indexer)

# Update the module
updated_module = writer.update_module(
    source_code="def new_function():\n    pass",
    extending_module=True,
    module_path="package.module"
)

# Write the updated module to disk
writer._write_module_to_disk("output/package/module.py")
```

## References

### PythonIndexer

- `__init__(self, rel_path: str) -> None`: Initializes a PythonIndexer instance.
- `retrieve_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]`: Retrieve code for a specified module, class, or function/method.
- `retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> Optional[str]`: Retrieve the docstring for a specified module, class, or function/method.
- `find_expression_context(root_dir: str, expression: str) -> str`: Inspects the codebase for lines containing the expression and returns the line number and surrounding lines.
- `retrieve_raw_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]`: Retrieves the raw code for a specified module (code + docstring), class, or function/method.
- `get_module_path(self, module_obj: Module) -> str`: Returns the module path for the specified module object.
- `build_overview() -> str`: Loops over the PythonParser's dictionaries and returns a string that provides an overview of the PythonParser's state.
- `build_module_overview() -> str`: Loops over the module and returns a string that provides an overview of the Module.

### PythonWriter

- `update_module(source_code: str, extending_module: bool, module_obj: Optional[Module], module_path: Optional[str]) -> Module`: Perform an in-place extension or reduction of a module object according to the received code.
- `write_module(self, module_path: str) -> None`: Write the modified AST module to a file at the specified output path.

### CodeBaseOracle

- `refresh_callback()`: A method to refresh the codebase state.
- `get_chain()`: A method to retrieve the chain of tools.
- `get_default_codebase_oracle()`: A method to get the default codebase oracle.
- `NumberedLinesTextLoader.load()`: Load from file path.

## ToolManagerFactory

The ToolManagerFactory is a utility class that creates instances of tool managers, such as PythonIndexerToolManager, PythonWriterToolManager, and CodebaseOracleToolManager.

```python
from automata.tool_management.tool_management_utils import ToolManagerFactory
from automata.configs.config_enums import ToolkitType

tool_manager = ToolManagerFactory.create_tool_manager(ToolkitType.PYTHON_INDEXER, inputs)
```

## ToolkitBuilder

The ToolkitBuilder class is used to build and manage toolkits, such as PythonIndexer, PythonWriter, and CodeBaseOracle.

```python
from automata.tool_management.tool_management_utils import ToolkitBuilder

builder = ToolkitBuilder()
tool_management = builder._tool_management
```
