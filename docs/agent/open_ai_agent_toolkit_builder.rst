OpenAIAgentToolkitBuilder
=========================

Overview
--------

``OpenAIAgentToolkitBuilder`` is an abstract class which means it cannot
be initialized itself. It is used to create robust classes that manage
and build tools for OpenAI agents.

It’s an essential piece in building tools for different types of
toolkits. For instance, builders for SymbolSearch, DocumentOracle,
AgentifiedSearch and Python code reading are subclasses of
``OpenAIAgentToolkitBuilder``. Each of those specific builders are able
to construct a list of appropriate ``OpenAITool``\ ’s, which can be used
by the OpenAI agents for various purposes such as code symbol search,
document search using oracles, or executing tasks using Python code.

The ``OpenAIAgentToolkitBuilder`` class contains two necessary methods:
- ``build_for_open_ai()``: An abstract method that, when implemented,
should build and return a list of ``OpenAITool`` objects. -
``can_handle()``: A class method that checks if the builder matches the
expected tool manager type.

Related Symbols
---------------

-  ``automata.llm.providers.openai_llm.OpenAITool``: A class that
   represents a tool which can be used by the OpenAI agent.
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder``:
   A class for interacting with the SymbolSearch API, to search indexed
   python codebase.
-  ``automata.tools.agent_tool_factory.AgentToolFactory``: The class is
   responsible for creating tools from a given agent tool name.
-  ``automata.tools.agent_tool_factory.AgentToolFactory.create_tools_from_builder``:
   A static method that uses the Builder Registry to create tools from a
   given agent tool name.
-  ``automata.agent.agent.AgentToolkitNames``: An enum for the different
   types of agent tools.

Example
-------

Due to the fact that ``OpenAIAgentToolkitBuilder`` is an abstract class
and cannot be instantiated on its own, we will show the instantiation of
its subclass ``SymbolSearchToolkitBuilder``:

.. code:: python

   from automata.experimental.tools.builders.symbol_search_builder import SymbolSearchToolkitBuilder
   from automata.llm.providers.symbol_search import SymbolSearch

   # initialize symbols search 
   symbol_search = SymbolSearch()

   # initialize builder
   symbol_search_builder = SymbolSearchToolkitBuilder(symbol_search=symbol_search)

The ``build`` method can then be called on the symbol_search_builder
object to construct a set of tools for that purpose:

.. code:: python

   tools = symbol_search_builder.build()

Limitations
-----------

The ``OpenAIAgentToolkitBuilder`` itself is an abstract class, which
requires it to be subclassed and its abstract methods to be implemented
in order to be fully utilized. This design may limit the flexibility for
direct usage.

Another limitation revolves around ``OpenAIAgentToolkitBuilder.mro()``.
Since it is an abstract method, its implementation is dependent on what
is defined in subclasses. This implies that the tasks that the created
tools can perform are limited to the responsibilities defined by the
subclasses.

Follow-up Questions
-------------------

-  What other concrete builders can be created by inheriting
   ``OpenAIAgentToolkitBuilder``?
-  How may additional functionality be added to the builder without
   changing the current subclasses?
