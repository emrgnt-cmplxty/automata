AgentTool
=========

``AgentTool`` is an abstract class for building tools for providers. This
class provides a structure for creating custom tools to be used in an
agent’s toolkit. Being an abstract class, it contains an abstract method
``build`` that needs to be implemented by any concrete class that
extends ``AgentTool``.

Related Symbols
---------------

-  ``automata.core.base.tool.Tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.tests.unit.test_base_tool.MockTool``
-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.base.tool.Toolkit``

Example
-------

Here is an example demonstrating how to create a custom tool by
extending the ``AgentTool`` class:

.. code:: python

   from automata.core.agent.tools.agent_tool import AgentTool
   from typing import Any

   class CustomTool(AgentTool):
       def __init__(self, **kwargs) -> None:
           super().__init__(**kwargs)
       
       def build(self) -> Any:
           # Implementation of the build method
           pass

Limitations
-----------

As an abstract class, ``AgentTool`` cannot be instantiated directly. It
must be extended by a concrete class that provides an implementation for
the ``build`` method. A potential limitation of this abstract class is
that it may not offer enough flexibility for all types of custom tools,
in which case it would be necessary to create a new abstract class or
directly implement all logic in a concrete tool class.

Follow-up Questions:
--------------------

-  Are there any alternative patterns for designing agent tools that
   provide more flexibility?
-  How can mock objects be replaced with the actual underlying objects
   within the examples provided, if possible?
