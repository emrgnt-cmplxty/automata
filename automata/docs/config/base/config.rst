AgentConfig.Config
==================

``AgentConfig.Config`` is a nested configuration class within the main
``AgentConfig`` class. It sets the provider to ``LLMProvider.OPENAI``,
allowing for communication with OpenAI’s Language Models as the default
provider for Automata Agents. This configuration class also enables the
use of arbitrary types by setting ``arbitrary_types_allowed`` to
``True``.

Overview
--------

``AgentConfig.Config`` serves as an essential and integral part of the
``AgentConfig`` class, providing default settings that are required when
working with OpenAI’s Language Models. The nested configuration class
sets the provider for the providers and allows the usage of arbitrary
types within the agent configuration.

Related Symbols
---------------

-  ``automata.config.base.AgentConfig``
-  ``automata.config.base.LLMProvider``

Example
-------

The following example demonstrates how the ``AgentConfig.Config`` class
is implemented within the ``AgentConfig`` class. In this case, we are
using the ``OpenAIAutomataAgentConfig`` subclass, which inherits the
properties from the ``AgentConfig`` class.

.. code:: python

   from automata.config.base import AgentConfig, LLMProvider
   from pydantic import BaseModel

   class OpenAIAutomataAgentConfig(AgentConfig, BaseModel):
       class Config:
           arbitrary_types_allowed = True
           provider = LLMProvider.OPENAI

Follow-up Questions:
--------------------

-  Are there other providers and configurations that should be supported
   by the AgentConfig.Config class?
-  How can we extend the AgentConfig.Config class to support more
   configurations and providers?
