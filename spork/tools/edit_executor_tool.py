from langchain.agents import Tool

from spork.tools.simple_text_editor import SimpleTextEditor


class EditExecutorTool(Tool):
    def __init__(self):
        editor = SimpleTextEditor()
        super().__init__(
            name="Edit Executor Tool",
            func=editor.execute_commands,
            description="Use it to execute compiled edit instructions on the file. "
            "The input should be a perfectly formatted string of instructions from compiler",
        )
