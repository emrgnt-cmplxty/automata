AgentifiedSearchOpenAIToolkitBuilder
====================================

Overview
--------

``AgentifiedSearchOpenAIToolkitBuilder`` is a class extending the
``AgentifiedSearchToolkitBuilder`` and ``OpenAIAgentToolkitBuilder``,
associated with the Agent Toolkit ``AGENTIFIED_SEARCH``. This class is
designed to build tools for agentified search functionality using the
OpenAI API.

The ``build_for_open_ai`` method is used to build and return a list of
OpenAITool objects based on the tools associated with agentified search.
The properties for the created ``OpenAITool`` objects include a query of
string type.

Related Symbols
---------------

-  ``automata.experimental.tools.builders.agentified_search_builder.AgentifiedSearchToolkitBuilder``
-  ``automata.llm.providers.openai_llm.OpenAIConversation.add_message``
-  ``automata.singletons.github_client.GitHubClient.create_issue``
-  ``automata.tasks.task_environment.AutomataTaskEnvironment.commit_task``
-  ``automata.tasks.task_database.AutomataAgentTaskDatabase.get_tasks_by_query``

Example
-------

.. code:: python

   from automata.experimental.tools.builders.agentified_search_builder import AgentifiedSearchOpenAIToolkitBuilder

   # Create an instance of the class
   tool_builder = AgentifiedSearchOpenAIToolkitBuilder()

   # Build the tools for OpenAI
   openai_tools = tool_builder.build_for_open_ai()

This script begins by importing necessary class
``AgentifiedSearchOpenAIToolkitBuilder``. An instance of this class is
then created. Finally, the tools for agentified search for OpenAI are
built and returned, using the ``build_for_open_ai`` method.

Limitations
-----------

``AgentifiedSearchOpenAIToolkitBuilder`` is a builder specifically
designed for agentified search with an OpenAI LLM Provider. This implies
that it may not be suited or compatible with other LLM Providers. The
properties of the built ``OpenAITool`` contains only ‘query’. If you
want to include additional properties, it may require changes in the
builder or an extended implementation.

Follow-up Questions:
--------------------

-  How compatible is ``AgentifiedSearchOpenAIToolkitBuilder`` with other
   LLM Providers?
-  How can additional properties, if required, be added to the built
   OpenAITools?

The context references symbols related to Git tasks, such as
``commit_task`` and ``create_issue``, as well as ones to paths and
indexing, such as ``get_project_paths`` and ``_load_index_protobuf``.
However, it’s unclear how these are connected or used in conjunction
with ``AgentifiedSearchOpenAIToolkitBuilder``. Better clarity on these
relationships is needed.
