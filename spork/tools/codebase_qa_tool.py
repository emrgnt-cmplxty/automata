import os
from pathlib import Path

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
        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            for file in filenames:
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
