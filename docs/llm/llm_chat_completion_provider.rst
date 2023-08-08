LLMChatCompletionProvider
=========================

Overview
--------

``LLMChatCompletionProvider`` is an abstract base class developed in the
``automata.llm.llm_base`` module and serves as a blueprint for building
different types of LLM chat completion providers. Designed as a core
component of an AI assistant, it provides the structure for receiving,
interpreting, and generating responses to user messages.

The key methods defined in the base class include
``get_next_assistant_completion()``, ``add_message()``, ``reset()``, and
``standalone_call()``. These methods provide a range of capabilities
from fetching the next assistant completion to managing the provider’s
buffer of chat messages. The ``standalone_call()`` method is especially
important as it allows interacting with the LLM chat provider
independently, which can be handy when the provider is treated as a
singular output source rather than a chat provider.

Related Symbols
---------------

-  ``automata.llm.providers.openai_llm.OpenAIConversation.get_latest_message``
-  ``automata.llm.providers.openai_llm.OpenAIConversation.get_messages_for_next_completion``
-  ``automata.llm.llm_base.LLMConversationDatabaseProvider.get_messages``
-  ``automata.llm.providers.openai_llm.OpenAIConversation.reset_conversation``
-  ``automata.llm.llm_base.LLMConversation.register_observer``
-  ``automata.llm.providers.openai_llm.OpenAIConversation.__len__``
-  ``automata.llm.llm_base.LLMConversation.notify_observers``
-  ``automata.llm.llm_base.LLMConversation.unregister_observer``
-  ``automata.core.utils.get_logging_config``
-  ``automata.singletons.github_client.GitHubClient.merge_pull_request``.

As the methods in ``LLMChatCompletionProvider`` are abstract, they need
to be overriden in any class that inherits from
``LLMChatCompletionProvider``. As such, related symbols include methods
in classes that are likely to override these methods.

Example
-------

.. code:: python

   class CustomChatCompletionProvider(LLMChatCompletionProvider):
       def get_next_assistant_completion(self) -> LLMChatMessage:
           # Implement custom logic to get the next assistant message
           pass

       def add_message(self, message: LLMChatMessage, session_id: Optional[str]=None) -> None:
           # Implement custom logic to add a new message to the buffer.
           pass

       def reset(self) -> None:
           # Implement custom logic to reset the chat provider's buffer.
           pass

       def standalone_call(self, prompt: str, session_id: Optional[str]=None) -> str:
           # If the provider's buffer is not devoid of content Throw Exception
           # else implement custom logic to handle standalone calls.
           pass

This demonstrates how a developer might implement a class that inherits
from ``LLMChatCompletionProvider``. Note, however, each method contains
a ``pass`` statement, indicating that the methods need to be replaced in
accordance with specific completion provider requirements.

Limitations
-----------

As ``LLMChatCompletionProvider`` is an abstract base class, it does not
provide any functionality on its own and must be subclassed. These
subclasses must implement all of its abstract methods, or they too will
become abstract classes. Moreover, the actual behavior of the methods is
entirely dependent on their implementation in the subclasses, resulting
in potential variability and inconsistency between different LLM
providers.

Additionally, the ``standalone_call()`` method may result in an
exception if the chat provider’s buffer is not devoid of content.

Follow-up Questions:
--------------------

-  What are some recommended best practices for implementing the
   abstract methods in ``LLMChatCompletionProvider`` subclasses?
-  How does the ``standalone_call()`` work in synergy with the other
   methods of the class?
-  Can we build in some consistency-check mechanisms to ensure a
   standard behavior across different LLM providers?
