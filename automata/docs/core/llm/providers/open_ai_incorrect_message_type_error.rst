OpenAIIncorrectMessageTypeError
===============================

``OpenAIIncorrectMessageTypeError`` is a custom exception raised when an
expected message of type ``OpenAIChatMessage`` is incorrectly passed as
another type.

Overview
--------

This exception is used within the ``automata.core.llm.providers.openai``
module to ensure that messages passed around in a conversation with the
OpenAI API are of the correct type, which is ``OpenAIChatMessage``. This
improves the robustness of the conversation handling and ensures that
the expected messages can be processed correctly.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.core.agent.agents.AutomataOpenAIAgent``

Example
-------

The following example demonstrates how the exception is raised when an
incorrect message type is passed.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIConversation, OpenAIIncorrectMessageTypeError
   from automata.core.llm.completion import LLMChatMessage

   # Create a conversation and a non-OpenAIChatMessage message
   conversation = OpenAIConversation()
   incorrect_message = LLMChatMessage(role="assistant", content="Some content")

   # The following line raises OpenAIIncorrectMessageTypeError
   try:
       conversation.add_message(incorrect_message)
   except OpenAIIncorrectMessageTypeError as error:
       print("Caught an exception:", error)

Limitations
-----------

The primary limitation of ``OpenAIIncorrectMessageTypeError`` is that it
can only be raised when an expected message type is
``OpenAIChatMessage``, and it’s not a general-purpose message type
error. It’s specifically designed for use in the
``automata.core.llm.providers.openai`` module.

Follow-up Questions:
--------------------

-  Are there other similar exceptions used in the
   ``automata.core.llm.providers.openai`` module?
-  Can we generalize the exception to handle other message types that
   might be expected in the future?
