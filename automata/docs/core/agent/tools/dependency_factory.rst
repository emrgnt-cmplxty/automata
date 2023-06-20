DependencyFactory
=================

``DependencyFactory`` is a helper class that creates dependencies
required for configuring ``Toolkit`` constructors. It provides a way to
manage instances of dependencies and can be used in conjunction with
other tools such as ``AgentTool`` and ``Toolkit``.

Overview
--------

``DependencyFactory`` maintains a dictionary of instances that are
created as required. It provides methods to create instances of various
dependencies such as ``PyContextRetriever``, ``SymbolGraph.SubGraph``,
``SymbolSimilarity``, and others. Users can also override dependency
configurations using keyword arguments when initializing the factory.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``base.tool.Tool, Toolkit, ToolkitType``
-  ``config.config_types.ConfigCategory``
-  ``coding.py_coding.retriever.PyCodeRetriever``
-  ``coding.py_coding.writer.PyCodeWriter``
-  ``context.py_context.retriever.PyContextRetriever, PyContextRetrieverConfig``
-  ``database.vector.JSONVectorDatabase``
-  ``embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``embedding.doc_embedding.SymbolDocEmbeddingHandler``
-  ``embedding.embedding_types.OpenAIEmbedding``
-  ``embedding.symbol_similarity.SymbolSimilarity``
-  ``symbol.graph.SymbolGraph``
-  ``symbol.search.rank.SymbolRankConfig``
-  ``symbol.search.symbol_search.SymbolSearch``
-  ``core.utils.config_fpath``

Example
-------

The following is an example demonstrating how to create an instance of
``DependencyFactory`` and retrieve a dependency.

.. code:: python

   from automata.core.agent.tools.tool_utils import DependencyFactory

   factory = DependencyFactory(symbol_graph_path="path/to/symbol/graph")
   symbol_graph = factory.get("symbol_graph")

Limitations
-----------

The primary limitation of ``DependencyFactory`` is that it relies on
pre-defined methods for creating dependency instances. This means that
adding new dependencies requires updates to the class definition.
Furthermore, the class does not support dynamically generating
dependencies, which might be useful for creating instances of
dependencies with custom configurations without having to manually
override the default values.

Follow-up Questions:
--------------------

-  Are there any alternative ways to dynamically generate dependencies
   without having to define methods for each dependency?
