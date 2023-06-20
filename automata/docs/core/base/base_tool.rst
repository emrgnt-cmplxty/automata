BaseTool
========

``BaseTool`` is a class responsible for defining a tool or skill for an
LLM. The class provides the base structure and methods for running a
tool synchronously or asynchronously. Other classes can inherit from
``BaseTool`` to implement their custom logic.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.agent.AutomataAgent``

Methods
-------

The ``BaseTool`` class provides the following methods:

``__call__(self, tool_input: Tuple[Optional[str], ...]) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows the tools to be callable with a string input. It
calls the ``run`` method with the given ``tool_input``.

``async arun(self, tool_input: Tuple[Optional[str], ...]) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method runs the tool asynchronously, using the internally defined
``_arun`` method with the given ``tool_input``.

``run(self, tool_input: Tuple[Optional[str], ...]) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method runs the tool synchronously, using the internally defined
``_run`` method with the given ``tool_input``.

Example
-------

To define a custom tool, inherit the ``BaseTool`` class and implement
the ``_run`` method. The following example demonstrates a simple tool
that generates the reverse of a given string.

.. code:: python

   from automata.core.base.base_tool import BaseTool

   class ReverseTool(BaseTool):
       def __init__(self):
           super().__init__(name="Reverse String", description="Reverses a given string")

       def _run(self, tool_input):
           return tool_input[0][::-1]

   reverse_tool = ReverseTool()
   result = reverse_tool("hello")
   print(result)  # Output: olleh

Limitations
-----------

The primary limitation of ``BaseTool`` is that it does not provide
concrete implementations of the ``_run`` and ``_arun`` methods. It is
intended as a base class for inheriting and implementing actual tools.

Follow-up Questions:
--------------------

-  What are some common use-cases where the synchronous ``run`` method
   is preferred over the asynchronous ``arun`` method?
