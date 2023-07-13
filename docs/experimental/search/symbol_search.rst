1. Yes, SymbolSearch can be utilized in real-time as long as the code
   being added or edited is properly indexed in the symbol graph. It
   operates based on the current state of the graph, so any updates will
   be taken into account during subsequent searches.

2. The handling of renaming or refactoring is mainly dependent on the
   indexing step. If symbols are renamed or refactored, the index (and
   by extension, the symbol graph) should be updated to reflect these
   changes. Once that’s done, SymbolSearch will be able to correctly
   identify the refactored or renamed symbols.

3. Yes, SymbolSearch is designed to support search methods beyond exact
   matches. It can also search for symbols semantically, which can find
   symbols related to a search pattern even if they don’t exactly match.
   The semantic search is done primarily through the use of embeddings,
   which capture the semantic relationships between different symbols.
   This allows the search to find related symbols based on their
   meanings, not just their names.
