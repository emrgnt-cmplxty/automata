import logging
import os
from typing import Dict, List, Tuple, cast

from langchain.agents import Tool

from spork.tools.documentation_tools.documentation_gpt import DocumentationGPT
from spork.tools.oracle.codebase_oracle import CodebaseOracle
from spork.tools.python_tools import PythonIndexer, PythonWriter
from spork.tools.tool_managers import (
    CodebaseOracleToolManager,
    DocumentationGPTToolManager,
    PythonIndexerToolManager,
    PythonWriterToolManager,
    build_tools,
)
from spork.tools.tool_managers.base_tool_manager import BaseToolManager
from spork.tools.utils import home_path


# TODO - Build a Tool enumeration for cleanliness
def load_llm_tools(
    tool_list: List[str], inputs: Dict[str, str], logger: logging.Logger
) -> Tuple[Dict[str, BaseToolManager], List[Tool]]:
    payload: Dict[str, BaseToolManager] = {}
    if "python_indexer" in tool_list:
        python_writer = PythonIndexer(os.path.join(home_path(), "spork"))
        payload["python_indexer"] = python_writer
    if "python_manipulator" in tool_list:
        assert "python_writer" in payload
        payload["python_writer"] = PythonWriter(python_writer)
    if "codebase_oracle" in tool_list:
        payload["codebase_oracle"] = CodebaseOracle.get_default_codebase_oracle()
    if "doc_gpt" in tool_list:
        payload["doc_gpt"] = cast(
            BaseToolManager,
            DocumentationGPT(
                url=inputs["documentation_url"],
                model=inputs["model"],
                temperature=0.7,
                verbose=True,
            ),
        )

    exec_tools: List[Tool] = []
    for tool_name in payload.keys():
        tool_name = tool_name.strip()
        if tool_name == "python_indexer":
            exec_tools += build_tools(PythonIndexerToolManager(payload["python_indexer"]))
        elif tool_name == "python_writer":
            exec_tools += build_tools(PythonWriterToolManager(payload["python_writer"]))
        elif tool_name == "codebase_oracle":
            exec_tools += build_tools(CodebaseOracleToolManager(payload["codebase_oracle"]))
        elif tool_name == "documentation_gpt":
            exec_tools += build_tools(
                DocumentationGPTToolManager(
                    payload["documentation_gpt"],
                )
            )
        else:
            logger.warning("Unknown tool: %s", tool_name)
    return payload, exec_tools
