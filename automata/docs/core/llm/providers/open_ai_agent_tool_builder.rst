OpenAIAgentToolkitBuilder
======================

``OpenAIAgentToolkitBuilder`` is an abstract class for building tools for
providers. It provides a base class for creating ``AgentToolkitBuilder``
implementations that work with providers that use OpenAI APIs (e.g.,
GPT-3).

Overview
--------

``OpenAIAgentToolkitBuilder`` inherits from ``AgentToolkitBuilder`` and
introduces an abstract method ``build_for_open_ai`` which needs to be
implemented by any concrete subclasses. This method should return a list
of ``OpenAITool`` instances, which are specialized versions of the
``Tool`` class designed to work with OpenAI agent tools.

Related Symbols
---------------

-  ``automata.core.agent.agent.AgentToolkitBuilder``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``
-  ``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``
-  ``automata.core.tools.builders.py_reader.PyReaderOpenAIToolkit``

Example
-------

The following example demonstrates how to create a custom
``OpenAIAgentToolkitBuilder`` implementation.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIAgentToolkitBuilder, OpenAITool

   class MyOpenAIToolkit(OpenAIAgentToolkitBuilder):
       TOOL_TYPE = "custom_tool"

       def build_for_open_ai(self) -> List[OpenAITool]:
           # Define the OpenAI-specific tools here, e.g.
           def my_openai_tool():
               """A custom tool that interacts with OpenAI API."""
               pass

           tools = [
               OpenAITool(
                   function=my_openai_tool,
                   name="my-openai-tool",
                   description="Execute a custom OpenAI tool.",
                   properties={
                       "input": {
                           "type": "string",
                           "description": "The input text for the tool.",
                       },
                   },
                   required=["input"],
               )
           ]
           return tools

Limitations
-----------

``OpenAIAgentToolkitBuilder`` is an abstract class and cannot be used
directly. It must be subclassed with implementations provided for the
``build_for_open_ai`` method. Another limitation is the reliance on the
specific OpenAI APIs or tools.

Follow-up Questions:
--------------------

-  What other abstract methods or properties could be included in
   ``OpenAIAgentToolkitBuilder`` to simplify building custom
   ``AgentToolkitBuilder`` implementations for OpenAI providers?
