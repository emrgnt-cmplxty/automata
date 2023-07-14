-  ``batch_size`` and the frequency of calls to ``flush`` are directly
   related. ``batch_size`` specifies the number of items that should be
   stored in memory before they are written (flushed) to the database. A
   larger ``batch_size`` would result in fewer calls to ``flush``, but
   would take up more memory. Therefore, a balance must be struck
   depending on the system’s resource constraints.

-  The size of the embeddings processed by
   ``SymbolCodeEmbeddingHandler`` can vary depending on the architecture
   of the embedding model used. For example, typical configurations of
   Word2Vec or GloVe could result in 100, 200, or 300-dimentional
   embeddings, while BERT embeddings might be 768-dimensional or larger.

-  The handling of symbols with no source code would depend on the
   implementation of ``SymbolCodeEmbeddingBuilder``. A common approach
   might be to return a null or zero vector of the same size as other
   embeddings. The ``SymbolCodeEmbeddingHandler`` would probably handle
   such cases as it does most other embeddings, unless a special case
   has been defined.
