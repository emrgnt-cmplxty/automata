OpenAIAutomataAgentConfig
=========================

``OpenAIAutomataAgentConfig`` is a subclass of ``AgentConfig`` intended
specifically for configuring Automata Agents. This configuration class
provides a set of settings that are used when initializing an instance
of OpenAIAutomataAgent. It integrates with the ``SymbolRank`` mechanism
to aid in the creation of a default formatter for system templates. The
class allows for custom configurations for the automata agent, enabling
dynamic behavior in response to different system needs and setups.

Overview
--------

``OpenAIAutomataAgentConfig`` includes several attributes such as
``system_template``, ``system_template_variables``,
``system_template_formatter``, ``instruction_version``, and
``system_instruction``. These attributes define the model, the session
id, the set of tools of the agent and specify how to handle
instructions, template formation and system responses in a session with
the Automata agent.

The class also includes an inner class ``TemplateFormatter`` which
creates a default formatter that might be utilized for system templates.

The class offers convenient methods to set up agent configurations,
assess if all configured elements are satisfactory, format the system
instructions, and retrieve the provider for the agent.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.config.base.AgentConfigName``
-  ``automata.tests.conftest.automata_agent``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder.create_config``

Usage Example
-------------

The following example demonstrates how to create an instance of
``OpenAIAutomataAgentConfig`` and set up its attributes with the
``setup`` method:

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfig
   from config.config_enums import AgentConfigName
   from automata.core.experimental.search.rank import SymbolRank

   config = OpenAIAutomataAgentConfig.load(AgentConfigName.AUTOMATA_MAIN)
   symbol_rank = SymbolRank()
   config.setup()

In this case, ``AgentConfigName.AUTOMATA_MAIN`` is used as a predefined
configuration but it could be replaced by any other available enum in
``AgentConfigName``.

Limitations
-----------

The current implementation of ``OpenAIAutomataAgentConfig`` does not
have a built-in way of handling configurations that are not
``AgentConfigName.AUTOMATA_MAIN`` or ``AgentConfigName.TEST``. If these
configurations are passed, it raises a ``NotImplementedError``.

Additionally, the ``create_default_formatter`` method is yet to be fully
implemented, and its usefulness will largely depend on pending
instruction configurations.

Follow-up Questions:
--------------------

-  Could the ``OpenAIAutomataAgentConfig`` setup mechanism incorporate
   more input validation to ensure the configured properties meet the
   expectations?
-  Should the ``OpenAIAutomataAgentConfig`` provide methods for handling
   configurations other than ``AUTOMATA_MAIN`` and ``TEST``?
-  How could we improve the creation flexibility of an
   ``OpenAIAutomataAgentConfig`` in order to streamline the
   instantiation of Automata Agents?
-  Will it be beneficial to implement a mechanism to support custom
   default formatters outside of the currently considered
   configurations?
