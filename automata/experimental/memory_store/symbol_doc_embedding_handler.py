"""A class to handle the embedding of `Symbol` documents."""
import logging

from automata.core.base import VectorDatabaseProvider
from automata.experimental.symbol_embedding.symbol_doc_embedding_builder import (
    SymbolDocEmbeddingBuilder,
)
from automata.symbol import Symbol, SymbolDescriptor
from automata.symbol_embedding import SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


# TODO - Implement some form of batch handling
class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    """A class to handle the embedding of symbols."""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: "SymbolDocEmbeddingBuilder",
        batch_size: int = 1,
        overwrite: bool = False,
    ) -> None:
        if batch_size != 1:
            raise ValueError(
                "SymbolDocEmbeddingHandler only supports batch_size=1"
            )
        super().__init__(embedding_db, embedding_builder, batch_size)
        self.overwrite = overwrite

    def process_embedding(self, symbol: Symbol) -> None:
        """
        Process the embedding for a `Symbol` -
        Currently we do nothing except update symbol commit hash and source code
        if the symbol is already in the database.
        """
        source_code = self.embedding_builder.fetch_embedding_source_code(
            symbol
        )

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.overwrite or not self.embedding_db.contains(symbol.dotpath):
            self._create_new_embedding(source_code, symbol)
        else:
            self._update_existing_embedding(source_code, symbol)

    def _create_new_embedding(self, source_code: str, symbol: Symbol) -> None:
        """Creates a new embedding for a symbol."""
        if symbol.py_kind == SymbolDescriptor.PyKind.Class:
            logger.debug(f"Creating a new class embedding for {symbol}")
            symbol_embedding = self.embedding_builder.build(
                source_code, symbol
            )
        elif isinstance(self.embedding_builder, SymbolDocEmbeddingBuilder):
            logger.debug(f"Creating a new non-class embedding for {symbol}")
            symbol_embedding = self.embedding_builder.build_non_class(
                source_code, symbol
            )
        else:
            raise ValueError(
                "SymbolDocEmbeddingHandler requires a SymbolDocEmbeddingBuilder"
            )
        self.embedding_db.add(symbol_embedding)
        logger.debug("Successfully added...")

    def _update_existing_embedding(
        self, source_code: str, symbol: Symbol
    ) -> None:
        """Updates the existing embedding for a symbol if necessary."""
        existing_embedding = self.embedding_db.get(symbol.dotpath)
        if (
            existing_embedding.symbol != symbol
            or existing_embedding.source_code != source_code
        ):
            logger.debug(
                f"Rolling forward the embedding for {existing_embedding.symbol} to {symbol}"
            )
            self.embedding_db.discard(symbol.dotpath)
            existing_embedding.symbol = symbol
            existing_embedding.source_code = source_code
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug(f"Doing nothing for symbol {symbol}")
