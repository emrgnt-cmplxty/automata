import logging
from typing import List, Tuple

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.symbol.base import Symbol
from automata.symbol_embedding.builders import SymbolCodeEmbeddingBuilder
from automata.symbol_embedding.handler import SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    """Handles a database for `Symbol` source code embeddings."""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: SymbolCodeEmbeddingBuilder,
        batch_size: int = 512,
    ) -> None:
        super().__init__(embedding_db, embedding_builder, batch_size)
        self.to_build: List[Tuple[str, Symbol]] = []

    def process_embedding(self, symbol: Symbol) -> None:
        """
        Process the embedding for a list of `Symbol`s by updating if the
        source code has changed.
        """
        source_code = self.embedding_builder.fetch_embedding_source_code(symbol)
        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")
        if self.embedding_db.contains(symbol.dotpath):
            self._update_existing_embedding(source_code, symbol)
        else:
            self._queue_for_building(source_code, symbol)

    def _update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check for differences between the source code of the symbol and the source code
        of the existing embedding. If there are differences, update the embedding.
        """
        existing_embedding = self.embedding_db.get(symbol.dotpath)

        if existing_embedding.document != source_code:
            self.to_discard.append(symbol.dotpath)
            self.to_build.append((source_code, symbol))
        elif existing_embedding.symbol != symbol:
            self.to_discard.append(symbol.dotpath)
            existing_embedding.symbol = symbol
            self.to_add.append(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)

        # If we have enough embeddings to update or create, do a batch update or creation
        if len(self.to_discard) >= self.batch_size or len(self.to_add) >= self.batch_size:
            self.flush()

    def _queue_for_building(self, source_code: str, symbol: Symbol) -> None:
        """Queue the symbol for batch embedding building."""
        self.to_build.append((source_code, symbol))

        if len(self.to_build) >= self.batch_size:
            self._build_and_add_embeddings()
            self.flush()

    def _build_and_add_embeddings(self) -> None:
        """Build and add the embeddings for the queued symbols."""
        # sources, symbols = zip(*self.to_build)
        sources = [ele[0] for ele in self.to_build]
        symbols = [ele[1] for ele in self.to_build]
        symbol_embeddings = self.embedding_builder.batch_build(sources, symbols)
        self.to_build = []

        self.to_add.extend(symbol_embeddings)
        logger.debug("Created new embeddings for symbols")

        if len(self.to_add) >= self.batch_size:
            self.flush()

    def flush(self):
        if self.to_build:
            self._build_and_add_embeddings()
        super().flush()
