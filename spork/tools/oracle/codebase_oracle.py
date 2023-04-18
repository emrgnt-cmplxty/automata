import os
from pathlib import Path
from typing import List, Tuple

from langchain import FAISS, PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.schema import AIMessage, Document, HumanMessage
from langchain.text_splitter import CharacterTextSplitter

from spork.tools.utils import NumberedLinesTextLoader, home_path

prompt_template = """Use the following pieces of context to answer the question about a codebase.
This codebase is giving to you in context, and it's called improved-spork.
The question may ask about some file or a piece of code, and you will always be able to come up with an answer using only the provided conext.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


class CodebaseOracle:
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

    def refresh_callback(self) -> None:
        # we give this to the editor so that it can tell the codebase oracle to refresh its chain with new codebase content
        self._needs_refresh = True

    def get_chain(self):
        if self._needs_refresh:
            self._build_chain()
            self._needs_refresh = False
        return self._chain

    @staticmethod
    def get_default_codebase_oracle() -> "CodebaseOracle":
        llm = ChatOpenAI(streaming=True, temperature=0.7, model_name="gpt-4")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        read_only_memory = ReadOnlySharedMemory(memory=memory)
        return CodebaseOracle(home_path(), llm, read_only_memory)

    def _build_chain(self) -> None:
        docs = []
        embeddings = OpenAIEmbeddings()
        for dirpath, dirnames, filenames in os.walk(self.codebase_path):
            if not CodebaseOracle._is_excluded(dirpath):
                directory_document = Document(
                    page_content=f"Directory: path={dirpath}; inner_directories={dirnames}; files={filenames}",
                    metadata={"source": dirpath},
                )
                docs.append(directory_document)
                for file in filenames:
                    if not CodebaseOracle._is_excluded(os.path.join(dirpath, file)):
                        try:
                            loader = NumberedLinesTextLoader(os.path.join(dirpath, file))
                            docs.extend(loader.load())
                        except Exception as e:
                            print(dirpath, file, e)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
        texts = text_splitter.split_documents(docs)
        docsearch = FAISS.from_documents(texts, embeddings)
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=docsearch.as_retriever(),
            qa_prompt=QA_PROMPT,
            memory=self.memory,
            return_source_documents=True,
            get_chat_history=CodebaseOracle._get_chat_history,
        )

    @staticmethod
    def _is_excluded(path) -> bool:
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

    @staticmethod
    def _get_chat_history(chat_history: List[Tuple[HumanMessage, AIMessage]]) -> str:
        buffer = ""
        for human_m, ai_m in chat_history:
            human = "Human: " + str(human_m)
            ai = "Assistant: " + str(ai_m)
            buffer += "\n" + "\n".join([human, ai])
        return buffer
