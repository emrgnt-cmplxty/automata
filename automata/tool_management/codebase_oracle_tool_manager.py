from typing import List

from automata.core.base.tool import Tool
from automata.core.utils import run_retrieval_chain_with_sources_format
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.oracle.codebase_oracle import CodebaseOracle


class CodebaseOracleToolManager(BaseToolManager):
    def __init__(self, **kwargs):
        self.codebase_oracle = (
            kwargs.get("codebase_oracle") or CodebaseOracle.get_default_codebase_oracle()
        )

    def build_tools(self) -> List[Tool]:
        """
        Initializes a CodebaseOracleToolManager object with the given inputs.

        Args:
        - codebase_oracle (CodebaseOracle): A CodebaseOracle object which facilitates code searches.

        Returns:
        - None
        """
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

    def _run_codebase_oracle_agent(self, query: str) -> str:
        """Lookup the documentation for the given input text."""
        result = run_retrieval_chain_with_sources_format(self.codebase_oracle.get_chain(), query)
        return result
