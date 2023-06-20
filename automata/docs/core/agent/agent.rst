Agent
=====

``Agent`` is an abstract base class representing an autonomous entity
that can perform actions and communicate with other agents. It provides
the necessary methods for performing operations, coordinating with other
instances, and running iterative tasks. It serves as a base class for
concrete agent implementations that interact with system components and
perform tasks.

Overview
--------

``Agent`` provides abstract methods that must be implemented by its
subclasses to handle specific tasks or interaction details. This
flexibility allows developers to create custom agent implementations
that fulfill diverse requirements and work seamlessly across different
domains.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.coordinator.AutomataCoordinator``

Key Methods
-----------

iter_step
~~~~~~~~~

.. code:: python

   @abstractmethod
   def iter_step(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
       pass

This is an abstract method that should be implemented by subclasses to
return a tuple containing an ``OpenAIChatMessage`` representing an input
and an ``OpenAIChatMessage`` representing a system response, or ``None``
if the agent has completed its task.

run
~~~

.. code:: python

   @abstractmethod
   def run(self) -> str:
       pass

This is an abstract method, which should be implemented by subclasses to
execute the agent’s primary task and return the result as a string.

set_coordinator
~~~~~~~~~~~~~~~

.. code:: python

   @abstractmethod
   def set_coordinator(self, coordinator: "AutomataCoordinator"):
       pass

This is an abstract method, which should be implemented by subclasses to
set a coordinator for the agent. This coordinator is responsible for
managing ``AutomataInstance`` objects and coordinating their execution.

Example
-------

The ``Agent`` class is an abstract base class, and as such, cannot be
directly instantiated. You should create a subclass of ``Agent`` and
implement its abstract methods to define the specific behavior of your
agent.

.. code:: python

   from automata.core.agent.agent import Agent

   class MyAgent(Agent):
       def iter_step(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
           # Implement the logic for iter_step
           pass

       def run(self) -> str:
           # Implement the logic for run
           pass

       def set_coordinator(self, coordinator: "AutomataCoordinator"):
           # Implement the logic for set_coordinator
           pass

Limitations
-----------

As an abstract base class, the ``Agent`` class cannot be instantiated
directly. It only provides the blueprint for creating custom agents and
requires users to define specific agent implementations by extending
this base class.

Follow-up Questions:
--------------------

-  Can you provide examples of concrete agent implementations that
   inherit from the ``Agent`` class?
