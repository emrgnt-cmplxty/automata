AgentConfig
===========

``AgentConfig`` class is a configuration base class used for setting up
agent instances in ``automata``. It is an abstract class (as it is
derived from the ``ABC`` class) that outlines the structure and basic
functionality for agent configurations in the package. This class
provides a basis for creating and loading custom agent configurations.

Overview
--------

The ``AgentConfig`` class includes several attributes, such as
``config_name``, ``tools``, ``instructions``, ``description``,
``model``, ``stream``, ``verbose``, ``max_iterations``, ``temperature``,
``session_id``. These attributes hold various information needed to
configure and run an agent.

Additionally, it has methods that must be implemented in subclasses -
``setup()``, ``load()``, and ``get_llm_provider()``. These methods are
crucial for setting up the agent and loading the needed configuration.

A nested ``Config`` class is also included, allowing for further
configuration settings. Using arbitrary types and specifying the
provider for low-level machine (LLM) operations are available within
this nested class.

Attributes
----------

-  ``config_name``: Indicates the name of the agent configuration
   (default is ``AgentConfigName.DEFAULT``).
-  ``tools``: A list of ``Tool`` instances used by the agent.
-  ``instructions``: A string containing instructions for the agent.
-  ``description``: A descriptive string for the agent.
-  ``model``: The model used by the agent.
-  ``stream``: Boolean indicating whether streaming functionality is
   enabled.
-  ``verbose``: Boolean controlling the verbosity of the agent.
-  ``max_iterations``: The maximum number of iterations the agent will
   attempt.
-  ``temperature``: A float controlling the random behaviour of the
   agent.
-  ``session_id``: An optional string describing the current session.

Related Symbols
---------------

-  ``automata.config.base.AgentConfigName``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.core.agent.agent.AgentInstance.Config``
-  ``automata.tests.unit.test_task_environment.TestURL``
-  ``automata.core.agent.instances.OpenAIAutomataAgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``

Example Usage
-------------

The following example shows how to create a subclass of ``AgentConfig``.
In the subclass, abstract methods are implemented and additional
configurations are set.

.. code:: python

   from automata.config.base import AgentConfig, ConfigCategory
   from automata.config.base import AgentConfigName, LLMProvider

   class CustomAgentConfig(AgentConfig):
       def __init__(self, **data: Any):
           super().__init__(**data)
           self.custom_attribute = ''

       def setup(self) -> None:
           pass
       
       @classmethod
       def load(cls, config_name: AgentConfigName) -> "CustomAgentConfig":
           loaded_yaml = cls._load_automata_yaml_config(config_name)
           return CustomAgentConfig(**loaded_yaml)

       @staticmethod
       def get_llm_provider() -> LLMProvider:
           return LLMProvider.OPENAI

   custom_config = CustomAgentConfig.load(AgentConfigName.AUTOMATA_MAIN)

Limitations
-----------

As ``AgentConfig`` is an abstract base class, it can’t be instantiated
directly. All abstract methods ``setup()``, ``load()``, and
``get_llm_provider()`` must be implemented in any subclass. It also
assumes a specific file structure for loading YAML configurations and
will raise errors if it can’t locate the necessary files.

Follow-up Questions:
--------------------

-  How can we handle custom YAML file structures in subclasses of
   ``AgentConfig``?
-  Can we add a method to validate the content of the loaded YAML
   configuration file?
