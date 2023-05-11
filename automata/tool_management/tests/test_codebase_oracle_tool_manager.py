from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory

from automata.core.utils import root_path
from automata.tool_management.codebase_oracle_tool_manager import CodebaseOracleToolManager
from automata.tools.oracle.codebase_oracle import CodebaseOracle


class TestCodebaseOracleToolManager:
    def test_oracle_init(self):
        llm2 = ChatOpenAI(streaming=True, temperature=0, model_name="gpt-4")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        read_only_memory = ReadOnlySharedMemory(memory=memory)

        codebase_oracle = CodebaseOracle(root_path(), llm2, read_only_memory)
        codebase_oracle_tool_manager = CodebaseOracleToolManager(codebase_oracle=codebase_oracle)
        assert codebase_oracle_tool_manager.codebase_oracle == codebase_oracle

    def test_oracle_build_tools(self):
        llm2 = ChatOpenAI(streaming=True, temperature=0, model_name="gpt-4")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        read_only_memory = ReadOnlySharedMemory(memory=memory)

        codebase_oracle = CodebaseOracle(root_path(), llm2, read_only_memory)

        codebase_oracle_tool_manager = CodebaseOracleToolManager(codebase_oracle=codebase_oracle)
        tools = codebase_oracle_tool_manager.build_tools()
        assert len(tools) == 1
        assert tools[0].name == "codebase-oracle-agent"
        assert (
            tools[0].description
            == "Exposes the run command a codebase oracle, which conducts a semantic search on the code repository using natural language queries, and subsequently returns the results to the main"
        )
