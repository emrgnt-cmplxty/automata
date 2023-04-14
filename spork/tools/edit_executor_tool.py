from langchain.agents import Tool

from spork.tools.simple_text_editor import SimpleTextEditor


class EditInstructionsExecutorTool(Tool):
    def __init__(self):
        editor = SimpleTextEditor()
        super().__init__(
            name="Edit Executor Tool",
            func=lambda input_str: self.try_edit(editor, input_str),
            description="Use it to execute compiled edit instructions on the file. "
            "The input should be a perfectly formatted string of instructions from compiler",
        )

    def try_edit(self, editor: SimpleTextEditor, input_str: str) -> str:
        try:
            editor.reset()
            return editor.execute_commands(input_str)
        except Exception as e:
            return f"Error: {e}"
