AgentToolkitBuilder
===================

``AgentToolkitBuilder`` is an abstract class used for building tools for
various providers. These tools, once built, are associated with the
respective ``AgentToolkitNames``.

Overview
--------

The fundamental purpose of ``AgentToolkitBuilder`` is to offer a
standardized way to create a collection of tools that can be used with
different types of agents, as defined by the ``AgentToolkitNames``.

Given the abstract nature of this class, it doesn’t instantiate any
object on its own, but outlines the requirements for
sub-classes/offspring of the ``AgentToolkitBuilder``.

Related Symbols
---------------

Here are some related classes that build upon or interact with
``AgentToolkitBuilder``:

-  ``ContextOracleOpenAIToolkitBuilder``
-  ``SymbolSearchOpenAIToolkitBuilder``
-  ``PythonAgentToolkit``
-  ``OpenAIAgentToolkitBuilder``
-  ``PyWriterOpenAIToolkitBuilder``

Mandatory Methods
-----------------

The ``AgentToolkitBuilder`` possesses an abstract method named
``build``:

.. code:: python

   @abstractmethod
   def build(self) -> List[Tool]:
       pass

This method, once implemented in the subclasses, is expected to return a
list of ``Tool`` objects.

Example
-------

Let’s provide an example of a class ``PythonAgentToolkit`` which
inherits from ``AgentToolkitBuilder``.

.. code:: python

   from automata.core.tools.base import Tool

   class PythonAgentToolkit:
       def __init__(self, python_agent: PythonAgent):
           self.python_agent = python_agent

       def build(self) -> List[Tool]:
           def python_agent_python_task():
               pass

           tools = [
               Tool(
                   "automata-task",
                   python_agent_python_task,  
                   "Execute a Python task using the PythonAgent. Provide the task description in plain English.",
               )
           ]
           return tools

In this example, the subclass ``PythonAgentToolkit`` implements the
``build`` method to generate a list of ``Tool`` items.

Limitations and Considerations
------------------------------

Since ``AgentToolkitBuilder`` is an abstract class, it should not be
instantiated directly. Instead, create a subclass that implements the
``build`` method. The usage and appropriateness of this class and its
subclasses will depend on the corresponding agent context where this
toolkit would be used.

Follow-up Questions:
--------------------

-  Are there existing subclasses of ``AgentToolkitBuilder`` apart from
   the ones identified?
-  Are there any additional methods that could be part of the
   ``AgentToolkitBuilder``, to be implemented by subclasses?
-  Any specific structures to be maintained in the ``Tool`` objects
   built by the subclasses? How are these ``Tool`` objects expected to
   interact with agents?
