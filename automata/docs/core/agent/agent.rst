Automata.core.agent.agent.Agent
===============================

``Agent`` class is an abstract base class, used as blueprint for
creating autonomous agents that can perform tasks and communicate.
Instantiation and primary operations of the agent are defined within the
class and are often implemented in subclasses.

Overview
--------

The ``Agent`` is an abstract base class that contains several abstract
methods. These methods are ``__iter__``, ``__next__``, ``run`` and
``set_database_provider``. Derived classes that inherit from ``Agent``
must provide implementations for these methods.

Import Statement
----------------

.. code:: python

   from automata.core.agent.agent import Agent

Methods
-------

-  ``__init__ (self, instructions: str) -> None``:

   Constructor method that initializes an agent with a set of
   instructions and sets task completion status and
   ``database_provider`` to None.

-  ``__iter__ (self) -> None``:

   An abstract method that should be overridden in subclasses, and used
   for iterating over the agent.

-  ``__next__ (self) -> LLMIterationResult``:

   Abstract method used to move the agent one step forward in its task.
   Result of this operation is returned as an instance of
   ``LLMIterationResult``, or None if task either completed or isn’t
   initialized.

-  ``run (self) -> str``:

   Abstract method that should be overridden in subclasses. Designed to
   execute the agent’s task until it’s complete - meaning, until
   ``__next__`` method returns None. May raise an ``AgentError`` if an
   attempt is made to run a task that has already been completed or
   exceeds the permissible number of iterations.

-  ``set_database_provider (self, provider: LLMConversationDatabaseProvider) -> None``:

   Abstract method that should be overridden in subclasses. Used to set
   the iteration provider for the database. If an agent fails to set a
   database provider, ``AgentDatabaseError`` is raised.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.core.agent.error.AgentResultError``
-  ``automata.tests.conftest.task``
-  ``automata.tests.unit.sample_modules.sample2.PythonAgentToolkit.python_agent_python_task``
-  ``automata.core.agent.error.AgentGeneralError``
-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.core.agent.error.AgentDatabaseError``

Dependencies
------------

-  ``automata.core.llm.foundation.LLMConversationDatabaseProvider``

Limitations
-----------

The ``Agent`` class provides a foundation for creating classes for
specific autonomous agents. However, as it is an abstract base class, it
cannot be instantiated or used on its own. It must be subclassed and its
methods must be implemented according to the specific requirements of
the derived classes.

Follow-up Questions:
--------------------

-  What are some common agents that can be implemented from this base
   class?
-  Can we further expand the ``Agent`` class to include additional
   optional base functionalities?
