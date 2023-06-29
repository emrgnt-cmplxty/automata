AgentConfig
===========

``AgentConfig`` is an abstract base class that provides a template for
configurations related to providers. It contains abstract methods like
``setup()`` and ``load()`` that need to be implemented by subclasses.
This class also handles the configuration of arbitrary types during the
initialization.

Overview
--------

``AgentConfig`` is designed for ensuring configurability of providers.
Subclasses need to provide implementations for the ``setup()`` and
``load()`` methods in order to properly define the behavior during the
agent setup and configuration loading processes. This class follows the
BaseModel design, making it easy to extend and customize according to
specific agent requirements.

Related Symbols
---------------

-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.tests.unit.test_task_environment.TestURL``
-  ``automata.core.base.agent.AgentInstance.Config``

Example
-------

The following example demonstrates how to create a custom agent
configuration by extending the ``AgentConfig`` class:

.. code:: python

   from config.config_types import AgentConfig

   class CustomAgentConfig(AgentConfig):

       def setup(self):
           # Define your custom agent setup process
           pass

       @classmethod
       def load(cls, config_name: AgentConfigName) -> "CustomAgentConfig":
           # Load the config for your custom agent
           pass

Limitations
-----------

``AgentConfig`` itself is an abstract class and cannot directly be
instantiated. It must be subclassed, and its methods need to be
implemented by the extending class according to the specific agent
requirements. Additionally, the current implementation allows for
arbitrary types, which may lead to code that is not type-safe.

Follow-up Questions:
--------------------

-  How can we ensure type safety while maintaining the flexibility and
   customizability provided by ``AgentConfig``?
