import os
from pathlib import Path

from langchain import FAISS
from langchain.agents import Tool
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.memory import ReadOnlySharedMemory
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

from spork.utils import (
    NumberedLinesTextLoader,
    _get_chat_history,
    run_retrieval_chain_with_sources_format,
)


class CodebaseOracleToolBuilder:
    def __init__(self, codebase_path: str, llm: BaseLLM, memory: ReadOnlySharedMemory):
        self.codebase_path = codebase_path
        self.llm = llm
        self.memory = memory
        # check that the codebase is a git repo
        assert (
            Path(self.codebase_path).joinpath(".git").exists()
        ), "Codebase path must be a git repo"
        # we make chain into a mutable state variable, because we need to refresh it occasionally
        self._needs_refresh = True

    def build(self) -> Tool:
        return Tool(
            name="Codebase Oracle tool",
            func=lambda q: run_retrieval_chain_with_sources_format(self._get_chain(), q),
            description="Useful for when you need to answer specific questions about the contents of the repository"
            " you're working on, like how does a given function work or where is a particular variable set,"
            " or what is in a file or where a file is. Input should be a fully formed question.",
        )

    def _build_chain(self):
        docs = []
        embeddings = OpenAIEmbeddings()
        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            if not self._is_excluded(dirpath):
                directory_document = Document(
                    page_content=f"Directory: path={dirpath}; inner_directories={dirnames}; files={filenames}",
                    metadata={"source": dirpath},
                )
                docs.append(directory_document)
                for file in filenames:
                    if not self._is_excluded(os.path.join(dirpath, file)):
                        try:
                            loader = NumberedLinesTextLoader(os.path.join(dirpath, file))
                            docs.extend(loader.load())
                        except Exception as e:
                            print(dirpath, file, e)
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        texts = text_splitter.split_documents(docs)
        docsearch = FAISS.from_documents(texts, embeddings)
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=docsearch.as_retriever(),
            memory=self.memory,
            return_source_documents=False,
            get_chat_history=_get_chat_history,
        )

    def _get_chain(self):
        if self._needs_refresh:
            self._build_chain()
            self._needs_refresh = False
        return self._chain

    def refresh_callback(self):
        # we give this to the editor so that it can tell the codebase oracle to refresh its chain with new codebase content
        self._needs_refresh = True

    def _is_excluded(self, path):
        exclusions = [
            ".git",
            ".gitignore",
            ".gitattributes",
            ".gitmodules",
            "__pycache__",
            ".idea",
            "build",
            "local_env",
            "dist",
            "chroma",
            "egg",  # exclude a few common directories in the
            ".git",  # root of the project
            ".hg",
            ".mypy_cache",
            ".tox",
            ".venv",
            "_build",
            "buck-out",
            "random",
        ]
        for exclusion in exclusions:
            if exclusion in path:
                return True
        return False
