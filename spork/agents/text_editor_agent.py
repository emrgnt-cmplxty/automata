from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

from spork.tools.codebase_oracle_tool import CodebaseOracleToolBuilder
from spork.tools.diff_applier_tool import DiffApplierTool
from spork.tools.diff_writer_tool import DiffWriterTool

task = (
    "You are a text editor agent. Other LLM agents call you to do editing tasks on local files. You pefrom these tasks by finding the correct files,"
    "breaking down changes into diffs and then applying them to the right files. Your current task is: {task}"
)


def make_text_editor_agent(
    llm: BaseLLM, memory: ReadOnlySharedMemory, home_dir: str
) -> AgentExecutor:
    """Create a text editor agent."""
    codebase_oracle_tool = CodebaseOracleToolBuilder(home_dir, llm, memory).build()
    diff_writer_tool = DiffWriterTool(llm)
    diff_applier_tool = DiffApplierTool()
    tools = [codebase_oracle_tool, diff_writer_tool, diff_applier_tool]
    editor_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )
    return editor_agent


def make_text_editor_task(instructions: str) -> str:
    task = (
        "You are a text editor agent. Other LLM agents call you to do editing tasks on local files. You pefrom these tasks by finding the correct files,"
        f"breaking down changes into diffs and then applying them to the right files. Your current task is: {instructions}"
    )
    return task
