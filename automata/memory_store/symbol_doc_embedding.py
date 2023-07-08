import logging

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.symbol.base import Symbol, SymbolDescriptor
from automata.symbol_embedding.builders import SymbolDocEmbeddingBuilder
from automata.symbol_embedding.handler import SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    """A class to handle the embedding of symbols"""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: SymbolDocEmbeddingBuilder,
    ) -> None:
        super().__init__(embedding_db, embedding_builder)

    def process_embedding(self, symbol: Symbol) -> None:
        """
        Process the embedding for a `Symbol` -
        Currently we do nothing except update symbol commit hash and source code
        if the symbol is already in the database.
        """

        source_code = self.embedding_builder.fetch_embedding_source_code(symbol)

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol.dotpath):
            self.update_existing_embedding(source_code, symbol)
            return
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            symbol_embedding = self.embedding_builder.build(source_code, symbol)
        elif isinstance(self.embedding_builder, SymbolDocEmbeddingBuilder):
            symbol_embedding = self.embedding_builder.build_non_class(source_code, symbol)
        else:
            raise ValueError("SymbolDocEmbeddingHandler requires a SymbolDocEmbeddingBuilder")

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
