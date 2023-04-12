import os
from pathlib import Path
from typing import List

from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


class CodebaseQAToolBuilder:
    def __init__(self, codebase_path: str, llm: BaseLLM):
        self.codebase_path = codebase_path
        self.llm = llm
        # check that the codebase is a git repo
        assert (
            Path(self.codebase_path).joinpath(".git").exists()
        ), "Codebase path must be a git repo"
        # go through the codebase and get all the files

    def build(self) -> Tool:
        docs = []
        embeddings = OpenAIEmbeddings()
        # skip anything in gitignore
        ignore = self._get_gitignore_files_and_dirs()
        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            if dirpath in ignore:
                continue
            for file in filenames:
                if file in ignore:
                    continue
                try:
                    loader = TextLoader(os.path.join(dirpath, file))
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    print(dirpath, file, e)

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(docs)
        print(
            "CodeQATool: Running Chroma using direct local API. Using DuckDB in-memory for database. Data will be transient."
        )

        docsearch = Chroma.from_documents(
            texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]
        )
        chain = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=docsearch.as_retriever()
        )

        return Tool(
            name="Codebase QA System",
            func=chain.run,
            description="useful for when you need to answer questions about the contents of the codebase"
            " you're working on, like how does a function work or what does a file do."
            " Input should be a fully formed question.",
        )

    def _get_gitignore_files_and_dirs(self) -> List[str]:
        # get the gitignore file
        gitignore_path = Path(self.codebase_path).joinpath(".gitignore")
        if not gitignore_path.exists():
            return []
        with open(gitignore_path, "r") as f:
            gitignore = f.read()
            # get the files and dirs to ignore
            files_and_dirs = gitignore.split("\n")
            # remove comments
            files_and_dirs = [f for f in files_and_dirs if not f.startswith("#")]
            # remove empty lines
            files_and_dirs = [f for f in files_and_dirs if f]
            return files_and_dirs
