AgentifiedSearchToolkitBuilder
==============================

Overview
--------

``AgentifiedSearchToolkitBuilder`` is a class responsible for
constructing tools used in agent facilitated search operations. Its
principal role is to create a list of ``Tool`` instances where each tool
represents a different operation in the codebase search process. These
tools perform operations such as fetching top N matches from symbol
search, retrieving the complete Python code for the best match among the
obtained results, and getting comprehensive documentation for the best
match if it exists.

The class uses multiple components to facilitate its operations, such as
a ``SymbolSearch`` object for searching symbols,
``SymbolDocEmbeddingHandler`` for handling symbol document embeddings,
and an ``LLMChatCompletionProvider`` for providing completion prompts.

The class inherits from the ``AgentToolkitBuilder`` abstract class and
overrides its abstract ``build`` method providing a custom
implementation for generating search specific tools.

Related Symbols
---------------

-  ``automata.experimental.search.symbol_search.SymbolSearch``
-  ``automata.experimental.symbol_embedding.symbol_embedding_handler.SymbolDocEmbeddingHandler``
-  ``automata.llm.providers.llm_chat.LLMChatCompletionProvider``
-  ``automata.agent.agent.AgentToolkitBuilder``

Example Usage
-------------

Let’s set up a ``AgentifiedSearchToolkitBuilder`` and build its
corresponding tools:

.. code:: python

   from automata.experimental.tools.builders.agentified_search_builder import AgentifiedSearchToolkitBuilder
   from automata.experimental.search.symbol_search import SymbolSearch
   from automata.experimental.symbol_embedding.symbol_embedding_handler import SymbolDocEmbeddingHandler

   # ...assuming we already have some pre-initialized symbol_search and symbol_doc_embedding_handler objects...

   toolkit_builder = AgentifiedSearchToolkitBuilder(symbol_search, symbol_doc_embedding_handler, top_n=5)

   tools = toolkit_builder.build()

   for tool in tools:
       print(tool.name)  # For instance, print out the name of each created tool

This should generate tools for the agent-facilitated search feature and
print their names: ‘search-top-matches’, ‘search-best-match-code’, and
‘search-best-match-docs’.

Limitations
-----------

``AgentifiedSearchToolkitBuilder`` relies on the
``get_symbol_code_similarity_results`` function of the provided
SymbolSearch object to acquire search results. Any limitations to this
function or inaccurate results produced by this function will affect the
toolkit builder’s performance.

Moreover, the builder assumes that documentation and code of the best
match are readily available and valid. In scenarios where these are
missing or improperly formatted, the tools generated may fail to perform
as expected.

Follow-up Questions:
--------------------

-  How does ``AgentifiedSearchToolkitBuilder`` handle cases where the
   ``SymbolSearch`` object does not find any matching symbols?
-  What alternatives are there if the
   ``get_symbol_code_similarity_results`` function in the provided
   ``SymbolSearch`` object is deficient or unavailable?
-  How can ``AgentifiedSearchToolkitBuilder`` handle the absence or
   improper formatting of documentation and code?
