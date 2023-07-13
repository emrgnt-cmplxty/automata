-  For the first question, it really depends on the use cases and
   requirements. The current options to build relationships, references,
   and caller-callee relationships, cover a wide range of information in
   the symbol graph. However, there may be specific contextual
   information that could be useful to capture. An example could be
   building edges for symbols, which are in the same file or module, or
   belong to the same class hierarchy.

-  Regarding the memory issue, one possible solution could be using a
   disk-based graph database, such as Neo4j or Amazon Neptune, instead
   of an in-memory data structure. These databases are designed to
   efficiently store and query large volumes of interconnected data.
   However, this would require significant changes to the
   ``GraphBuilder`` and its related classes. Alternatively, the size of
   the graph could also be reduced by filtering out less important nodes
   and edges, or by simplifying the data structure of the nodes. For
   example, instead of storing all properties of a ``Symbol``, we could
   only store its unique identifier and maintain a separate lookup table
   for its properties.
