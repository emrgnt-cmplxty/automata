LLMChatCompletionProvider
=========================

``LLMChatCompletionProvider`` is an abstract base class used to
structure different types of Language Learning Model (LLM) chat
completion providers. The class contains four essential methods that
should be implemented by any subclass. These methods include adding new
chat messages and retrieving the next assistant’s completion from a chat
provider. Additionally, the chat provider can be reset, and it can
operate as a standalone output supplier for the LLM.

Its main function is to form the fundamental structure for various chat
completion providers in the LLM by standardizing their core methods.

Overview
--------

The ``LLMChatCompletionProvider`` class provides a blueprint for LLM
chat completion providers. It comprises two primary operations – sending
and receiving messages from the chat provider and managing the chat
session. This is especially crucial in controlling the flow of data in
and out of the chat provider, paired with the functionality to control
and manipulate the chat buffer.

Related Symbols
---------------

-  ``LLMChatMessage``: This is a base class for different types of chat
   messages that are used by LLM and can be provided to the
   LLMChatCompletionProvider to add new messages to the chat buffer.
-  ``LLMCompletionResult``: This provides the structure for different
   types of completion results received from the
   ``LLMChatCompletionProvider``.
-  ``OpenAIChatCompletionProvider``: This is a subclass of
   ``LLMChatCompletionProvider`` that uses the OpenAI API to provide
   chat messages. This class has implemented the abstract methods of the
   ``LLMChatCompletionProvider`` and can operate as functional
   completion provider.

Example
-------

As ``LLMChatCompletionProvider`` is an abstract base class, you cannot
instantiate it or use it as is. Instead, you use subclasses of
``LLMChatCompletionProvider`` that have implemented the abstract
methods. One such subclass is ``OpenAIChatCompletionProvider``. Below is
an example of how to use it:

.. code:: python

   from automata.core.llm.providers.openai import OpenAIChatCompletionProvider
   from automata.core.llm.foundation import LLMChatMessage

   provider = OpenAIChatCompletionProvider()

   # Add a new message to the provider's buffer
   provider.add_message(LLMChatMessage(content="Hello World", channel="general"))

   # Get the next assistant completion from the LLM.
   next_message = provider.get_next_assistant_completion()
   print(next_message.content)  # Prints the content of the next assistant completion message

Limitations
-----------

The LLMChatCompletionProvider only provides an abstract structure and
does not implement the methods which limits its direct usage. Subclasses
are required to implement the where necessary for interacting with
different LLM chat completion providers.

It also assumes that a unique message can be added to the provider’s
buffer and that the provider can be queried for the next assistant
completion at any time. This may not align with the actual behavior of
all chat completion providers.

Follow-up Questions
-------------------

-  Can this class be refactored further for more versatile usage?
