OpenAIAutomataAgent
===================

``OpenAIAutomataAgent`` is a class that represents an autonomous agent
designed to execute instructions and report the results back to the main
system. This agent communicates with the OpenAI API to generate
responses based on the given instructions, and it manages interactions
with various tools.

Overview
--------

The ``OpenAIAutomataAgent`` handles the process of executing natural
language instructions by operating in sequences of iteration. During
each iteration, the agent generates a new response and considers the
reply from the user, managing the iteration count and checking if the
task has completed or if the maximum number of iterations has been
reached.

The agent is configured with an instance of
``OpenAIAutomataAgentConfig``, which contains details such as session
ID, number of max iterations, and maximum tokens.

Related Symbols
---------------

-  ``automata.config.openai_config.OpenAIAutomataAgentConfig``
-  ``automata.config.openai_config.OpenAIAutomataAgentConfigBuilder``
-  ``automata.llm.providers.openai_llm.OpenAITool``
-  ``automata.agent.agent.Agent``
-  ``automata.agent.openai_agent.OpenAIAgentToolkitBuilder``
-  ``automata.tasks.task_executor.IAutomataTaskExecution``
-  ``automata.eval.agent.openai_function_eval.OpenAIFunctionCallAction``
-  ``automata.tasks.task_environment.AutomataTaskEnvironment``
-  ``automata.experimental.tools.builders.agentified_search_builder.AgentifiedSearchOpenAIToolkitBuilder``

Usage Example
-------------

.. code:: python

   # Setup configuration
   from automata.config.openai_config import OpenAIAutomataAgentConfigBuilder
   from automata.agent.openai_agent import OpenAIAutomataAgent

   config = OpenAIAutomataAgentConfigBuilder().with_model('gpt3').create_config()
   instructions = "Write a Python function to sum two numbers."
   agent = OpenAIAutomataAgent(instructions, config)

   # Run the agent
   result = agent.run()

   print(result)

Limitations
-----------

A limitation of ``OpenAIAutomataAgent`` is the requirement of
configurable parameters in ``OpenAIAutomataAgentConfig`` to tailor the
agent’s operations. Consequently, improper configurations might lead to
unexpected behaviors or errors. Moreover, complex tasks or insufficient
max iterations might lead to unfinished tasks.

Follow-up Questions:
--------------------

-  How can we optimally handle hierarchical agents or support multiple
   parallel agents?
-  Can we provide efficient ways to estimate token consumption to avoid
   hitting maximum tokens?
-  How can the agent best handle scenario when a tool fails during the
   execution?
