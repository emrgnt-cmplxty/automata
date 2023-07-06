OpenAIIncorrectMessageTypeError
===============================

``OpenAIIncorrectMessageTypeError`` is an error class that is raised
when the type of message provided is not of the expected
``OpenAIChatMessage`` type.

Overview
--------

The class is used in various methods in OpenAI-based classes, where it
helps in maintaining the correct type of data being used for the
communication with the OpenAI API.

Related Symbols
---------------

1.  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``
2.  ``automata.tests.unit.test_automata_agent.test_run_with_completion_message``
3.  ``automata.tests.unit.test_automata_agent.test_run_with_no_completion``
4.  ``automata.core.llm.providers.openai.OpenAIConversation``
5.  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
6.  ``automata.core.llm.providers.openai.OpenAIConversation.add_message``
7.  ``automata.tests.unit.test_automata_agent.test_iter_step_without_api_call``
8.  ``automata.core.agent.providers.OpenAIAutomataAgent``
9.  ``automata.tests.unit.test_automata_agent_builder.test_builder_invalid_input_types``
10. ``automata.core.llm.providers.openai.OpenAIConversation.__init__``

Example
-------

The following is an example demonstrating a likely use case for
``OpenAIIncorrectMessageTypeError``. This example supposes a case where
a message to OpenAIConversation of incorrect type is passed and the
error is raised.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIConversation, OpenAIIncorrectMessageTypeError

   try:
       conversation = OpenAIConversation()
       message = "This is a sample message." # Should be of type OpenAIChatMessage

       conversation.add_message(message) # Adds message to the conversation
   except OpenAIIncorrectMessageTypeError:
       print("Incorrect message type provided.")

Limitations
-----------

The ``OpenAIIncorrectMessageTypeError`` class does not provide methods
to automatically correct the type of the message and thus places the
responsibility of ensuring correct message type on the user.

Follow-up Questions
-------------------

-  Is there a specific reason for not including automatic type
   correction within the ``OpenAIIncorrectMessageTypeError`` class?
-  Could the design of the ``OpenAIIncorrectMessageTypeError`` class be
   improved to allow for more user-friendly data type handling?
-  Are there other similar type error classes within the OpenAI suite of
   APIs and does ``OpenAIIncorrectMessageTypeError`` interact with them
   in any way?
