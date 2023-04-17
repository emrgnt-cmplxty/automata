from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

from spork.tools.oracles.documentation_oracle import DocumentationOracleTool

URL = "https://python.langchain.com/en/latest/"


class LangchainDocumentationOracleTool(DocumentationOracleTool):
    def __init__(self, llm: BaseLLM, memory: ReadOnlySharedMemory):
        super().__init__(
            llm=llm,
            memory=memory,
            url=URL,
            name="Langchain Documentation Oracle",
            description="Use this tool to ask questions about langchain works and how to use it. "
            "You can ask about chains, tools, agents, memory, and other abstractions that langchain provides. "
            "You can also ask for code examples. Input should be a fully formed question.",
        )
