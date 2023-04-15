from typing import List, Optional

from langchain.agents import Tool

from spork.tools.simple_text_editor import SimpleTextEditor


class EditInstructionsExecutorTool(Tool):
    def __init__(self, callbacks: Optional[List]):
        editor = SimpleTextEditor()
        super().__init__(
            name="Edit Executor Tool",
            func=lambda input_str: self.try_edit(input_str, editor, callbacks),
            description="Use it to execute compiled edit instructions on the file. "
            "The input should be a perfectly formatted string of instructions from compiler",
        )

    def try_edit(self, input_str: str, editor: SimpleTextEditor, callbacks: Optional[List]) -> str:
        try:
            editor.reset()
            result = editor.execute_commands(input_str)
            if callbacks:
                for callback in callbacks:
                    callback()
            return result
        except Exception as e:
            return f"Error: {e}"
