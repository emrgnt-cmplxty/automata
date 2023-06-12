import abc
from typing import Any, Dict, List

import jsonpickle
import numpy as np

from automata_docs.core.database.provider import DatabaseProvider
from automata_docs.core.symbol.symbol_types import Embedding, Symbol


class VectorDatabaseProvider(DatabaseProvider):
    """
    Abstract base class for different types of vector database providers.
    """

    @abc.abstractmethod
    def calculate_similarity(self, embedding: Embedding) -> List[Dict[Symbol, float]]:
        """
        Abstract method to calculate the similarity between the given vector and vectors in the database.
        """
        pass


class JSONVectorDB(VectorDatabaseProvider):
    """
    Concrete class to provide a vector database that saves into a JSON file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[Embedding] = []
        self.index: Dict[Symbol, int] = {}
        self.load()

    def save(self):
        with open(self.file_path, "w") as file:
            encoded_data = jsonpickle.encode(self.data)
            file.write(encoded_data)

    def load(self) -> Any:
        with open(self.file_path, "r") as file:
            self.data = jsonpickle.decode(file.read())
            self.index = {embedding.symbol: i for i, embedding in enumerate(self.data)}

    def add(self, embedding: Embedding):
        self.data.append(embedding)
        self.index[embedding.symbol] = len(self.data) - 1

    def discard(self, symbol: Symbol):
        index = self.index[symbol]
        del self.data[index]
        del self.index[symbol]

    def get(self, symbol: Symbol) -> Embedding:
        return self.data[self.index[symbol]]

    def clear(self):
        self.data = []
        self.index = {}

    def calculate_similarity(self, vector: np.array) -> List[Dict[Symbol, float]]:
        # Implement the logic to calculate similarity between the given vector and vectors in the data.
        # This will depend on how the data is structured and the specific similarity measure to be used (e.g., cosine similarity).
        # Here, just returning the data as a placeholder.
        # return self.data
        pass
