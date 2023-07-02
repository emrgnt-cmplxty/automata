ToolkitType
===========

The ``ToolkitType`` is an enumeration class that represents various
types of toolkits available in the automata project. The enumeration is
used to identify and manage different toolkits that can be used by the
Automata tools system.

Overview
--------

The current supported ``ToolkitType`` enumeration values include:

-  ``PY_RETRIEVER``: Represents a toolkit for Python retrieval
   operations.
-  ``PY_WRITER``: Represents a toolkit for Python writing operations.
-  ``SYMBOL_SEARCHER``: Represents a toolkit for searching and
   identifying symbols.
-  ``CONTEXT_ORACLE``: Represents an oracle toolkit for generating
   context.

Related Symbols
---------------

-  ``automata.core.tools.tool.Toolkit``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.toolss.tool_utils.UnknownToolError``

Example
-------

Here is an example of using ``ToolkitType``:

.. code:: python

   from automata.core.tools.tool import ToolkitType

   toolkit_type = ToolkitType.PY_RETRIEVER
   print(toolkit_type.name)

This will output:

::

   PY_RETRIEVER

Limitations
-----------

The ``ToolkitType`` enum class does not have any direct methods or
functionality associated with it, and it can be used only to define or
recognize the type of toolkit being used for an operation. The
enumeration values available in the class need to be manually extended
to support more toolkit types in the future.

Follow-up Questions:
--------------------

-  What are the specific use cases for each toolkit type?
