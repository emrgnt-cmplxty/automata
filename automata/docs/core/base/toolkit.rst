Toolkit
=======

``Toolkit`` is a collection of tools that provide various
functionalities. It contains a list of tools and supports adding and
using tools.

Overview
--------

The ``Toolkit`` class provides an interface to store and manage a
collection of tools. A tool is a callable object, like a Python function
or a coroutine that takes a string input and returns a string output
with additional metadata. The ``Toolkit`` class has a ``__repr__``
method to provide a string representation of the toolkit.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.base.toolkit.List``
-  ``automata.core.base.toolkit.Optional``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

The following example demonstrates how to create an instance of
``Toolkit`` with a list of tools.

.. code:: python

   from automata.core.base.tool import Tool
   from automata.core.base.toolkit import Toolkit

   # Define example tools
   def tool_one(input: str) -> str:
       return f"Tool One: {input}"

   def tool_two(input: str) -> str:
       return f"Tool Two: {input}"

   tool_list = [
       Tool(name="Tool One", func=tool_one, description="Example Tool One"),
       Tool(name="Tool Two", func=tool_two, description="Example Tool Two")
   ]

   # Create a Toolkit instance
   my_toolkit = Toolkit(tools=tool_list)

   # Display the Toolkit
   print(my_toolkit)

Limitations
-----------

The primary limitation from using the ``Toolkit`` class is that it
requires a specific structure for the tools that are to be added. The
tools must be instances of the ``Tool`` class or other subclasses that
extend ``BaseTool``. This limitation enforces a level of consistency,
but may restrict rapid prototyping and quick addition of tools that are
not in the desired format.

Follow-up Questions:
--------------------

-  Is there a more flexible way to add tools to a toolkit yet still
   maintain readability and maintainability of the code?
-  Can we provide wrapper functions to automatically convert functions
   to Tool instances for a more convenient addition to the toolkit?
