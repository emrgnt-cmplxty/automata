LLMConversation
===============

``LLMConversation`` acts as an abstract base class defining the
essential features and behaviour for different types of LLM (logic and
language model) conversation models. It provides the structure for
conversation implementations, including getting messages, registering
and notifying observers, and resetting conversations.

``LLMConversation`` also includes an internal
``LLMEmptyConversationError`` Exception class thrown when the
conversation is empty.

Overview
--------

``LLMConversation`` serves as the foundational class for any LLM
conversations. It specifies the necessary interface but does not
implement these methods, expecting the child classes to provide specific
implementations. Key methods available include message retrieval
options, observer management operations, and procedures for obtaining
conversation-specific information like length and the latest message.

Related Symbols
---------------

-  ``automata.llm.llm_chat_message.LLMChatMessage``
-  ``automata.llm.llm_base.LLMEmptyConversationError``
-  ``automata.llm.observers.Observer``

Example
-------

As ``LLMConversation`` is an abstract base class, it cannot be
instantiated directly. Instead, a child class inheriting from
``LLMConversation`` should implement all the abstract methods. Here’s an
example:

.. code:: python

   from automata.llm.llm_base import LLMConversation
   from automata.llm.llm_chat_message import LLMChatMessage

   class SimpleLLMConversation(LLMConversation):
       def __init__(self):
           super().__init__()
           self.conversation = []

       @property
       def messages(self) -> Sequence[LLMChatMessage]:
           return self.conversation

       def __len__(self) -> int:
           return len(self.conversation)

       def get_messages_for_next_completion(self) -> Any:
           return self.conversation[-1] if self.conversation else None

       def get_latest_message(self) -> LLMChatMessage:
           return self.conversation[-1] if self.conversation else None

       def reset_conversation(self) -> None:
           self.conversation = []

Limitations
-----------

``LLMConversation`` assumes that any inheriting class will provide
concrete implementations for all abstract methods. It’s thus crucial to
ensure that all these methods are adequately defined in child classes.

Some methods, like notifying observers, assume a traditional observer
pattern. If a different design is used for managing observers, these
methods may need to be overridden or adapted.

Lastly, the actual interaction with the chat infrastructure (for
example, sending and receiving LLMChatMessages) is not specified within
this class and should be implemented contextually in the subclasses or
surrounding code.

Follow-up Questions:
--------------------

-  How does ``LLMConversation`` interact directly with the LLM if it
   requires message information?
-  Are there guidelines or standards that must be observed when
   implementing the abstract methods? For instance, what should be
   considered the “next” messages for the
   ``get_messages_for_next_completion`` method?
-  How to handle updates to the class due to changes in observer
   methods? How should the class be structured to accommodate potential
   changes in the notification mechanism?
