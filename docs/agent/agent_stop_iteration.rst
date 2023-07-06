automata.agent.error.AgentStopIteration
=======================================

Overview
--------

``AgentStopIteration`` is a built-in exception class in the ``automata``
library. It is raised when the agent stops iterating in the program
execution process. It provides useful debugging information if a running
agent stops iterating prematurely for some reason.

The ``AgentStopIteration`` exception is mostly used within classes that
implement the Python iterable and iterator protocols. It serves as a
signal to the agent’s iterator to stop the iteration process.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent.test_run_with_no_completion``:
   This unit test uses the ``AgentStopIteration`` exception to ensure
   the ``automata_agent`` stops iterating when no completion is present.

-  ``automata.tests.unit.test_automata_agent.test_iter_step_without_api_call``:
   In this unit test, ``AgentStopIteration`` reflects the expected
   behavior when manually feeding next(…) calls to the automata agent
   without an API call.

-  ``automata.agent.error.AgentMaxIterError``: This is another exception
   class used when the agent exceeds the maximum number of allowed
   iterations.

-  ``automata.agent.agent.Agent.__iter__``: The ``__iter__`` method of
   the ``Agent`` class calls upon the ``AgentStopIteration`` when the
   agent stops iterating.

-  ``automata.agent.providers.OpenAIAutomataAgent``: The
   ``OpenAIAutomataAgent``, designed to execute instructions and
   interact with various tools, uses the ``AgentStopIteration``
   exception to handle situations where the agent ceases to iterate.

-  ``automata.agent.providers.OpenAIAutomataAgent.__iter__``: The
   ``__iter__`` method in the ``OpenAIAutomataAgent`` class handles the
   ``AgentStopIteration`` exception when the iteration process is
   stopped.

Example
-------

There’s no directly instantiable example of ``AgentStopIteration`` as it
is raised when an iteration is stopped in a running agent. However,
below is an example of a possible use case in context of
``OpenAIAutomataAgent``. Please note mock situations have been
represented without the actual underlying object:

.. code:: python

   from unittest.mock import patch
   from automata.agent.providers import OpenAIAutomataAgent
   from automata.agent.error import AgentMaxIterError

   @patch("openai.ChatCompletion.create")
   def test_agent_stops_iteration(mock_openai_chatcompletion_create, automata_agent):
       automata_agent = OpenAIAutomataAgent('instructions', 'config')
       # Mock the API response
       mock_openai_chatcompletion_create.return_value = {
           "choices": [{"message": {"content": "...", "role": "assistant"}}]
       }

       try: 
           automata_agent.run()   # runs the agent
       except AgentStopIteration:
           print("Agent has stopped iterating.")

In this code snippet, ``AgentStopIteration`` is expected to be raised
when ``automata_agent.run()`` is called. If the agent stops, the
exception is caught and it prints “Agent has stopped iterating.”

Limitations
-----------

The ``AgentStopIteration`` exception is raised when the agent stops
iterating. However, it does not provide information regarding why the
agent stopped iterating. Determining the agents stopping reasoning
requires additional debugging or error checks within the code.

Follow-up Questions
-------------------

-  What specific conditions in the agent’s operations trigger
   ``AgentStopIteration``?
-  Can we handle and resume from ``AgentStopIteration`` in certain
   contexts?
