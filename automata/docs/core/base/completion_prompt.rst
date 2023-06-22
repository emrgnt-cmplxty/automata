CompletionPrompt
================

The ``CompletionPrompt`` class is part of the Automata Agent framework
and is used to wrap prompts to be compatible with non-chat models, which
use ``openai.Completion.create``. It extends from the ``Prompt`` class
and provides a method to convert the raw prompt into a formatted string
compatible with non-chat models.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``
-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_tool_message_to_parse``
-  ``automata.core.base.openai.text_prompt_to_chat_prompt``
-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_agent_message_to_parse``
-  ``automata.tests.unit.test_automata_agent.test_iter_step_with_completion_message``
-  ``automata.tests.unit.test_automata_agent.test_iter_step_with_parsed_completion_message``
-  ``automata.core.base.openai.CompletionResult``
-  ``automata.tests.unit.test_automata_coordinator.mock_openai_response_with_agent_query``
-  ``automata.core.base.openai.CompletionResult.get_completions``
-  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
-  ``automata.core.base.openai.chat_prompt_to_text_prompt``
-  ``automata.core.base.openai.Prompt``
-  ``automata.core.base.openai.is_chat_prompt``

Example
-------

.. code:: python

   import threading
   from typing import Any, Dict, List, NamedTuple, Union
   from automata.core.base.openai import CompletionPrompt

   raw_prompt = "What is the capital of France?"

   # Create a CompletionPrompt instance
   completion_prompt = CompletionPrompt(raw_prompt)

   # Convert the raw prompt to a formatted prompt
   formatted_prompt = completion_prompt.to_formatted_prompt()

   print(formatted_prompt)  # Output: What is the capital of France?

Limitations
-----------

``CompletionPrompt`` is limited to supporting only the conversion of raw
prompts for models using ``openai.Completion.create``. It does not
support other model types or formats. Additionally, the conversion might
not handle some complex cases of chat-based prompts correctly, which can
result in unexpected formatting.

Follow-up Questions:
--------------------

-  Can ``CompletionPrompt`` be extended to support other model types or
   prompt formats?
-  How can we handle complex chat-based prompts, and are there known
   formatting issues with certain types of prompts?
