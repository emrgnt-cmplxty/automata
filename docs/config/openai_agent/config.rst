OpenAIAutomataAgentConfig.Config
================================

The ``OpenAIAutomataAgentConfig.Config`` class is a configuration class
that is used within ``OpenAIAutomataAgentConfig``. It manages
configurations related to OpenAI models and set up parameters for the
Automata agent such as which OpenAI engine models are supported and
whether arbitrary types are allowed.

The computation setup and the model are crucial elements while building
an agent. This class provides configurations for such important elements
enabling developers to build and utilize the agents effectively.

Overview
--------

The class includes attributes such as ``SUPPORTED_MODELS`` and
``arbitrary_types_allowed``. The ``SUPPORTED_MODELS`` attribute is a
list of OpenAI engine model names that identifies which models are
supported to help ensure compatibility and performance. The
``arbitrary_types_allowed`` attribute dictates whether arbitrary types
are allowed in the model.

Related Symbols
---------------

-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``

Example
-------

Here is an example of how you might build and use an
``OpenAIAutomataAgentConfig`` with a specified model:

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfig
   from automata.config.base import AgentConfigName

   config = OpenAIAutomataAgentConfig.Config()
   config_name = AgentConfigName.AUTOMATA_MAIN # get config name
   config.model = "gpt-4"  # Set model
   config.arbitrary_types_allowed = True

Limitations
-----------

``OpenAIAutomataAgentConfig.Config`` can only use the predefined models
listed in ``SUPPORTED_MODELS``. If you need to use a different model,
you would need to update the ``SUPPORTED_MODELS`` attribute in the
class.

Follow-up Questions:
--------------------

-  Currently, the class uses a hard-coded list for supported models. Can
   it potentially support all models in the future?
-  How does the class handle arbitrary types in a safe and performant
   manner?
