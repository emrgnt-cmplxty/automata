from typing import List

from langchain.agents import Tool

from spork.tools.documentation_tools.documentation_gpt import DocumentationGPT
from spork.tools.tool_managers.base_tool_manager import BaseToolManager


class DocumentationGPTToolManager(BaseToolManager):
    def __init__(self, documentation_gpt: DocumentationGPT):
        self.documentation_gpt = documentation_gpt

    def build_tools(self):
        tools = [
            Tool(
                name="doc-gpt-lookup",
                func=lambda input_str: self.documentation_gpt_lookup(input_str),
                description="Vector search over the specified API documentation.",
                return_direct=False,
            ),
        ]
        return tools

    def documentation_gpt_lookup(self, input_text):
        result = self.documentation_gpt.run(input_text)
        return result

    def build_tools_with_meeseeks(self) -> List[Tool]:
        return []
