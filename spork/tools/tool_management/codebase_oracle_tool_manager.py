from typing import List

from spork.core.base.tool import Tool
from spork.core.utils import run_retrieval_chain_with_sources_format
from spork.tools.oracle.codebase_oracle import CodebaseOracle
from spork.tools.tool_management.base_tool_manager import BaseToolManager


class CodebaseOracleToolManager(BaseToolManager):
    def __init__(self, codebase_oracle: CodebaseOracle):
        self.codebase_oracle = codebase_oracle

    def build_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="codebase-oracle-agent",
                func=lambda query: self._run_codebase_oracle_agent(query),
                description="Exposes the run command a codebase oracle, which conducts a semantic search on the code repository using natural language queries, and subsequently returns the results to the master",
                return_direct=True,
                verbose=True,
            )
        ]
        return tools

    def build_tools_with_meeseeks(self) -> List[Tool]:
        raise NotImplementedError

    def _run_codebase_oracle_agent(self, query: str) -> str:
        result = run_retrieval_chain_with_sources_format(self.codebase_oracle.get_chain(), query)
        return result
