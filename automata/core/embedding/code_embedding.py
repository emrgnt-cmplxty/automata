import logging

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.llm.embedding import (
    EmbeddingProvider,
    SymbolEmbeddingBuilder,
    SymbolEmbeddingHandler,
)
from automata.core.symbol.base import Symbol, SymbolCodeEmbedding

logger = logging.getLogger(__name__)


class SymbolCodeEmbeddingBuilder(SymbolEmbeddingBuilder):
    """Builds `Symbol` source code embeddings."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self.embedding_provider = embedding_provider

    def build(self, source_code: str, symbol: Symbol) -> SymbolCodeEmbedding:
        embedding_vector = self.embedding_provider.build_embedding_array(source_code)
        return SymbolCodeEmbedding(symbol, source_code, embedding_vector)

    def fetch_embedding_context(self, symbol: Symbol) -> str:
        """For a code embedding the context is the source code itself."""
        from automata.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        return str(convert_to_fst_object(symbol))


class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
    """Handles a database for `Symbol` source code embeddings."""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: SymbolCodeEmbeddingBuilder,
    ) -> None:
        super().__init__(embedding_db, embedding_builder)

    def get_embedding(self, symbol: Symbol) -> SymbolCodeEmbedding:
        return self.embedding_db.get(symbol)

    def process_embedding(self, symbol: Symbol) -> None:
        """Process the embedding for a `Symbol` by updating if the source code has changed."""
        source_code = self.embedding_builder.fetch_embedding_context(symbol)

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol):
            self.update_existing_embedding(source_code, symbol)
        else:
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
            self.embedding_db.add(symbol_embedding)

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check for differences between the source code of the symbol and the source code
        of the existing embedding. If there are differences, update the embedding.
        """
        existing_embedding = self.embedding_db.get(symbol)
        if existing_embedding.embedding_source != source_code:
            logger.debug("Building a new embedding for %s", symbol)
            self.embedding_db.discard(symbol)
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
            self.embedding_db.add(symbol_embedding)
        elif existing_embedding.symbol != symbol:
            logger.debug("Updating the embedding for %s", symbol)
            self.embedding_db.discard(symbol)
            existing_embedding.symbol = symbol
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)


# import logging

# from automata.core.base.database.vector import VectorDatabaseProvider
# from automata.core.llm.embedding import EmbeddingProvider, SymbolEmbeddingHandler
# from automata.core.symbol.base import Symbol, SymbolCodeEmbedding

# logger = logging.getLogger(__name__)


# class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
#     """Handles a database and provider for `Symbol` source code embeddings."""

#     def __init__(
#         self,
#         embedding_db: VectorDatabaseProvider,
#         embedding_provider: EmbeddingProvider,
#     ) -> None:
#         super().__init__(embedding_db, embedding_provider)

#     def get_embedding(self, symbol: Symbol) -> SymbolCodeEmbedding:
#         return self.embedding_db.get(symbol)

#     def process_embedding(self, symbol: Symbol) -> None:
#         """Process the embedding for a `Symbol` by updating if the source code has changed."""
#         from automata.core.symbol.symbol_utils import (  # imported late for mocking
#             convert_to_fst_object,
#         )

#         source_code = str(convert_to_fst_object(symbol))

#         if not source_code:
#             raise ValueError(f"Symbol {symbol} has no source code")

#         if self.embedding_db.contains(symbol):
#             self.update_existing_embedding(source_code, symbol)
#         else:
#             symbol_embedding = self.build_embedding_array(source_code, symbol)
#             self.embedding_db.add(symbol_embedding)

#     def build_embedding_array(self, source_code: str, symbol: Symbol) -> SymbolCodeEmbedding:
#         embedding_vector = self.embedding_provider.build_embedding_array(source_code)
#         return SymbolCodeEmbedding(symbol, source_code, embedding_vector)

#     def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
#         """
#         Check for differences between the source code of the symbol and the source code
#         of the existing embedding. If there are differences, update the embedding.
#         """
#         existing_embedding = self.embedding_db.get(symbol)
#         if existing_embedding.embedding_source != source_code:
#             logger.debug("Building a new embedding for %s", symbol)
#             self.embedding_db.discard(symbol)
#             symbol_embedding = self.build_embedding_array(source_code, symbol)
#             self.embedding_db.add(symbol_embedding)
#         elif existing_embedding.symbol != symbol:
#             logger.debug("Updating the embedding for %s", symbol)
#             self.embedding_db.discard(symbol)
#             existing_embedding.symbol = symbol
#             self.embedding_db.add(existing_embedding)
#         else:
#             logger.debug("Passing for %s", symbol)
