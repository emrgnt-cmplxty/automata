AdvancedContextOracleToolkitBuilder
===================================

``AdvancedContextOracleToolkitBuilder`` is a builder class in the
Automata framework that provides tools which translate Natural Language
Processing (NLP) queries into relevant context. It retrieves the context
by evaluating semantic similarity between a specified query and
documentation/code of available symbols.

Overview
--------

The ``AdvancedContextOracleToolkitBuilder`` gets initiated with
``symbol_search``, ``symbol_doc_embedding_handler``,
``symbol_code_embedding_handler``, and
``embedding_similarity_calculator`` objects. These dependencies are used
for handling and translating symbols and their embeddings.

The builder can create a list of ``Tool`` objects through its ``build``
method. These tools utilize the ``EmbeddingSimilarityCalculator`` and
``SymbolSearch`` to provide context for a given query by computing
semantic similarity between the query and all available symbols’
documentation and code.

Finally, the ``_get_context`` method provides the core functionality of
the ``AdvancedContextOracleToolkitBuilder``. Given a query, it
constructs the context by concatenating the source code and
documentation of the most semantically similar symbol to the query. It
also includes documentation summaries of the most highly ranked symbols
which are similar to the query.

Related Symbols
---------------

-  ``automata.cli.options.common_options``
-  ``automata.singletons.github_client.GitHubClient.__init__``
-  ``automata.tasks.task_registry.AutomataTaskRegistry.get_all_tasks``
-  ``automata.cli.cli_utils.ask_choice``
-  ``automata.llm.llm_base.LLMConversation.get_messages_for_next_completion``
-  ``automata.tasks.task_environment.AutomataTaskEnvironment.__init__``
-  ``automata.symbol.symbol_base.SymbolPackage.__repr__``
-  ``automata.symbol.graph.symbol_relationships.RelationshipProcessor.__init__``
-  ``automata.tasks.task_database.AutomataAgentTaskDatabase.update_task``
-  ``automata.tasks.task_database.AutomataAgentTaskDatabase.insert_task``

Usage Example
-------------

.. code:: python

   from automata.experimental.tools.builders.advanced_context_oracle_builder import AdvancedContextOracleToolkitBuilder

   symbol_search = # Initialized SymbolSearch object
   symbol_doc_embedding_handler = # Initialized SymbolDocEmbeddingHandler object
   symbol_code_embedding_handler = # Initialized SymbolCodeEmbeddingHandler object
   embedding_similarity_calculator = # Initialized EmbeddingSimilarityCalculator object

   builder = AdvancedContextOracleToolkitBuilder(
       symbol_search,
       symbol_doc_embedding_handler,
       symbol_code_embedding_handler,
       embedding_similarity_calculator
   )

   tools = builder.build()

   # Get context for a query
   query = "input processing"
   context = tools[0].function(query)

   print(context)

Ensure to replace ``# Initialized ... object`` comments with the actual
initialized objects.

Limitations
-----------

The ``AdvancedContextOracleToolkitBuilder`` relies on the semantic
similarity of the query with symbols’ documentation and source code to
produce the context. This can be a potential limitation as the accuracy
of the context provided depends on the similarity metrics and the
quality of the symbols’ documentation and source code.

Follow-up Questions:
--------------------

-  What kinds of similarity metrics are used?
-  How can we ensure the quality of the documentation and source code?
-  Are there ways to improve the semantic similarity calculation for
   more accurate context?
-  How can we deal with symbols which don’t have meaningful or relevant
   documentation or source code?
