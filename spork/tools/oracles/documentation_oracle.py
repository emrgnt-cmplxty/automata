from langchain import FAISS
from langchain.agents import Tool
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

from spork.utils import _get_chat_history, run_retrieval_chain_with_sources_format


class DocumentationOracleTool(Tool):
    def __init__(
        self,
        llm: BaseLLM,
        memory: ReadOnlySharedMemory,
        url: str,
        name: str,
        description: str,
    ):
        loader = WebBaseLoader(url)
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
            name=name,
            func=lambda q: run_retrieval_chain_with_sources_format(chain, q),
            description=description,
        )
