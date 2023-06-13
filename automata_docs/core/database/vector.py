import abc
import logging
import logging.config
from typing import Dict, List

import jsonpickle
import numpy as np

from automata_docs.core.database.provider import SymbolDatabaseProvider
from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding

logger = logging.getLogger(__name__)


class VectorDatabaseProvider(SymbolDatabaseProvider):
    """
    Abstract base class for different types of vector database providers.
    """

    @abc.abstractmethod
    def calculate_similarity(self, embedding: SymbolEmbedding) -> List[Dict[Symbol, float]]:
        """
        Abstract method to calculate the similarity between the given vector and vectors in the database.
        """
        pass

    @abc.abstractmethod
    def get_all_symbols(self) -> List[Symbol]:
        """
        Abstract method to calculate the similarity between the given vector and vectors in the database.
        """
        pass


class JSONVectorDatabase(VectorDatabaseProvider):
    """
    Concrete class to provide a vector database that saves into a JSON file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[SymbolEmbedding] = []
        self.index: Dict[Symbol, int] = {}
        self.load()

    def save(self) -> None:
        with open(self.file_path, "w") as file:
            encoded_data = jsonpickle.encode(self.data)
            file.write(encoded_data)

    def load(self) -> None:
        try:
            with open(self.file_path, "r") as file:
                self.data = jsonpickle.decode(file.read())
                self.index = {embedding.symbol: i for i, embedding in enumerate(self.data)}
        except FileNotFoundError:
            logger.info("Creating new vector embedding db at %s" % self.file_path)

    def add(self, embedding: SymbolEmbedding) -> None:
        self.data.append(embedding)
        self.index[embedding.symbol] = len(self.data) - 1

    def update(self, embedding: SymbolEmbedding) -> None:
        self.data[self.index[embedding.symbol]] = embedding

    def discard(self, symbol: Symbol) -> None:
        index = self.index[symbol]
        del self.data[index]
        del self.index[symbol]

    def contains(self, symbol: Symbol) -> bool:
        return symbol in self.index

    def get(self, symbol: Symbol) -> SymbolEmbedding:
        return self.data[self.index[symbol]]

    def clear(self) -> None:
        self.data = []
        self.index = {}

    def calculate_similarity(self, vector: np.array) -> List[Dict[Symbol, float]]:
        # Implement the logic to calculate similarity between the given vector and vectors in the data.
        # This will depend on how the data is structured and the specific similarity measure to be used (e.g., cosine similarity).
        # Here, just returning the data as a placeholder.
        # return self.data
        raise NotImplementedError

    def get_all_symbols(self) -> List[Symbol]:
        symbol_list = list(self.index.keys())
        return sorted(symbol_list, key=lambda x: str(x.path))
