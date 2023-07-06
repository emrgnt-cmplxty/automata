OpenAIAutomataAgentConfig
=========================

``OpenAIAutomataAgentConfig`` is an agent configuration class for the
Automata OpenAI Agent. It extends the ``AgentConfig`` abstract base
class and is designed to hold the configuration settings for the OpenAI
agent. These settings include the agent’s system template, template
variables and formatter, instruction version, system instruction, and
other configuration parameters.

Overview
--------

The ``OpenAIAutomataAgentConfig`` class defines the necessary
configuration settings for an OpenAI-powered Automata agent. The
parameters for this agent configuration include the system template,
system template variables, instruction version, and a system
instruction, among others. This class also includes a ``setup`` method
that ensures the necessary class attributes are properly initialized.

The class also consists of a ``TemplateFormatter`` and a ``load``
method. The ``TemplateFormatter`` is a static class that provides a
method to create a default formatter for the given configuration while
the ``load`` method is used to load the configuration for an agent based
on the given ``config_name``.

However, usage of the class revolves generally around initializing it,
calling the ``setup`` and ``load`` methods when necessary, and utilizing
the configuration in an OpenAI Automata Agent.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``:
   This method tests whether the config builder can correctly create an
   instance of the OpenAIAutomataAgentConfig class.
-  ``automata.tests.conftest.automata_agent_config_builder``: This is a
   fixture that provides a builder for the OpenAIAutomataAgentConfig
   class.
-  ``automata.core.agent.providers.OpenAIAutomataAgent``: This class
   utilizes the OpenAIAutomataAgentConfig for operational settings
   during its instantiation and behavior.
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``:
   This method tests the initialization of the AutomataAgent with the
   corresponding configuration.

Example
-------

Here is an example of creating an instance of
``OpenAIAutomataAgentConfig`` using a predefined configuration name.

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfig
   from automata.config.base import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = OpenAIAutomataAgentConfig.load(config_name)

Limitations
-----------

The main limitation of the ``OpenAIAutomataAgentConfig`` is its
dependence on specific configurations and enum values. It’s currently
limited to a set of supported models, and the ``load`` method relies on
the ``AgentConfigName`` enum for loading the configuration. Hence,
custom configuration beyond these narrow bounds may not be possible.
Furthermore, it’s particularly critical that the keys in the
``system_template_formatter`` match exactly with
``system_template_variables``, resulting in a potential source of error
if not met.

Follow-up Questions:
--------------------

1. Is there a way to extend the list of supported models?
2. How can we ensure safe and error-free usage with the stipulation of
   the exact match between ``system_template_formatter`` and
   ``system_template_variables``?
3. Can functionality be expanded to accept custom configurations beyond
   the listed ``AgentConfigName`` values?
