OpenAIConversation
==================

Overview
--------

``OpenAIConversation`` is a module provided by Automata’s OpenAI lower
level model(LLM) providers. It represents a conversation with the OpenAI
API. It holds a list of messages as an instance variable and provides
methods to interact with this list of messages such as adding a message,
getting messages for the next completion, getting the latest message,
and resetting the conversation.

Main properties and methods of the ``OpenAIConversation`` include:

-  ``messages``: A list that contains all the messages in the current
   conversation.
-  ``add_message(message: LLMChatMessage, session_id: Optional[str]) -> None``:
   This method adds message to the conversation.
-  ``get_messages_for_next_completion() -> List[Dict[str, Any]]``: This
   method provides a list of all messages in the current conversation
   prepared for the next completion.
-  ``get_latest_message() -> LLMChatMessage``: This method returns the
   latest message in the conversation.
-  ``reset_conversation() -> None``: This method empties the list of
   messages, thus resetting the conversation.

Related Symbols
---------------

-  ``automata.llm.providers.openai_llm.LLMChatMessage``
-  ``automata.llm.providers.openai_llm.OpenAIChatMessage``
-  ``automata.llm.providers.openai_llm.OpenAIIncorrectMessageTypeError``

Example
-------

Below is a simple usage example of how to interact with the OpenAI API
using the ``OpenAIConversation`` class.

.. code:: python

   from automata.llm.providers.openai_llm import OpenAIConversation, OpenAIChatMessage

   # Initialize the OpenAIConversation object.
   conversation = OpenAIConversation()

   # Create a message.
   message = OpenAIChatMessage("Hello, OpenAI!")

   # Add the message to the conversation.
   conversation.add_message(message, None)

   # Fetch the latest message in the conversation.
   latest_message = conversation.get_latest_message()
   print(latest_message) # Output: <LLMChatMessage: Hello, OpenAI!>

   # Reset the conversation.
   conversation.reset_conversation()

Limitations
-----------

A significant limitation of the ``OpenAIConversation`` class is the lack
of support for asynchronous operations. All operations are performed
synchronously which can lead to blocking of the entire application if
the operations are time-consuming, like in a live chat implementation.

Another limitation is that the conversation is stateful. Once a message
is added to the conversation, it cannot be removed. This makes it
difficult to manage long conversations. While there is a method to reset
the entire conversation (``reset_conversation``), there’s no way to
manipulate individual messages within the conversation.

Follow-up Questions:
--------------------

-  Is there a way to support asynchronous operations with
   ``OpenAIConversation``?
-  Can there be methods incorporated to manage (add or remove)
   individual messages within the conversation?
-  How can the ``OpenAIConversation`` handle much larger conversations?
