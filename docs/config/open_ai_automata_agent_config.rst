OpenAIAutomataAgentConfig
=========================

``OpenAIAutomataAgentConfig`` is a configuration class for Automata
agents interacting with the OpenAI API. This class extends the
``AgentConfig`` base class and provides specific configurations related
to the OpenAI API.

Overview
--------

The purpose of the ``OpenAIAutomataAgentConfig`` class is to maintain
all configuration settings required for automata agents talking to
OpenAI. It stores key information like system templates, template
variables, and provides ways to perform necessary setup and
configuration loading.

Attributes
----------

-  ``system_template (str)``: A string template that guides the initial
   message of the system.
-  ``system_template_variables (List[str])``: A list of string variable
   names indicating the placeholders in the system template.
-  ``system_template_formatter (Dict[str, str])``: A dictionary that
   formats the system template.
-  ``instruction_version (InstructionConfigVersion)``: The instruction
   configuration version.
-  ``system_instruction (Optional[str])``: System instruction.

These configurations control the interaction of an automata agent with
OpenAI API in terms of conversation initiation, system instructions and
more.

Methods
~~~~~~~

-  ``setup() -> None``: Performs setup for the agent such as computing
   session_id, setting setup the ``system_template_formatter`` and
   creating system instructions.
-  ``load(config_name: AgentConfigName) -> OpenAIAutomataAgentConfig``:
   Class method to load the configuration for the agent.
-  ``get_llm_provider() -> LLMProvider``: Provides the type of
   LLMProvider that the agent uses.
-  ``_formatted_instruction() -> str``: Transforms the system template
   into a system instruction.

Example Usage
-------------

The following code shows how to load an ``OpenAIAutomataAgentConfig``
configuration for the ``DEFAULT`` agent:

.. code:: python

   from automata.config.openai_config import OpenAIAutomataAgentConfig
   # Load default configuration for OpenAI Automata Agent
   config = OpenAIAutomataAgentConfig.load(AgentConfigName.DEFAULT)

Further manipulation of the config object allows customization of the
agent’s behaviors:

.. code:: python

   # Change system template
   config.system_template = 'This is a template with {variable}.'

Limitations
-----------

``OpenAIAutomataAgentConfig`` cannot be initialized with arbitrary
configuration values, and must be loaded from a predefined selection
(``AgentConfigName``). This can limit customization potential as any
additional configurations will have to be manually added after loading.

Follow-up Questions
-------------------

-  How can users add bespoke configuration settings not covered under
   the ``AgentConfigName`` enumeration?
-  Can there be a mechanism for users to specify and load configuration
   from their own files?
