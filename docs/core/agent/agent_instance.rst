AgentInstance
=============

``AgentInstance`` is an abstract class used to implement a unique
occurrence of an agent.

Overview
--------

An AgentInstance is used for creating dynamic agent instances based on
specific agent configurations. It provides a blueprint for creating
multiple agent instances while also facilitating a means to run these
instances. The AgentInstance should be inherited to implement the
``run`` method which can determine the operational logic of the agent.

Import Statements
-----------------

.. code:: python

   from abc import ABC, abstractmethod
   from automata.config.base import AgentConfigName

Related Symbols
---------------

-  ``config.config_enums.AgentConfigName``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.core.agent.instances.OpenAIAutomataAgentInstance``

Example
-------

This example shows how to use the ``AgentInstance.create`` method to
create an agent instance. Inherit the ``AgentInstance`` abstract class
and implement the ``run`` method to create a custom agent instance.

.. code:: python

   from automata.config.base import AgentConfigName
   from automata.core.agent.agent import AgentInstance

   class MyAgent(AgentInstance):
       def run(self, instructions: str) -> str:
           return "Hello, World!"

   config_name = AgentConfigName.TEST
   agent = MyAgent.create(config_name)
   print(agent.run("Hello, World!"))  # Outputs: Hello, World!

Limitations
-----------

The ``AgentInstance`` class lacks default implementations of its core
functionalities. Therefore, it cannot be directly instantiated and must
be subclassed, providing concrete implementations of its abstract
methods.

Follow-up Questions
-------------------

-  How does the ``create`` class method interact with the implementation
   of ``run``?
-  What explicit configurations does ``AgentConfigName`` provide to the
   ``create`` method?
-  How are different agent behaviors handled when building multiple
   instances of the same agent?
