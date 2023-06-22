OpenAIChatMessage
=================

``OpenAIChatMessage`` is a data class used by ``AutomataAgent`` to store
the role and content of the messages exchanged during the agent’s
interactions with the OpenAI API. This makes it easy to convert the
messages into a dictionary format which can be used during API calls.

Overview
--------

``OpenAIChatMessage`` holds two main attributes: the role of the message
sender (such as “system”, “user”, or “assistant”), and the content of
the message itself. It helps manage and organize messages exchanged
between the agent and the OpenAI API in a unified format. The
``to_dict`` method allows converting the message into a dictionary
format, which is required for making API calls.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.openai.OpenAIChatCompletionResult``

Example
-------

The following example demonstrates how to create an instance of
``OpenAIChatMessage`` and convert it into a dictionary format.

.. code:: python

   from automata.core.base.openai import OpenAIChatMessage

   role = "user"
   content = "Find the files where AutomataAgent is imported."
   message = OpenAIChatMessage(role=role, content=content)
   message_dict = message.to_dict()

   print(message_dict)

Output:

.. code:: python

   {"role": "user", "content": "Find the files where AutomataAgent is imported."}

Limitations
-----------

The current limitations of ``OpenAIChatMessage`` include its lack of
support for more advanced message formats and structures that the OpenAI
API may evolve to support. The class is primarily designed to work with
the current chat-based API format and may require updates to accommodate
future API changes.

Follow-up Questions:
--------------------

-  Are there any known upcoming changes or updates to the OpenAI API
   that may affect the structure or usage of ``OpenAIChatMessage``?
