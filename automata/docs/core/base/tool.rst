Tool
====

``automata.core.base.tool.Tool`` is a class that provides a way to
create a Tool object that directly takes in a function or coroutine. A
Tool is an extendable utility program that can perform specific tasks.
The ``Tool`` class inherits from
``automata.core.base.base_tool.BaseTool`` and is initialized with a
``name``, ``func``, and ``description``.

Overview
--------

``Tool`` provides a convenient way to create a callable tool or utility
that can be used by the agent. The ``Tool`` class takes a ``name``, a
``func`` which can be a function or coroutine, and a ``description`` for
the tool during initialization. The class takes care of the
initialization process, making it easy to create a tool that performs a
specific task.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.agent.action.AutomataActionExtractor.extract_actions``
-  ``automata.core.base.base_tool.BaseTool``

Example
-------

The following is an example demonstrating how to create an instance of
``Tool`` with a custom function.

.. code:: python

   from automata.core.base.tool import Tool

   def custom_function(input_string):
       return input_string.upper()

   tool = Tool(
       name="UpperCase",
       func=custom_function,
       description="A simple tool that converts the input string to upper case."
   )

   output = tool("hello world")
   print(output)  # Output: "HELLO WORLD"

Limitations
-----------

``Tool`` objects rely on the developer providing a correctly implemented
function or coroutine for their intended functionality. An incorrectly
implemented function or coroutine could lead to unexpected behavior or
errors during the execution of the tool.

Follow-up Questions:
--------------------

-  What happens if an incorrect function or coroutine is provided during
   initialization of a ``Tool`` object?
