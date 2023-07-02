import logging

from automata.core.symbol.base import Symbol
from automata.core.symbol_embedding.base import (
    JSONSymbolEmbeddingVectorDatabase,
    SymbolDocEmbedding,
    SymbolEmbeddingHandler,
)
from automata.core.symbol_embedding.builders import SymbolDocEmbeddingBuilder

logger = logging.getLogger(__name__)


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    """A class to handle the embedding of symbols"""

    def __init__(
        self,
        embedding_db: JSONSymbolEmbeddingVectorDatabase,
        embedding_builder: SymbolDocEmbeddingBuilder,
    ) -> None:
        self.embedding_db = embedding_db
        self.embedding_builder = embedding_builder

    def get_embedding(self, symbol: Symbol) -> SymbolDocEmbedding:
        return self.embedding_db.get(symbol.dotpath)

    def process_embedding(self, symbol: Symbol) -> None:
        source_code = self.embedding_builder.fetch_embedding_context(symbol)

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol.dotpath):
            self.update_existing_embedding(source_code, symbol)
        else:
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
            self.embedding_db.add(symbol_embedding)

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        existing_embedding = self.embedding_db.get(symbol.dotpath)
        if existing_embedding.symbol != symbol or existing_embedding.source_code != source_code:
            logger.debug(
                f"Rolling forward the embedding for {existing_embedding.symbol} to {symbol}"
            )
            self.embedding_db.discard(symbol.dotpath)
            existing_embedding.symbol = symbol
            existing_embedding.source_code = source_code
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)
