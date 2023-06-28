AutomataAgentConfigFactory
==========================

``AutomataAgentConfigFactory`` is a factory class that provides a way to
create an ``AutomataAgentConfig`` instance from the provided arguments.
It contains a single static method ``create_config(*args, **kwargs)``
that creates an instance of ``AutomataAgentConfig`` using the provided
arguments.

Overview
--------

The class is useful for creating customized instances of
``AutomataAgentConfig`` based on user-defined settings. It ensures that
the created config instances are validated and set up correctly. The
``create_config`` method takes various arguments and keyword arguments
to construct and define an ``AutomataAgentConfig`` instance, then
returns it.

Related Symbols
---------------

-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.core.agent.agents.AutomataOpenAIAgent``
-  ``automata.tests.conftest.automata_agent``

Example
-------

Here is an example demonstrating how to create an
``AutomataAgentConfig`` instance using ``AutomataAgentConfigFactory``.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigFactory
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   automata_agent_config = AutomataAgentConfigFactory.create_config(main_config_name=config_name, model="gpt-4", verbose=True)

Limitations
-----------

The primary limitation of the ``AutomataAgentConfigFactory`` is that its
functionality is quite specific to the use case of creating an
``AutomataAgentConfig`` instance. It is not a general-purpose factory
class that can be used for other purposes.

Follow-up Questions:
--------------------

-  How can we extend the functionality of ``AutomataAgentConfigFactory``
   to support more types of agent configurations?
