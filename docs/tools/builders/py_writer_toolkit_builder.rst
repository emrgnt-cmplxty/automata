PyWriterToolkitBuilder
======================

``PyWriterToolkitBuilder`` is a class that provides functionalities for
manipulating Python code by interacting with the PythonWriter API.

Overview
--------

``PyWriterToolkitBuilder`` allows you to modify existing Python code or
create new modules. Initialization of an instance requires an instance
of the ``PyWriter`` class, and an optional boolean argument ``do_write``
that defines whether the module is written to disk after updating.

Its ``build`` method provides two functionalities:

1. ``update-module``: This inserts or updates python code of a
   function, class, method in an existing module. It can create new
   objects, modify existing code, or even introduce new import
   statements.
2. ``create-new-module``: It creates a new module at a given
   path with the given code.

Related Symbols
---------------

-  ``automata.tools.base.Tool``: The ``Tool`` class exposes a function
   or coroutine directly which is then used by
   ``PyWriterToolkitBuilder`` to implement its methods.

-  ``automata.tests.unit.test_py_writer_tool.python_writer_tool_builder``:
   This tests the ``PyWriterToolkitBuilder`` and asserts its instance
   type as ``Tool``.

-  ``automata.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``:
   Provides similar method to ``build()`` in ``PyWriterToolkitBuilder``
   to build Python toolkit for OpenAI.

-  ``automata.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``:
   Builds toolkit for handling of context Oracle within OpenAI.

Usage Example
-------------

.. code:: python

   from automata.code_handling.py.writer import PyWriter
   from automata.tools.builders.py_writer import PyWriterToolkitBuilder

   py_writer = PyWriter(py_reader)
   py_toolkit_builder = PyWriterToolkitBuilder(py_writer=py_writer)
   tools = py_toolkit_builder.build()

   for tool in tools:
       print(f"Tool Name: {tool.name}")
       print(f"Tool Description: {tool.description}")

Limitations
-----------

The ``PyWriterToolkitBuilder`` is restricted to working with Python code
only. Additionally, it requires an existing ``PyWriter`` instance during
initialization.

Follow-up Questions:
--------------------

-  Can ``PyWriterToolkitBuilder`` handle non-python code as well?
-  What could be some potential security risks associated with modifying
   python code or creating new modules?
-  What safeguards have been put in to avoid these potential security
   risks?
-  Is there a way to initiate ``PyWriterToolkitBuilder`` without having
   to pass in a ``PyWriter`` instance during initialization?
