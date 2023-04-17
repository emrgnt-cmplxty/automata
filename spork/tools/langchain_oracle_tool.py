from langchain import FAISS
from langchain.agents import Tool
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

from spork.utils import _get_chat_history, run_retrieval_chain_with_sources_format

URL = "https://python.langchain.com/en/latest/"


class LangchainDocumentationOracleTool(Tool):
    def __init__(self, llm: BaseLLM, memory: ReadOnlySharedMemory):
        loader = WebBaseLoader(URL)
        docs = loader.load()
        vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            return_source_documents=True,
            memory=memory,
            get_chat_history=_get_chat_history,
        )
        super().__init__(
            name="Langchain Documentation Oracle",
            func=lambda q: run_retrieval_chain_with_sources_format(chain, q),
            description="Use this tool to ask questions about langchain works and how to use it. "
            "You can ask about chains, tools, agents, memory, and other abstractions that langchain provides. "
            "You can also ask for code examples. Input should be a fully formed question.",
        )
