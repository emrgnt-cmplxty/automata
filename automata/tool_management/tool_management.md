# Automata Tool Managers Documentation

## Overview

This documentation covers various tool managers used by the AutomataAgent. These tool managers interact with different APIs and provide functionality to read and modify the code state of Python files, build low-level manipulation (LLM) toolkits, and facilitate code searches.

The primary tool managers discussed in this documentation include:

- `PythonWriterToolManager`: Interacts with the PythonWriter API to modify the code state of a given directory of Python files.
- `PythonIndexerToolManager`: Interacts with the PythonIndexer API to read the code state of local Python files.
- `CodebaseOracleToolManager`: Initializes a CodebaseOracle object to facilitate code searches.

Additionally, we cover `ToolManagerFactory` for creating tool managers, `ToolkitBuilder` for building tools from a tool manager, and `build_llm_toolkits` for loading specified tools.

## Usage

To use the tool managers, you will generally interact with the `ToolManagerFactory` to create the desired tool manager, use the `build_tools` method to build the tools, and then use the `build_llm_toolkits` function to load the tools.

## Examples

### Creating a PythonWriterToolManager

```python
from automata.tool_management.tool_management_utils import ToolManagerFactory
from automata.core.base.tool import ToolkitType

tool_manager = ToolManagerFactory.create_tool_manager(ToolkitType.PYTHON_WRITER, inputs={})
```

### Building Tools with ToolkitBuilder

```python
from automata.tool_management.tool_management_utils import ToolkitBuilder

builder = ToolkitBuilder()
tools = builder.build_tools(tool_manager)
```

### Loading LLM Toolkits

```python
from automata.tool_management.tool_management_utils import build_llm_toolkits

tool_list = ["python_writer", "python_inspector", "codebase_oracle"]
toolkits = build_llm_toolkits(tool_list)
```

## References

### PythonWriterToolManager

- `build_tools()`: Builds a list of Tool objects for interacting with the PythonWriter API.

### PythonIndexerToolManager

- `build_tools()`: Builds a list of Tool objects for interacting with the PythonIndexer API.

### CodebaseOracleToolManager

- `build_tools(codebase_oracle: CodebaseOracle)`: Initializes a CodebaseOracleToolManager object with the given inputs.

### ToolManagerFactory

- `create_tool_manager(toolkit_type: ToolkitType, inputs: dict) -> Optional[BaseToolManager]`: Creates a tool manager of the specified type with the provided inputs.

### ToolkitBuilder

- `build_tools(tool_manager: BaseToolManager) -> List[Tool]`: Builds tools from the given tool manager.

### build_llm_toolkits

- `build_llm_toolkits(tool_list: List[str], **kwargs) -> Dict[str, Tool]`: Loads the tools specified in the tool_list and returns a dictionary of the loaded tools. Raises a ValueError if an unknown tool is specified.
