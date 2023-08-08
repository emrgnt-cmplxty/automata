DocumentOracleToolkitBuilder
============================

Overview
--------

``DocumentOracleToolkitBuilder`` is a class derived from
``AgentToolkitBuilder`` that is primarily focused on providing tools
which translate a natural language processing (NLP) query to relevant
context. It accomplishes this by finding the most semantically similar
symbol’s documentation in a Python codebase.

The builder utilizes two main components: ``SymbolSearch`` and
``SymbolDocEmbeddingHandler``. These components assist in identifying
the most related symbol in a given codebase, and returning its
corresponding class documentation which provides context for the query.

The builder method constructs the tools associated with the
``DocumentOracleToolkitBuilder``, designated with the name
‘document-oracle’.

Related Symbols
---------------

-  ``automata.cli.env_operations.replace_key``
-  ``automata.symbol.symbol_base.Symbol.is_protobuf``
-  ``automata.symbol.symbol_base.SymbolDescriptor.unparse``
-  ``automata.tasks.task_base.Task._get_log_dir``
-  ``automata.tasks.task_base.Task._get_task_dir``
-  ``automata.cli.env_operations.get_key``
-  ``automata.symbol_embedding.symbol_embedding_base.SymbolCodeEmbedding.metadata``
-  ``automata.llm.providers.openai_llm.OpenAIChatMessage.to_dict``
-  ``automata.cli.env_operations.log_cli_output``
-  ``automata.experimental.scripts.run_update_tool_eval.process_modules``

Usage Example
-------------

.. code:: python

   from automata.experimental.tools.builders.document_oracle_builder import DocumentOracleToolkitBuilder
   from automata.symbol_search import SymbolSearch
   from automata.embedding_handlers.symbol_doc_embedding_handler import SymbolDocEmbeddingHandler

   symbol_search = SymbolSearch(symbol_database, symbol_ranker)
   symbol_doc_embedding_handler = SymbolDocEmbeddingHandler(embedding_calculator, symbol_database)

   doc_oracle_builder = DocumentOracleToolkitBuilder(symbol_search, symbol_doc_embedding_handler)
   doc_oracle_tool = doc_oracle_builder.build()[0]

   query = "What is the purpose of replace_key function?"
   res = doc_oracle_tool.function(query)

Limitations
-----------

The primary limitation of the ``DocumentOracleToolkitBuilder`` is its
dependence on the quality and correctness of the embedded documentation
linked to code symbols. It inherently relies on the accuracy of natural
language understanding capabilities to find the right context from the
symbol’s documentation. Thus, poorly documented or ambiguous definitions
could lead to misleading context. Further, it might fail when trying to
generate embeddings for symbols, in such cases, it returns the
corresponding error.

Lastly, ``DocumentOracleToolkitBuilder`` does not account for potential
changes in a codebase over time. To function optimally, the tool assumes
an up-to-date codebase with complete and relevant documentation for each
symbol.

Follow-up Questions:
--------------------

-  Is there a feature to update the symbol embeddings in the
   ``DocumentOracleToolkitBuilder`` in case of dynamic changes in the
   codebase?
