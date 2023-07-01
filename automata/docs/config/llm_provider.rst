LLMProvider
===========

``LLMProvider`` is an enumeration used to identify and facilitate the
configuration of LLMChatCompletionProvider instances. The instances are
used to provide chat completions using the specified providers (e.g.,
OpenAI). The LLMProvider enumeration has a one-to-one mapping with the
respective completion provider classes.

Related Symbols
---------------

-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.config.base.AgentConfig``
-  ``automata.config.openai_agent.AutomataOpenAIAgentConfig``

Overview
--------

The ``LLMProvider`` enumeration is used as a simple, clean way to
identify the specific type of LLMChatCompletionProvider used in an
application. By referencing the available enumeration values, the
application can instantiate the appropriate provider based on the
settings in the ``AgentConfig``.

Example
-------

The following example shows how to use ``LLMProvider`` to identify and
create the desired LLMChatCompletionProvider for an application.

.. code:: python

   from automata.config.base import LLMProvider
   from automata.config.openai_agent import AutomataOpenAIAgentConfig
   from automata.core.llm.foundation import LLMChatCompletionProvider

   # Get the LLMProvider from the agent configuration
   config = AutomataOpenAIAgentConfig()
   provider = config.get_provider()

   # Create the appropriate LLMChatCompletionProvider based on the LLMProvider value
   if provider == LLMProvider.OPENAI:
       completion_provider = LLMChatCompletionProvider()

Limitations
-----------

The main limitation of ``LLMProvider`` is that it currently only
supports a limited set of providers (e.g., OpenAI). To support
additional LLMChatCompletionProviders, new enumeration values must be
added to the LLMProvider enumeration, and the corresponding code must be
written to handle those new values in any logic that uses
``LLMProvider``.

Follow-up Questions:
--------------------

-  How can we easily extend ``LLMProvider`` to include other
   LLMChatCompletionProvider types?
-  How can we ensure that applications consistently handle new
   LLMChatCompletionProvider variants as they are added to the
   LLMProvider enumeration?
