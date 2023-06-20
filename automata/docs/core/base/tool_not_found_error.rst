ToolNotFoundError
=================

``ToolNotFoundError`` is a custom exception class that is raised when a
tool is not found while using the ``automata`` package. This class
inherits from the ``BaseException`` class. The exception contains a
``tool_name`` attribute that represents the name of the tool that was
not found.

Overview
--------

``ToolNotFoundError`` is used to signal errors in finding tools in the
``automata`` software suite. It is commonly used in the
``automata.core.base`` module, particularly in the ``BaseTool`` class
when an operation involves using a tool that does not exist.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.symbol.symbol_types.Symbol``

Example
-------

The following example shows how to raise a ``ToolNotFoundError``:

.. code:: python

   from automata.core.base.tool import ToolNotFoundError

   try:
       # code that may result in a nonexistent tool being requested
       raise ToolNotFoundError("my_tool")
   except ToolNotFoundError as e:
       print(e)  # Output: Error: Tool 'my_tool' not found.

Limitations
-----------

``ToolNotFoundError`` is a relatively simple exception class that only
provides an error message indicating the tool name that was not found.
It does not provide additional information about why the tool was not
found or where the user might look to find or install the missing tool.

Follow-up Questions:
--------------------

-  How can we extend ``ToolNotFoundError`` to provide more informative
   error messages, such as suggesting potential alternatives or
   installation instructions for the missing tool?
