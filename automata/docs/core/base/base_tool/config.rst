BaseTool
========

``BaseTool`` is a base class from which specific tools can inherit when
building tools for the Automata ecosystem. The tools are designed to
automate tasks and interact with various systems. The ``BaseTool`` class
provides a flexible foundation for creating new tools and managing their
configurations, as well as organizing them within toolkits.

Overview
--------

``BaseTool`` primarily serves as a base class to be inherited by other
classes when creating custom tools. The class contains a ``Config``
class, which defines configuration options for the tool. It also
provides methods to be implemented or overridden by the inheriting
subclasses.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``

Example
-------

The following example shows how to create a custom tool class by
inheriting from ``BaseTool``:

.. code:: python

   from automata.core.base.base_tool import BaseTool

   class CustomTool(BaseTool):

       def __init__(self, name: str, description: str):
           super().__init__(name=name, description=description)

       def execute(self, *args, **kwargs):
           # Implement the functionality of the custom tool
           pass

   tool = CustomTool(name="example_tool", description="A custom tool example")

Limitations
-----------

The primary limitation of ``BaseTool`` is that it only offers a
foundation for creating tools. Developers need to subclass and implement
or override the required methods to create functional tools. Also, the
functional scope of the tools is determined by the developer and may be
limited by the libraries and systems they integrate with.

Follow-up Questions:
--------------------

-  What are the best practices for creating new tools within the
   Automata ecosystem?
-  How do I integrate custom tools within the Automata Agent and
   coordinate their usage?
