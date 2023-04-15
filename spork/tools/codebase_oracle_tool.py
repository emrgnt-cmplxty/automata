import os
from pathlib import Path

from langchain import FAISS
from langchain.agents import Tool
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.memory import ReadOnlySharedMemory
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

from spork.utils import NumberedLinesTextLoader


def run_retrieval_chain_with_sources(chain: BaseConversationalRetrievalChain, q: str) -> str:
    result = chain(q)
    return f'Answer: {result["answer"]}.\n\n Sources: {result["source_documents"]}'


class CodebaseOracleToolBuilder:
    def __init__(self, codebase_path: str, llm: BaseLLM, memory: ReadOnlySharedMemory):
        self.codebase_path = codebase_path
        self.llm = llm
        self.memory = memory
        # check that the codebase is a git repo
        assert (
            Path(self.codebase_path).joinpath(".git").exists()
        ), "Codebase path must be a git repo"
        # go through the codebase and get all the files

    def build(self) -> Tool:
        docs = []
        embeddings = OpenAIEmbeddings()
        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            if not self.is_excluded(dirpath):
                directory_document = Document(
                    page_content=f"Directory: path={dirpath}; inner_directories={dirnames}; files={filenames}",
                    metadata={"source": dirpath},
                )
                docs.append(directory_document)
                for file in filenames:
                    if not self.is_excluded(os.path.join(dirpath, file)):
                        try:
                            loader = NumberedLinesTextLoader(os.path.join(dirpath, file))
                            docs.extend(loader.load())
                        except Exception as e:
                            print(dirpath, file, e)
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        texts = text_splitter.split_documents(docs)

        docsearch = FAISS.from_documents(
            texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]
        )
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=docsearch.as_retriever(),
            memory=self.memory,
            return_source_documents=True,
        )
        return Tool(
            name="Codebase Oracle tool",
            func=lambda q: run_retrieval_chain_with_sources(chain, q),
            description="Useful for when you need to answer specific questions about the contents of the repository"
            " you're working on, like how does a given function work or where is a particular variable set,"
            " or what is in a particular file. Input should be a fully formed question.",
        )

    def is_excluded(self, path):
        exclusions = [
            ".git",
            ".gitignore",
            ".gitattributes",
            ".gitmodules",
            "__pycache__",
            ".idea",
            "/build/",
            "local_env",
            "/.",
        ]
        for exclusion in exclusions:
            if exclusion in path:
                return True
        return False
