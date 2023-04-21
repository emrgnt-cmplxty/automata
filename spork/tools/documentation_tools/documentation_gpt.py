"""
DocGPT

A simple chatbot that uses DocGPT to answer questions about documentation.


"""
import logging
import logging.config
import traceback

from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings

from ..utils import get_logging_config

logger = logging.getLogger(__name__)


class DocumentationGPT:
    def __init__(self, url, model="gpt-3.5-turbo", temperature=0.7, verbose=False):
        load_dotenv()
        self.url = url
        self.model = model
        self.temperature = temperature
        self.verbose = verbose
        self.loader = WebBaseLoader(self.url)
        self.docs = self.loader.load()
        self.llm = ChatOpenAI(streaming=True, temperature=0, model=self.model)
        self.vector_store = FAISS.from_documents(self.docs, OpenAIEmbeddings())
        self.chat_history = []

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            return_source_documents=self.verbose,
        )
        logging_config = get_logging_config(
            log_level=logging.DEBUG if self.verbose else logging.INFO
        )
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info(
            f"Starting chat session for {self.url} using {self.model} with t={self.temperature}..."
        )
        while True:
            try:
                query = input("You: ")
                result = self.chain({"question": query, "chat_history": self.chat_history})
                answer = result["answer"]
                self.logger.info(f"DocGPT: {answer}")
                self.chat_history += [(query, answer)]
            except KeyboardInterrupt:
                self.logger.info("Ending chat session...")
                break
            except Exception as e:
                tb = traceback.format_exc()
                self.logger.info("Oops: %s %s" % (e, tb))
