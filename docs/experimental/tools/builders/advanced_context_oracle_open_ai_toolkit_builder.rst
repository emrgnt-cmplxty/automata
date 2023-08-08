AdvancedContextOracleOpenAIToolkitBuilder
=========================================

Overview
--------

``AdvancedContextOracleOpenAIToolkitBuilder`` is a class in the
``automata.experimental.tools.builders`` module designed to build tools
associated with the context oracle for the OpenAI API. This class
extends the functionality of both
``AdvancedContextOracleToolkitBuilder`` and
``OpenAIAgentToolkitBuilder``. The
``AdvancedContextOracleOpenAIToolkitBuilder`` is registered as a tool
manager with the ``OpenAIAutomataAgentToolkitRegistry``.

This class primarily hosts the ``build_for_open_ai()`` method, which
builds a list of OpenAI tools. Each OpenAI tool is an instance of
``OpenAITool`` with customized properties and required parameters.

Related Symbols
---------------

-  ``automata.llm.providers.openai_llm.OpenAIIncorrectMessageTypeError``:
   An exception type for incorrect message types.

-  ``automata.cli.install_indexing.install_indexing()``: A function to
   execute the install indexing script.

-  ``automata.llm.providers.openai_llm.OpenAIIncorrectMessageTypeError.__init__``:
   Initialization method for the OpenAIIncorrectMessageTypeError
   exception.

-  ``automata.agent.openai_agent.OpenAIAutomataAgent._build_initial_messages``:
   Method to build initial messages for the agent’s conversation.

-  ``automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.get_messages``:
   Method to get all messages corresponded to the original session id.

-  ``automata.tasks.task_registry.AutomataTaskRegistry.fetch_task_by_id``:
   Fetches a task by its recorded session id.

-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionProvider._stream_message``:
   Method to stream response message from the agent.

-  ``automata.tasks.task_registry.AutomataTaskRegistry.update_task``:
   Updates a task in the registry.

-  ``automata.llm.llm_base.LLMChatCompletionProvider.get_next_assistant_completion``:
   Abstract method to return the next assistant’s completion.

-  ``automata.tasks.task_environment.AutomataTaskEnvironment.setup``:
   Method to set up the environment by cloning the repository into the
   task directory.

Example
-------

Here is a simplified example demonstrating how to utilize
``AdvancedContextOracleOpenAIToolkitBuilder`` to build OpenAI tools.

.. code:: python

   from automata.experimental.tools.builders.advanced_context_oracle_builder\
       import AdvancedContextOracleOpenAIToolkitBuilder

   # Instantiate the builder
   builder = AdvancedContextOracleOpenAIToolkitBuilder()

   # Build the OpenAI Tools
   openai_tools = builder.build_for_open_ai()

   # Explore the built tools
   for tool in openai_tools:
       print(f"Tool Function: {tool.function}")
       print(f"Tool Name: {tool.name}")
       print(f"Tool Description: {tool.description}")

Limitations
-----------

The ``AdvancedContextOracleOpenAIToolkitBuilder`` is specifically
designed to generate tools associated with the context oracle for the
OpenAI API. Therefore, it may not be suitable or efficient for building
tools associated with other APIs or non-OpenAI contexts. It also
requires the explicit definition of properties and required parameters
which could limit its flexibility.

Follow-up Questions:
--------------------

-  What are the exact properties and required parameters needed in
   OpenAITool instances?
-  Can we make this class more flexible, allowing it to handle tools
   associated with different APIs and contexts?
