Agent
=====

``Agent`` is an abstract class for implementing an agent. An agent is an
autonomous entity that can perform actions and communicate with other
providers. This class provides a basic structure for creating providers and
must be subclassed to create a custom agent implementation.

Overview
--------

The ``Agent`` class provides a framework for implementing an agent. It
includes an abstract method called ``run`` which must be implemented by
subclasses to provide the agent’s main logic. The class also includes a
method called ``set_database_provider`` to set the agent’s conversation
database provider.

Agents interact with an environment, perform actions, and communicate
with other providers. You can create a custom agent by subclassing the
``Agent`` class and implementing its methods.

Related Symbols
---------------

-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.core.llm.completion.LLMConversationDatabaseProvider``
-  ``automata.core.llm.providers.openai.OpenAIAgent``

Example Usage
-------------

The following example demonstrates how to create a custom agent by
subclassing ``Agent``. This custom agent simply logs each step of its
iteration and has a limited number of total steps.

.. code:: python

   import logging
   from automata.core.base.agent import Agent
   from automata.core.llm.completion import LLMIterationResult

   class CustomAgent(Agent):
       def __init__(self, instructions: str, max_steps: int = 10) -> None:
           super().__init__(instructions)
           self.max_steps = max_steps
           self.current_step = 0

       def __iter__(self):
           return self

       def __next__(self) -> LLMIterationResult:
           if self.current_step < self.max_steps:
               logging.info(f"Step {self.current_step}: Executing custom actions")
               self.current_step += 1
               return LLMIterationResult()
           else:
               raise StopIteration

       def run(self) -> str:
           logging.info("Running CustomAgent")
           for _ in self:
               pass
           logging.info("CustomAgent completed")
           return "Custom agent result"

       def set_database_provider(self, provider):
           # Custom agent does not use a database provider in this example
           pass

   # Example usage of the custom agent
   agent = CustomAgent("Perform custom actions for 10 steps")
   result = agent.run()
   print(result)

Output:

::

   Running CustomAgent
   Step 0: Executing custom actions
   Step 1: Executing custom actions
   Step 2: Executing custom actions
   Step 3: Executing custom actions
   Step 4: Executing custom actions
   Step 5: Executing custom actions
   Step 6: Executing custom actions
   Step 7: Executing custom actions
   Step 8: Executing custom actions
   Step 9: Executing custom actions
   CustomAgent completed
   Custom agent result

Limitations
-----------

``Agent`` is an abstract class and cannot be used directly. It must be
subclassed to create a custom agent implementation that provides the
necessary functionality.

Follow-up Questions:
--------------------

-  Are there any specific limitations or requirements for the
   ``set_database_provider`` method?
