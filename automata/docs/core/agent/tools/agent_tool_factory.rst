AgentToolFactory
================

``AgentToolFactory`` is a class for creating tool managers to be
utilized by providers in their tasks. This factory class generates specific
tool managers based on the toolkit type and ensures that all the
required arguments are correctly provided to construct the desired agent
tool.

Overview
--------

``AgentToolFactory`` provides a static method ``create_agent_tool`` that
takes the ``ToolkitType`` and required arguments to create the specified
agent tool. The primary function of this class is to create a tool
manager that takes care of generating and managing toolkits for further
use. This class also maintains the mappings of toolkit types to tool
class and arguments.

Related Symbols
---------------

-  ``automata.core.tools.tool.ToolkitType``
-  ``automata.core.toolss.agent_tool.AgentTool``
-  ``automata.core.toolss.py_code_retriever.PyCodeRetrieverTool``
-  ``automata.core.toolss.context_oracle.ContextOracleTool``
-  ``automata.core.toolss.py_code_writer.PyCodeWriterTool``
-  ``automata.core.toolss.symbol_search.SymbolSearchTool``
-  ``automata.core.toolss.tool_utils.DependencyFactory``
-  ``automata.core.toolss.tool_utils.UnknownToolError``
-  ``automata.core.toolss.tool_utils.ToolCreationError``

Example
-------

The following example demonstrates the usage of
``AgentToolFactory.create_agent_tool()`` to create a
``SymbolSearchTool``.

.. code:: python

   from automata.core.toolss.tool_utils import AgentToolFactory
   from automata.core.tools.tool import ToolkitType
   from automata.core.experimental.search.symbol_search import SymbolSearch
   from automata.core.symbol_embedding.similarity import SymbolSimilarity
   from automata.core.symbol.graph import SymbolGraph
   from automata.tests.unit.test_base_tool import mock_tool

   symbol_search = SymbolSearch(SymbolGraph(), SymbolSimilarity(mock_tool))
   toolkit_type = ToolkitType.SYMBOL_SEARCHER
   agent_tool = AgentToolFactory.create_agent_tool(toolkit_type,
       symbol_search=symbol_search,
       symbol_doc_similarity=SymbolSimilarity(mock_tool)
   )

**Note:** In the example, the ``mock_tool`` used is just for
illustration purposes. In a real-world scenario, proper instances of
``SymbolEmbeddingHandler`` should be used.

Limitations
-----------

One limitation of ``AgentToolFactory`` is that the mappings between
toolkit types, tool classes, and required arguments are maintained
locally within the class. A dynamic method of generating these mappings,
such as decorator on the tool classes, would lead to more maintainable
and scalable code.

Follow-up Questions:
--------------------

-  Are there any plans for implementing a dynamic method to generate the
   toolkit type to tool class and required arguments mappings?
