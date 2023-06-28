AgentDatabaseError
==================

``AgentDatabaseError`` is an exception raised when the agent fails to
set the database provider. This error is mainly encountered when
``AutomataOpenAIAgent`` is not able to set the correct database provider
for conversation or task management.

Related Symbols
---------------

-  ``automata.core.agent.error.AgentGeneralError``
-  ``automata.core.agent.error.AgentResultError``
-  ``automata.core.agent.error.AgentTaskGitError``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.tests.unit.test_task_database.db``
-  ``automata.core.agent.agents.AutomataOpenAIAgent``

Example
-------

The following is an example of how the ``AgentDatabaseError`` might be
encountered and handled when setting up the database provider for an
``AutomataOpenAIAgent``.

.. code:: python

   from automata.core.agent.agents import AutomataOpenAIAgent
   from automata.core.agent.error import AgentDatabaseError
   from automata.conversation_database.SimpleSQLiteConversationDatabase import SimpleSQLiteConversationDatabase

   try:
       agent = AutomataOpenAIAgent("Instructions to the agent")
       # Assuming `db` is an instance of a valid LLMConversationDatabaseProvider such as SimpleSQLiteConversationDatabase
       agent.set_database_provider(db)
   except AgentDatabaseError as e:
       print(f"Failed to set database provider: {e}")

Limitations
-----------

The ``AgentDatabaseError`` is tied to the implementation of the
``AutomataOpenAIAgent``. If the agent is updated to use a different
mechanism or method for setting the provider, the error may become
obsolete.

Follow-up Questions:
--------------------

-  Are there any alternative methods for setting the database provider
   that avoids raising ``AgentDatabaseError``?
