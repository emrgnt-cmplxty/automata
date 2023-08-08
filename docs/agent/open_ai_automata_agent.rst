OpenAIAutomataAgent
===================

``OpenAIAutomataAgent`` is a specific type of ``Agent`` tailored for
executing tasks using the OpenAI engine. This autonomous agent takes
instructions, performs actions based on them, and reports the results.
The interactions with the various tools are managed via the OpenAI API
for generating responses.

Overview
--------

An instance of ``OpenAIAutomataAgent`` is initialized with a set of
``instructions`` along with a ``config`` object of type
``OpenAIAutomataAgentConfig`` detailng the operational parameters of the
agent. During its life cycle, the agent executes a series of iterations,
each of which consists of generating a new assistant message, processing
it, and incrementing an iteration counter. The agent also manages a
conversation with the OpenAI API, storing the history of user and
assistant messages.

Usage Example
-------------

In this sample, an ``OpenAIAutomataAgent`` is created with a specific
set of ``instructions`` and a configuration object:

::

   from automata.agent.openai_agent import OpenAIAutomataAgent
   from automata.config.openai_config import OpenAIAutomataAgentConfigBuilder

   instructions = 'Translate the following English text to French: {TEXT_TO_TRANSLATE}.'
   config = OpenAIAutomataAgentConfigBuilder.from_name('automata').with_stream(False).with_system_template_formatter({}).build()

   agent = OpenAIAutomataAgent(instructions, config)
   agent.run()

After instantiating the OpenAIAutomataAgent, the ``run`` method can be
called to start executing the task.

Related Symbols
---------------

-  ``automata.config.openai_config.OpenAIAutomataAgentConfig``
-  ``automata.llm.providers.openai_llm.OpenAITool``
-  ``automata.llm.providers.openai_llm.OpenAIChatMessage``
-  ``automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase``
-  ``automata.agent.agent.Agent``
-  ``automata.tasks.task_registry.AutomataTaskRegistry``
-  ``automata.tasks.automata_task.AutomataTask``

Limitations
-----------

-  While ``OpenAIAutomataAgent`` supports executing larger tasks
   interactively over multiple iterations, exceeding the maximum number
   of iterations or tokens raises an ``AgentStopIterationError``.
-  Interactions with tools are currently only executed sequentially,
   without support for hierarchical or parallel invocation of tools or
   asynchronous tool execution.
-  The agent only supports a conversation model where the user and
   assistant take turns in communicating, with the assistant always
   responding to the user’s prompts or responses to previous assistant
   messages.

Follow-up Questions:
--------------------

-  Can ``OpenAIAutomataAgent`` be customized or extended for different
   interaction models with the assistant?
-  Very long instructions are currently truncated while generating
   status notes. Would deeper support for long instructions be
   beneficial?
-  How would ``OpenAIAutomataAgent`` be used in a live, interactive
   setting with real users providing inputs to the agent, as opposed to
   pre-set instructions?
