DependencyFactory
=================

``DependencyFactory`` is a source class found in
**automata.singleton.dependency_factory** that is utilized in the
creation of dependencies for input Tool construction.

The main functionality of ``DependencyFactory`` is to ensure that the
dependencies required by any given set of tools are created and made
available for use.

The ``DependencyFactory`` class implements singleton design pattern,
means there will only be one instance of this class and all the required
dependencies are created on this single instance.

Import Statements:
------------------

When making use of the ``DependencyFactory`` class, below are the
dependencies to import,

.. code:: python

   import os
   import networkx as nx
   from functools import lru_cache
   from typing import Any, Dict, List, Set, Tuple
   from automata.config.base import ConfigCategory
   from automata.agent.agent import AgentToolkitNames
   from automata.agent.error import AgentGeneralError, UnknownToolError
   from automata.core.base.patterns.singleton import Singleton
   from automata.code_handling.py.reader import PyReader
   from automata.code_handling.py.writer import PyWriter
   from automata.embedding.base import EmbeddingSimilarityCalculator
   from automata.experimental.search.rank import SymbolRank, SymbolRankConfig
   from automata.experimental.search.symbol_search import SymbolSearch
   from automata.llm.providers.openai import (
         OpenAIChatCompletionProvider,
         OpenAIEmbeddingProvider,
     )
   from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
   from automata.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
   from automata.retrievers.py.context import (
         PyContextRetriever,
         PyContextRetrieverConfig,
     )
   from automata.symbol.graph import SymbolGraph
   from automata.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
   from automata.symbol_embedding.builders import (
         SymbolCodeEmbeddingBuilder,
         SymbolDocEmbeddingBuilder,
     )
   from automata.tools.factory import AgentToolFactory, logger
   from automata.core.utils import get_config_fpath

Usage Example
-------------

Here is an example that showcases how ``DependencyFactory`` is used:

.. code:: python

   from automata.singletons.dependency_factory import DependencyFactory

   # Create a DependencyFactory object setting the overrides
   dep_factory = DependencyFactory(py_context_retriever_config=PyContextRetrieverConfig())

   # To get the instance of a created dependency use 'get' method
   symbol_ranker = dep_factory.get('symbol_rank')

   # After using the instances, do not forget to reset overrides
   dep_factory.set_overrides()

Limitations
-----------

The DependencyFactory class doesn’t handle concurrent requests.
Therefore it is not suitable for a multi-threaded or a multi-processed
environment.

To build more complex dependencies, the DependencyFactory class can
become a bit bloated and difficult to manage as the number of
dependencies increases.

Follow-up Questions:
--------------------

-  What are some of the solutions to handle concurrent requests for
   building dependencies?
-  How to manage DependencyFactory when number of dependencies
   increases?
