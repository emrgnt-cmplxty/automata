from typing import List, Optional

from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

from spork.tools.codebase_oracle_tool import CodebaseOracleToolBuilder
from spork.tools.text_editor.edit_instructions_compiler_tool import EditInstructionsCompilerTool
from spork.tools.text_editor.edit_instructions_executor_tool import EditInstructionsExecutorTool


def make_text_editor_agent(
    llm: BaseLLM, memory: ReadOnlySharedMemory, home_dir: str, callbacks: Optional[List] = None
) -> AgentExecutor:
    """Create a text editor agent."""
    codebase_oracle_tool = CodebaseOracleToolBuilder(home_dir, llm, memory).build()
    compiler_tool = EditInstructionsCompilerTool(llm, memory)
    executor_tool = EditInstructionsExecutorTool(
        callbacks
    )  # the idea here is that editor changes the file, so it should call a callback for the codebase oracle to update its state
    tools = [codebase_oracle_tool, compiler_tool, executor_tool]
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
        "You are a text editor agent. You help other agents edit and save files. Other LLM agents call you to do editing tasks. "
        "You perform these tasks with your given tools by finding the correct files,"
        f"compiling changes into edit instructions and then executing them on the right files. Your current task is: {instructions}"
        "You should use codebase oracle repeatedly to ask better questions that help you with your objective. "
        "When you're ready, you should use the edit instructions compiler tool to compile your instructions into edit commands."
        "ALWAYS end by using the edit executor tool to apply your edit commands to the file."
        "If you see an Error, you should try to ask the codebase oracle tool for more context before retrying."
    )
    return task
