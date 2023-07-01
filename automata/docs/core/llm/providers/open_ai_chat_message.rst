OpenAIChatMessage
=================

``OpenAIChatMessage`` is a class to represent a processed chat message
to or from OpenAI. It extends the ``LLMChatMessage`` class and adds
additional functionality to handle chat messages that involve function
calls. The ``OpenAIChatMessage`` class plays a vital role in generating
messages for conversation with the OpenAI API.

Overview
--------

``OpenAIChatMessage`` provides methods to create and manipulate chat
messages. It includes utility methods for converting messages to and
from dictionary representations and creating ``OpenAIChatMessage``
instances from ``OpenAIChatCompletionResult`` objects.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.core.llm.providers.openai.FunctionCall``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.foundation.LLMCompletionResult``

Example
-------

The following example demonstrates how to create an instance of
``OpenAIChatMessage`` and generate its dictionary representation using
the ``to_dict`` method.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIChatMessage

   role = "assistant"
   content = "Hello, user!"
   message = OpenAIChatMessage(role=role, content=content)

   # Get the dictionary representation of the message
   message_dict = message.to_dict()

Limitations
-----------

The primary limitation of ``OpenAIChatMessage`` is that it assumes a
specific structure when parsing messages returned by the OpenAI API. If
the API response format changes, the implemented methods might not work
as expected.

Follow-up Questions:
--------------------

-  Are there any plans to support other APIs or platforms, and if so,
   how can we make the ``OpenAIChatMessage`` class more flexible to
   cater to different message formats?
