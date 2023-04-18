import logging
from typing import Dict, List, Tuple, cast

from langchain.agents import Tool

from spork.tools.documentation_tools.documentation_gpt import DocumentationGPT
from spork.tools.oracle.codebase_oracle import CodebaseOracle
from spork.tools.python_tools import PythonParser, PythonWriter
from spork.tools.tool_managers import (
    CodebaseOracleToolManager,
    DocumentationGPTToolManager,
    PythonParserToolManager,
    PythonWriterToolManager,
    build_tools,
)
from spork.tools.tool_managers.base_tool_manager import BaseToolManager


# TODO - Build a Tool enumeration for cleanliness
def load_llm_tools(
    tool_list: List[str], inputs: Dict[str, str], logger: logging.Logger
) -> Tuple[Dict[str, BaseToolManager], List[Tool]]:
    payload: Dict[str, BaseToolManager] = {}
    if "python_parser" in tool_list:
        python_parser = PythonParser()
        payload["python_parser"] = cast(BaseToolManager, python_parser)
    if "python_writer" in tool_list:
        assert "python_parser" in payload
        payload["python_writer"] = cast(BaseToolManager, PythonWriter(python_parser))
    if "codebase_oracle" in tool_list:
        payload["codebase_oracle"] = cast(
            BaseToolManager, CodebaseOracle.get_default_codebase_oracle()
        )
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
        if tool_name == "python_parser":
            exec_tools += build_tools(
                PythonParserToolManager(cast(PythonParser, payload["python_parser"]))
            )
        elif tool_name == "python_writer":
            exec_tools += build_tools(
                PythonWriterToolManager(cast(PythonWriter, payload["python_writer"]))
            )
        elif tool_name == "codebase_oracle":
            exec_tools += build_tools(
                CodebaseOracleToolManager(
                    cast(CodebaseOracle, payload["codebase_oracle"]),
                )
            )
        elif tool_name == "documentation_gpt":
            exec_tools += build_tools(
                DocumentationGPTToolManager(
                    cast(
                        DocumentationGPT,
                        (payload["documentation_gpt"]),
                    )
                )
            )
        else:
            logger.warning("Unknown tool: %s", tool_name)
    return payload, exec_tools
