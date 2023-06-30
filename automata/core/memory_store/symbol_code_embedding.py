import logging

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.llm.embedding import SymbolEmbeddingHandler
from automata.core.symbol.base import Symbol
from automata.core.symbol_embedding.base import SymbolCodeEmbedding
from automata.core.symbol_embedding.embedding_builders import SymbolCodeEmbeddingBuilder

logger = logging.getLogger(__name__)


class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
    """Handles a database for `Symbol` source code embeddings."""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: SymbolCodeEmbeddingBuilder,
    ) -> None:
        super().__init__(embedding_db, embedding_builder)

    def get_embedding(self, symbol: Symbol) -> SymbolCodeEmbedding:
        return self.embedding_db.get(symbol.dotpath)

    def process_embedding(self, symbol: Symbol) -> None:
        """Process the embedding for a `Symbol` by updating if the source code has changed."""
        source_code = self.embedding_builder.fetch_embedding_context(symbol)

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol.dotpath):
            self.update_existing_embedding(source_code, symbol)
        else:
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
            self.embedding_db.add(symbol_embedding)

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check for differences between the source code of the symbol and the source code
        of the existing embedding. If there are differences, update the embedding.
        """
        existing_embedding = self.embedding_db.get(symbol.dotpath)
        if existing_embedding.embedding_source != source_code:
            logger.debug("Building a new embedding for %s", symbol)
            self.embedding_db.discard(symbol.dotpath)
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
            self.embedding_db.add(symbol_embedding)
        elif existing_embedding.symbol != symbol:
            logger.debug("Updating the embedding for %s", symbol)
            self.embedding_db.discard(symbol.dotpath)
            existing_embedding.symbol = symbol
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)
