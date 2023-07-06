OpenAIChatCompletionProvider
============================

``OpenAIChatCompletionProvider`` is a class that provides chat messages
from OpenAI API. It utilizes the OpenAI ChatCompletion method to
interact with AI agents and manage conversations.

Overview
--------

``OpenAIChatCompletionProvider`` allows developers to interact with AI
agents through chat. The class takes in several parameters, such as
``model``, ``temperature``, ``stream`` and ``functions``. The class also
provides methods to manage conversations, including adding messages,
getting completion messages from the AI, and resetting conversations.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.llm.foundation.LLMConversation``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``

Example
-------

The following is an example demonstrating how to instantiate and use the
``OpenAIChatCompletionProvider``:

.. code:: python

   from automata.core.llm.providers.openai import OpenAIChatCompletionProvider, LLMChatMessage

   model = "gpt-4"
   conversation = OpenAIChatCompletionProvider(model)
   conversation.add_message(LLMChatMessage(role="user", content="Hello!"))
   response_message = conversation.get_next_assistant_completion()
   print(response_message.content)

Limitations
-----------

The ``OpenAIChatCompletionProvider``\ ’s
``get_approximate_tokens_consumed`` method is an approximation and may
not exactly represent the total tokens consumed by the generated chat
instance. Additionally, the ``standalone_call`` method requires an empty
conversation, so the ``reset`` method needs to be called prior to using
``standalone_call`` if there are existing messages in the conversation.

Follow-up Questions:
--------------------

-  What would be the impact on the conversation history if the ``reset``
   method is called, particularly in an ongoing conversation?
-  Do we need to manage token limits on our applications to avoid
   reaching OpenAI API’s token limit in a relatively shorter timespan?
   Can this be automatically managed?
