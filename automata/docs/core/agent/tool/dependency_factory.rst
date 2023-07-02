DependencyFactory
=================

``DependencyFactory`` is a utility class that creates dependencies for
constructing input ``Tool`` objects. It allows users to customize
specific dependencies by providing keyword arguments. The class
maintains a dictionary of instances for each dependency and initializes
them when requested. Caching of dependency instances is achieved using
the ``classmethod_lru_cache`` decorator that provides an LRU cache for
class methods. ``DependencyFactory`` supports various features like
symbol code similarity, symbol search, Python context retrieval, and
other functionalities.

Related Symbols
---------------

-  ``automata.core.tools.tool_utils.classmethod_lru_cache``
-  ``automata.core.code_handling.py.reader.PyReader``
-  ``automata.core.code_handling.py.writer.PyWriter``
-  ``automata.core.base.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.core.retrievers.py.context.PyContextRetrieverConfig``
-  ``automata.core.agent.error.AgentGeneralError``

Example
-------

Here is a simple example demonstrating the usage of
``DependencyFactory``:

.. code:: python

   from automata.core.tools.tool_utils import DependencyFactory

   inst_factory = DependencyFactory()
   symbol_search = inst_factory.get("symbol_search")
   print(symbol_search)

Limitations
-----------

``DependencyFactory`` creates instances for different dependencies
during runtime according to the user’s requirements. However, it relies
on the names of the dependencies (corresponding to the method names in
the class) to create them. If a dependency is not found, it raises an
``AgentGeneralError``. Also, the class assumes specific default
configurations for each dependency and may not cover all use cases for
customization.

Follow-up Questions:
--------------------

-  Are there any specific scenarios where the provided default
   configurations are not suitable?
-  How can we improve the error handling system related to dependency
   initialization in ``DependencyFactory``?
