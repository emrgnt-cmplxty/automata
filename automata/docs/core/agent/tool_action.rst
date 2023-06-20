ToolAction
==========

``ToolAction`` is a class representing an agent action that interacts
with a specific tool. It provides methods to initialize, access, and
manage the properties of the ToolAction object. The class supports
interaction with various tools and provides a way to execute a query
with a tool using the specified arguments.

Overview
--------

The primary properties of the ``ToolAction`` class are its
``tool_name``, ``tool_query``, and ``tool_args``. The ``tool_name``
property identifies the tool that the action is associated with. The
``tool_query`` contains the query to be executed by the tool, and the
``tool_args`` is a list of arguments to be passed to the tool. The class
also provides utility methods like ``from_lines`` that allows creating a
``ToolAction`` instance from a list of lines.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.agent.action.AutomataActionExtractor.extract_actions``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.graph.SymbolGraph``

Example
-------

The following example demonstrates how to create an instance of
``ToolAction`` with a designated tool and query.

.. code:: python

   from automata.core.agent.action import ToolAction

   tool_name = "example_tool"
   tool_query = "example query"
   tool_args = ["arg1", "arg2"]

   tool_action = ToolAction(tool_name=tool_name, tool_query=tool_query, tool_args=tool_args)

Limitations
-----------

``ToolAction`` class is mainly limited by its simplicity, as it only
stores basic information about a tool action. It does not directly
execute the action nor interact with the associated tool, but rather
serves as a container for the tool action information.

Follow-up Questions:
--------------------

-  How can we directly execute a ``ToolAction`` with a specific tool?
-  What other properties and methods might be useful for the
   ``ToolAction`` class?
