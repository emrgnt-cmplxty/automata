OpenAIAgentToolkitBuilder
=========================

``OpenAIAgentToolkitBuilder`` is an abstract class for building OpenAI
agent tools. It is used to define ``build_for_open_ai`` and
``can_handle`` as abstract methods. Developers intending to use OpenAI
for agents should subclass from ``OpenAIAgentToolkitBuilder`` and
provide implementations for these methods.

Overview
--------

Some classes that have implemented the ``OpenAIAgentToolkitBuilder``
abstract class include
``automata.core.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``,
``automata.core.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``,
and
``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``
among others. Every implementing class must define the
``build_for_open_ai`` method which returns a list of ``OpenAITool``
objects, and the ``can_handle`` method which checks if the class can
handle a given tool manager.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.agent.agent.AgentToolkitBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.core.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``

Example
-------

.. code:: python

   from automata.core.tools.builders.context_oracle import ContextOracleOpenAIToolkitBuilder

   class MyOpenAIToolkitBuilder(ContextOracleOpenAIToolkitBuilder):
       TOOL_TYPE = "my-type"

       def build_for_open_ai(self):
           # Create a list of OpenAITools here
           openai_tools = [OpenAITool(...), OpenAITool(...)]
           return openai_tools

The above example creates a subclass of
``ContextOracleOpenAIToolkitBuilder`` that builds OpenAI tools for the
``"my-type"`` toolkit.

Limitations
-----------

As ``OpenAIAgentToolkitBuilder`` is an abstract class, it cannot be
instantiated directly and must be subclassed with implementation
provided for the ``build_for_open_ai`` and ``can_handle`` methods.

Follow-up Questions:
--------------------

-  What happens if the subclass does not provide implementation for the
   ``build_for_open_ai`` and ``can_handle`` methods?
-  Can there be multiple ways to implement the ``build_for_open_ai``
   method or is there a particular way it should be done?
