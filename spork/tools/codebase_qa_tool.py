import os
from typing import List

from langchain.agents import Tool
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


class CodebaseQAToolBuilder:
    def __init__(self, codebase_path: str, llm: BaseLLM, memory=None):
        self.codebase_path = codebase_path
        self.llm = llm
        self.memory = memory
        # check that the codebase is a git repo
        # assert (
        #     Path(self.codebase_path).joinpath(".git").exists()
        # ), "Codebase path must be a git repo"
        # go through the codebase and get all the files

    def build(self) -> Tool:
        docs = []
        embeddings = OpenAIEmbeddings()

        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            directory_document = Document(
                page_content=f"Directory: path={dirpath}; folders={dirnames}; filenames={filenames}",
                metadata={"source": dirpath},
            )
            docs.append(directory_document)
            for file in filenames:
                try:
                    loader = TextLoader(os.path.join(dirpath, file))
                    docs.extend(loader.load())
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
        chat_history: List = []
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=docsearch.as_retriever(),
        )

        return Tool(
            name="Codebase QA tool",
            func=lambda q: chain.run({"question": q, "chat_history": chat_history}),
            description="Useful for when you need to answer specific questions about the contents of a specific file in the repository"
            " you're working on, like how does a function work or where is a variable set."
            " Input should be a fully formed question about a file.",
        )
