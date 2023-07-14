-  To handle parsing errors more gracefully within
   ``ReferenceProcessor.process()``, a possible way would be to add a
   default representation for unparseable symbols. This could be a
   certain default symbol node which all unparseable symbols are
   connected to. This way, we would still have a record of these
   unparseable symbols in the graph, which could be useful for later
   analysis or debugging. However, this approach should be treated
   carefully as this might lead to misleading interpretations of the
   graph (i.e. many references to this default node might be considered
   as a prominent symbol in the graph).

-  If ``ReferenceProcessor`` was dealing with a standard ``DiGraph``
   instead of a ``MultiDiGraph``, multiple references between the same
   pair of nodes would overwrite each other since ``DiGraph`` does not
   support multi-edges. This would lose important information about the
   number and context of these multiple references, and may affect the
   accuracy of subsequent analyses based on the graph. Therefore, for
   use cases where multiple independent references between the same pair
   of nodes are possible (like a codebase where a function or variable
   might be referenced multiple times), a ``MultiDiGraph`` would be the
   more correct choice.
