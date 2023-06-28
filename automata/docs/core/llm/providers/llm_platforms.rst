LLMPlatforms
============

``LLMPlatforms`` is an enumeration class that defines the available
platforms for the language learning model (LLM) completion providers. It
provides a convenient way to specify the platform for providers such as
the OpenAI API.

Overview
--------

``LLMPlatforms`` enables easy platform selection for LLM completion
providers. The class is based on the ``Enum`` class from the Python
standard library, which allows for a simple and efficient enumeration of
the available platforms.

Related Symbols
---------------

-  ``automata.core.llm.completion.LLMChatCompletionProvider``
-  ``automata.core.llm.providers.openai.OpenAIConversation.get_latest_message``

Example
-------

The following example demonstrates how to use the ``LLMPlatforms``
enumeration to set up an LLM completion provider for the OpenAI
platform.

.. code:: python

   from automata.core.llm.providers.available import LLMPlatforms
   from automata.core.llm.providers.openai import OpenAIProvider

   platform = LLMPlatforms.OPENAI
   provider = OpenAIProvider(api_key="your_openai_api_key")

Limitations
-----------

``LLMPlatforms`` enumeration currently only supports the OpenAI
platform. Future platforms should be added to the enumeration as they
become available.

Follow-up Questions:
--------------------

-  Are there other platforms that should be added to the
   ``LLMPlatforms`` enumeration?
-  Are there any specific requirements or setup steps needed for each
   platform that should be documented in this section?
