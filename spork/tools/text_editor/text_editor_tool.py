from langchain.agents import AgentExecutor, Tool

from spork.agents.text_editor_agent import make_text_editor_task


class TextEditorTool(Tool):
    def __init__(self, text_editor_agent: AgentExecutor):
        super().__init__(
            name="Text Editor Tool",
            func=lambda x: text_editor_agent.run(make_text_editor_task(x)),
            description="This tool is a text editor agent that takes instructions and edits a file. "
            "The instructions should be a fully formed request to edit a SINGLE file at a time. For example: Rename the variable x to y in file foo.py;"
            "Add a print statement on line 64 of bar.sh; Delete the try-except block around 12 of baz.py.",
        )
