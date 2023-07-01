LLMChatMessage
==============

``LLMChatMessage`` is a base class for different types of LLM chat
messages. It stores message metadata (such as role and content) and
provides a ``to_dict`` method to convert the message into a dictionary
format for easier processing.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIConversation.get_latest_message``
-  ``automata.core.llm.foundation.LLMConversation.get_latest_message``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.tests.unit.test_conversation_database.test_put_message_increments_interaction_id``
-  ``automata.core.llm.foundation.LLMConversation``
-  ``automata.tests.unit.test_conversation_database.test_get_messages_returns_all_messages_for_session``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.tests.unit.test_conversation_database.test_multiple_put_message_increments_interaction_id``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``

Example
-------

Here is an example of creating an ``LLMChatMessage`` instance:

.. code:: python

   from automata.core.llm.foundation import LLMChatMessage

   role = "user"
   content = "Hello, how are you?"

   message = LLMChatMessage(role=role, content=content)

``LLMChatMessage`` can also be converted into a dictionary using the
``to_dict`` method:

.. code:: python

   message_dict = message.to_dict()
   print(message_dict)  # Output: {'role': 'user', 'content': 'Hello, how are you?'}

Limitations
-----------

The ``LLMChatMessage`` class does not handle message processing or
validation; it simply stores the message metadata. Any additional
processing or validation should be implemented by the developer using
this class.

Follow-up Questions:
--------------------

-  Are there any specific data types that should be supported beyond the
   base string and dictionary types?
-  Is there a need for additional utility methods or properties within
   the ``LLMChatMessage`` class for common use cases?
