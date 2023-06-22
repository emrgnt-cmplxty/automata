AutomataInstance
================

``AutomataInstance`` is a base class for creating specific instances of
Automata agents. It serves as a foundation to define specific Automata
agents with different configurations, descriptions, and behaviors.
Instances of Automata agents can then be managed by the
``AutomataCoordinator`` to execute instructions and coordinate the work
of the agents.

Overview
--------

The ``AutomataInstance`` class provides an interface to create and
manage different Automata agent instances. It helps specify the
configuration and the description of the agent, while also providing a
method to run instructions in the context of the agent. The class works
alongside the ``AutomataCoordinator`` and other related symbols such as
``AgentConfigName`` and ``AutomataAgent``.

Related Symbols
---------------

-  ``automata.core.agent.coordinator.AutomataInstance.Config``
-  ``automata.tests.unit.test_automata_coordinator.MockAutomataInstance``
-  ``automata.core.agent.coordinator.AutomataInstance``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.agent.coordinator.AutomataCoordinator``

Example
-------

The following example demonstrates how to create an instance of a custom
Automata agent by subclassing ``AutomataInstance``.

.. code:: python

   from automata.core.agent.coordinator import AutomataInstance
   from automata.config.config_types import AgentConfigName

   class CustomAutomataInstance(AutomataInstance):
       def __init__(
           self,
           config_name: AgentConfigName,
           description: str,
       ):
           super().__init__(config_name=config_name, description=description)

       def run(self, instruction):
           return f"Executing {instruction} on {self.config_name.value}."

   # Create a custom AutomataInstance
   config_name = AgentConfigName.AUTOMATA_MAIN
   description = "Custom Automata Agent"
   custom_instance = CustomAutomataInstance(config_name=config_name, description=description)

   # Run custom instance with an instruction
   instruction = "Example task"
   result = custom_instance.run(instruction)
   print(result)

Limitations
-----------

``AutomataInstance`` serves as a base class for instances of Automata
agents and does not include any specific implementation for performing
tasks. You need to create a subclass of ``AutomataInstance`` and define
the ``run()`` method on it to execute instructions. Moreover, the class
relies on ``AgentConfigName`` for configuration settings, which can only
be loaded from predefined configuration files.

Follow-up Questions:
--------------------

-  How can more complex behaviors be implemented in subclasses of
   ``AutomataInstance``?
