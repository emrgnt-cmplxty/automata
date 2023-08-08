DependencyFactory
=================

``DependencyFactory`` is a Singleton class that is responsible for
creating and managing dependencies that are required for tool
construction. It serves as a centralized location to handle
dependencies, allowing a single point of access to share, coordinate and
manage these dependencies for avoiding conflicts and minimizing
redundancy.

Overview
--------

``DependencyFactory`` provides various methods to get, set, reset and
directly create dependencies. When creating dependencies, it also
supports specification and override of keyword arguments during
initialization. Internally, it maintains a cache of class instances
promoting efficiency.

It can be used to create dependencies like SymbolGraph, SymbolRank,
SymbolSearch, etc. It also supports retrieving pre-created instances of
dependencies, building dependencies required for a given set of tools,
and even allows to override the creation parameters for dependencies.

Related Symbols
---------------

-  ``automata.singletons.Singleton``
-  ``automata.utils.symbol_provider.SynchronizationContext, ISymbolProvider``
-  ``automata.base_config.SymbolRankConfig, PyContextHandlerConfig, EmbeddingDataCategory``
-  ``automata.structures.SymbolGraph, SymbolRank, SymbolSearch``
-  ``automata.embedding_handler.SymbolCodeEmbeddingHandler, SymbolDocEmbeddingHandler``
-  ``automata.py_context.PyContextHandler, PyContextRetriever``
-  ``automata.py_io.PyReader, PyCodeWriter``
-  ``automata.exceptions.UnknownToolError``
-  ``automata.toolkits.agent_tool.Toolkits, AgentToolkitNames, AgentToolFactory``

Example
-------

This example demonstrates how to initialize a ``DependencyFactory`` and
create a SymbolGraph instance:

.. code:: python

   from automata.singletons.dependency_factory import DependencyFactory
   from automata.utils.interface import EmbeddingDataCategory
   from automata.base_config import get_embedding_data_fpath

   factory = DependencyFactory()
   symbol_graph = factory.get('symbol_graph')

In the above example, ``symbol_graph`` will have the instance returned
by the ``create_symbol_graph`` method of the ``DependencyFactory``. The
instance creation is cached, all further calls to
``get('symbol_graph')`` will return the same instance.

Returning custom ``SymbolGraph`` instance with overridden arguments:

.. code:: python

   factory = DependencyFactory(symbol_graph_scip_fpath="/custom/path/to/scip")
   symbol_graph = factory.get('symbol_graph')

``symbol_graph`` in this case will be the instance created using the
overridden ``scip_filepath``.

Resetting all dependencies:

.. code:: python

   factory.reset()

After calling ``reset()``, all cached dependencies are cleared and
``factory.get('symbol_graph')`` will create a new SymbolGraph.

Limitations
-----------

-  It is important to understand that the behavior of ``get`` method
   will differ based on when it is called, especially if overrides have
   been set.
-  If setting overrides after Dependency Factory has already created
   dependencies, ``Dependency Factory`` will not allow and raise
   ValueError. It is suggested to set the overrides during
   initialization or just after, prior to creating any dependencies.
-  Depending upon the argument values provided, object creation might
   fail. Make sure the arguments are in their expected formats and
   contain the correct values.

Follow-up Questions:
--------------------

-  How does DependencyFactory handle object initialization errors when
   creating dependencies?
-  What happens when an invalid argument is passed to the get method, is
   there a default response mechanism?
