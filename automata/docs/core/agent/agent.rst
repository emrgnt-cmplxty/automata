Agent
=====

``Agent`` is an abstract base class representing an autonomous entity
that can perform actions and communicate with other providers in the
context of Automata. Derived classes from ``Agent`` should implement the
``iter_step``, ``run`` and ``set_coordinator`` abstract methods.
``Agent`` provides the basic structure for different types of providers
that can be used in the Automata system.

Overview
--------

To create a custom agent, you should inherit from the ``Agent`` base
class and define the abstract methods based on your agent’s purpose. The
agent should be able to perform actions by implementing the
``iter_step`` and ``run`` methods. Additionally, the agent should be
able to interact with an ``AutomataCoordinator`` by implementing the
``set_coordinator`` method. This will allow them to be managed and
communicate with other providers within the same coordinator.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.agent.coordinator.AutomataCoordinator``
-  ``automata.tests.unit.test_automata_coordinator.test_set_coordinator_main``

Example
-------

Below is an example of how to create a custom agent that inherits from
the ``Agent`` base class:

.. code:: python

   from automata.core.agent.agent import Agent
   from automata.core.coordinator.automata_coordinator import AutomataCoordinator
   from typing import Optional, Tuple
   from automata.core.base.openai import OpenAIChatMessage

   class MyCustomAgent(Agent):
       def iter_step(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
           # Perform specific actions for your custom agent here
           return some_action_output
           
       def run(self) -> str:
           # Implement the main logic for your custom agent here
           return some_result
         
       def set_coordinator(self, coordinator: AutomataCoordinator) -> None:
           # Set the AutomataCoordinator instance for your custom agent here
           self.coordinator = coordinator

Limitations
-----------

As ``Agent`` is an abstract base class, it cannot be directly
instantiated and must be subclassed. The abstract methods must be
implemented in the derived class to properly define the agent’s behavior
and interaction with the ``AutomataCoordinator``.

Follow-up Questions:
--------------------

-  How can the derived class interact with other providers in the Automata
   system?
-  What additional methods or attributes should be added to the
   ``Agent`` abstract base class to support a wider range of agent
   types?
