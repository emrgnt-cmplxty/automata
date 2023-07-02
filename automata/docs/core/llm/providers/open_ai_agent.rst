OpenAIAgent
===========

The ``OpenAIAgent`` class provides an agent that interacts with the
OpenAI API. The agent can process various instructions, manage
conversations, and generate responses based on the given instructions.
The code examples below showcase how to import, initialize, and use the
``OpenAIAgent`` class.

Import Statements
-----------------

.. code:: python

   import openai
   from automata.core.agent.agent import Agent
   from automata.core.llm.foundation import (
       LLMChatCompletionProvider,
       LLMChatMessage,
       LLMCompletionResult,
       LLMConversation
   )

Initialization
--------------

To create an instance of the ``OpenAIAgent`` class, you need to provide
a string containing the instructions that the agent should execute.

.. code:: python

   instructions = "Some instructions for the OpenAIAgent"
   agent = OpenAIAgent(instructions)

Termination
-----------

You can check if the agent has completed its task using the
``completed`` attribute. To terminate the agent, use the ``terminate``
method and provide a result string.

.. code:: python

   if not agent.completed:
       result = "The agent has completed its task."
       agent.terminate(result)

Related Symbols
---------------

-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.core.llm.providers.openai.OpenAIConversation``

Example
-------

Below is an example of how to create an instance of ``OpenAIAgent``,
provide instructions, and terminate the agent when it has completed its
task.

.. code:: python

   from automata.core.agent.agent import Agent
   from automata.core.llm.foundation import (
       LLMChatCompletionProvider,
       LLMChatMessage,
       LLMCompletionResult,
       LLMConversation
   )

   instructions = "Retrieve the latest news articles."
   agent = OpenAIAgent(instructions)

   if not agent.completed:
       result = "The agent has completed its task."
       agent.terminate(result)

Limitations
-----------

``OpenAIAgent`` relies on the OpenAI API for generating responses, so it
is subject to the limitations and restrictions of the API itself. The
performance of the agent is dependent on factors such as the model
chosen, latency between requests, and rate-limiting.

Follow-up Questions:
--------------------

-  How can I integrate the OpenAIAgent with additional OpenAI API
   features and models?
-  How can the performance of the OpenAIAgent be improved or optimized
   for specific tasks?
