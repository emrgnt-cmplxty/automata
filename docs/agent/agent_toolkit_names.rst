AgentToolkitNames
=================

``AgentToolkitNames`` is an enumerated class that defines the different
types of agent tools available. These names correspond to various types
of agent tools. This enum provides an easy way to identify an agent tool
through its name.

The associated builders, which construct corresponding agent tools, can
be found in the ``automata/core/agent/builder/*`` directory.

Overview
--------

``AgentToolkitNames`` is a ``Python Enum`` that provides symbolic names
to the agent tools used within the OpenAI Automata system. It helps in
maintaining a clean, clear enumeration and handling of agent toolkit
names.

This enum consists of several members:

-  SYMBOL_SEARCH
-  ADVANCED_CONTEXT_ORACLE
-  DOCUMENT_ORACLE
-  PY_READER
-  PY_WRITER
-  PY_INTERPRETER
-  AGENTIFIED_SEARCH

These names, when used, are replaced by their respective string values
``'symbol-search'``, ``'advanced-context-oracle'``,
``'document-oracle'``, ``'py-reader'``, ``'py-writer'``,
``'py-interpreter'``, and ``'agent-search'``.

Related Symbols
---------------

-  ``automata.agent.openai_agent.OpenAIAutomataAgent``
-  ``automata.tools.agent_tool_factory.AgentToolFactory``
-  ``automata.agent.openai_agent.OpenAIAgentToolkitBuilder``
-  ``automata.tools.tool_base.Tool``
-  ``automata.llm.providers.openai_llm.OpenAITool``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder``
-  ``automata.experimental.tools.builders.document_oracle_builder.DocumentOracleOpenAIToolkitBuilder``
-  ``automata.experimental.tools.builders.agentified_search_builder.AgentifiedSearchOpenAIToolkitBuilder``

Example
-------

The following example demonstrates how to access one of the enumerations
in the AgentToolkitNames Enum.

.. code:: python

   from automata.agent.agent import AgentToolkitNames

   agent_tool = AgentToolkitNames.SYMBOL_SEARCH
   print(agent_tool)  # outputs: AgentToolkitNames.SYMBOL_SEARCH
   print(agent_tool.value)  # outputs: 'symbol-search'

Limitations
-----------

While the ``AgentToolkitNames`` enum offers a convenient way to maintain
a list of agent toolkit names, one limitation is that the associated
agent tools need to be implemented and their builders need to be located
in the ``automata/core/agent/builder/*`` directory.

Follow-up Questions:
--------------------

-  Is it possible to dynamically add new agent tool names to this enum
   at runtime?
-  How are builders associated with the agent tools and how are they
   retrieved given an ``AgentToolkitNames`` value?
