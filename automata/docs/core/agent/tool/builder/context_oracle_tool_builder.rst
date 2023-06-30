ContextOracleToolBuilder
========================

``ContextOracleToolBuilder`` is a class that provides a powerful tool
combining ``SymbolSearch`` and ``SymbolSimilarity`` to create rich and
relevant contexts given a query. This functionality can be useful in
applications such as documentation or codebase exploration where context
about certain elements is required.

Overview
--------

The ``ContextOracleToolBuilder`` class creates a tool that allows you to
search for symbols and analyze symbol-related documentation. Given a
query, it calculates the similarity between each symbol’s documentation
and the query to find the most similar documents. Then, it uses
``SymbolSearch`` to combine Semantic Search with PageRank to find the
most relevant symbols to the query. The overview documentation of these
symbols is then combined with the result of the ``SymbolSimilarity`` to
create a comprehensive context.

Import Statements
-----------------

.. code:: python

   import logging
   import textwrap
   from typing import List
   from automata.config.base import LLMProvider
   from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
   from automata.core.base.agent import AgentToolBuilder, AgentToolProviders
   from automata.core.base.tool import Tool
   from automata.core.symbol_embedding.similarity import SymbolSimilarityCalculator
   from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool
   from automata.core.symbol.search.symbol_search import SymbolSearch

Related Symbols
---------------

Here are the classes closely related to ``ContextOracleToolBuilder``

-  ``automata.tests.unit.test_context_oracle_tool.test_init``
-  ``automata.core.agent.tool.builder.context_oracle.ContextOracleOpenAIToolBuilder``
-  ``automata.tests.unit.test_context_oracle_tool.context_oracle_tool_builder``
-  ``automata.tests.unit.test_context_oracle_tool.test_build``

Example
-------

Below is an example demonstrating how to create an instance of
``ContextOracleToolBuilder``.

.. code:: python

   from automata.core.agent.tool.builder.context_oracle import ContextOracleToolBuilder
   from automata.core.symbol.search.symbol_search import SymbolSearch # Replace MagicMock in example
   from automata.core.symbol_embedding.similarity import SymbolSimilarityCalculator # Replace MagicMock in example

   symbol_search = SymbolSearch() # Mocked in example, replace with appropriate parameters
   symbol_doc_similarity = SymbolSimilarityCalculator() # Mocked in example, replace with appropriate parameters

   context_oracle_tool_builder = ContextOracleToolBuilder(
                   symbol_search=symbol_search_mock, 
                   symbol_doc_similarity=symbol_doc_similarity_mock
               )

Limitations
-----------

It is important to note that the quality of the context created by
``ContextOracleToolBuilder`` largely depends on the effectiveness and
accuracy of the ``SymbolSearch`` and ``SymbolSimilarityCalculator``
classes. If these classes are flawed or not finely tuned, the generated
context might not be as relevant or comprehensive.

Follow-up Questions:
--------------------

-  How can we improve the novel combination of the SymbolSearch and
   SymbolSimilarity tools?
-  Are there ways to fine-tune the page rank or semantic search to yield
   even more relevant results?
-  How robust is the tool in its current state? What types of queries or
   symbols would it struggle with?
