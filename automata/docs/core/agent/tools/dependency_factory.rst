DependencyFactory
=================

``DependencyFactory`` is a class responsible for creating dependencies
for input Toolkit construction. It provides methods to create instances
of various classes like ``PyContextRetriever``,
``SymbolGraph.SubGraph``, ``SymbolSimilarity``, ``SymbolGraph``, and
``SymbolSearch``. These instances are constructed based on the
dependencies required and can also be fetched by their names using the
``get`` method.

Related Symbols
---------------

-  ``automata.core.toolss.agent_tool.AgentTool``
-  ``automata.core.toolss.context_oracle.ContextOracleTool``
-  ``automata.core.toolss.py_code_retriever.PyCodeRetrieverTool``
-  ``automata.core.toolss.py_code_writer.PyCodeWriterTool``
-  ``automata.core.toolss.symbol_search.SymbolSearchTool``
-  ``automata.core.tools.tool.Toolkit``

Example
-------

The following is an example demonstrating how to use
``DependencyFactory`` to create various instances and get them by their
dependency names.

.. code:: python

   from automata.core.toolss.tool_utils import DependencyFactory

   dependency_factory = DependencyFactory()
   py_context_retriever = dependency_factory.get("py_context_retriever")
   subgraph = dependency_factory.get("subgraph")
   symbol_code_similarity = dependency_factory.get("symbol_code_similarity")
   symbol_doc_similarity = dependency_factory.get("symbol_doc_similarity")
   symbol_graph = dependency_factory.get("symbol_graph")
   symbol_search = dependency_factory.get("symbol_search")

Limitations
-----------

One primary limitation of ``DependencyFactory`` is that to support a new
dependency, the respective ``create_`` method must be added to the
class. This imposes a constraint where the class has to be updated for
every new dependency required.

Follow-up Questions:
--------------------

-  How can the DependencyFactory be extended to support new dependencies
   without the need for updating the class with new ``create_`` methods?
