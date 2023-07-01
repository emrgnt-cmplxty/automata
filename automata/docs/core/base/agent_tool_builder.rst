AgentToolkit
================

``AgentToolkit`` is an abstract class for building tools for
providers. Tools are essential components as they define the
functionality and behavior of an agent. The ``AgentToolkit`` class
provides a standard interface for creating tools. This class should be
inherited by classes implementing specific tool creation logic.

Overview
--------

The primary method in the ``AgentToolkit`` class is ``build()``.
This method returns a list of ``Tool`` objects. To implement a custom
tool builder, inherit from the ``AgentToolkit`` class and override
the ``build`` method to define the tool creation logic.

Related Symbols
---------------

-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.tool.tool_utils.AgentToolFactory``
-  ``automata.core.agent.tool.builder.py_writer.PyWriterOpenAIToolkit``
-  ``automata.core.agent.tool.builder.py_reader.PyReaderOpenAIToolkit``

Example
-------

The following example demonstrates how to create a custom tool builder
that inherits the ``AgentToolkit`` class.

.. code:: python

   from automata.core.base.agent import AgentToolkit
   from automata.core.base.tool import Tool

   class CustomToolkit(AgentToolkit):
       def build(self) -> List[Tool]:
           # Implement tool creation logic here
           tools = []
           return tools

Limitations
-----------

As ``AgentToolkit`` is an abstract base class, it does not contain
any implementation details for tool building. To leverage this class,
you must create a concrete subclass that implements the ``build``
method.

Follow-up Questions:
--------------------

-  Are there any built-in tools or builders that can be used as examples
   for creating custom tools?
-  What are the best practices for organizing and managing custom tools?
-  Are there any performance implications when scaling up the number of
   tools in a custom builder?
