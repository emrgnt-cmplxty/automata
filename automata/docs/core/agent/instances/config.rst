AutomataOpenAIAgentInstance
===========================

``AutomataOpenAIAgentInstance`` is an instance of an Automata OpenAI
agent designed to execute instructions and report the results back to
the main system. It communicates with the OpenAI API to generate
responses based on given instructions and manages interactions with
various tools.

Overview
--------

The ``AutomataOpenAIAgentInstance`` class is a specialized
implementation of the ``OpenAIAutomataAgent`` for interacting with
OpenAI API. It is built on top of the ``OpenAIAutomataAgent`` class and
provides a simple interface to run the agent with given instructions. It
inherits methods and properties from the ``OpenAIAutomataAgent`` class
and adapts them for the specific use case of running an instance of the
agent.

Related Symbols
---------------

-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.core.llm.providers.openai.OpenAIAgent``

Example
-------

The following example demonstrates how to create an instance of
``AutomataOpenAIAgentInstance`` and run it with given instructions.

.. code:: python

   from automata.core.agent.instances import AutomataOpenAIAgentInstance

   instructions = "Find the largest prime number less than 100."
   agent_instance = AutomataOpenAIAgentInstance()
   result = agent_instance.run(instructions)

   print(result)

Limitations
-----------

The primary limitation of ``AutomataOpenAIAgentInstance`` is its
reliance on the OpenAI API for generating responses. This might lead to
less flexibility, depending on individual use cases and specific API
limitations.

Follow-up Questions:
--------------------

-  What are some alternatives for using the
   ``AutomataOpenAIAgentInstance`` class without relying on the OpenAI
   API?
-  Are there any built-in fallback mechanisms in case the OpenAI API is
   unavailable or unreliable for performing certain tasks?
