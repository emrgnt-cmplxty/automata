OpenAITool
==========

Overview
--------

``OpenAITool`` is a class intended to represent a tool that can be
implemented by the OpenAI agent. This class mainly provides
functionalities for initializing OpenAI tools with specific functions,
names, descriptions, properties, and requirements. The initialization
process of ``OpenAITool`` involves invoking the ``OpenAIFunction``
class.

This class is primarily used by OpenAI’s toolkit builders, such as
``ContextOracleOpenAIToolkitBuilder``, ``PyWriterOpenAIToolkitBuilder``,
and ``SymbolSearchOpenAIToolkitBuilder``, to create lists of
``OpenAITool`` instances for OpenAI.

Related Symbols
---------------

-  ``automata.core.embedding.base.EmbeddingVectorProvider``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.foundation.LLMCompletionResult``
-  ``automata.core.llm.foundation.LLMConversation``
-  ``automata.core.tools.base.Tool``
-  ``automata.tests.unit.test_tool.TestTool``

Example
-------

Below is an example of how to instantiate an ``OpenAITool`` using the
test tool as a function, which simply returns a string “TestTool
response” irrespective of the input provided.

.. code:: python

   from automata.core.llm.providers.openai import OpenAITool
   from automata.tests.unit.test_tool import TestTool

   tool = TestTool(
       name="TestTool",
       description="A test tool for testing purposes",
       function=lambda x: "TestTool response",
   )

   openai_tool = OpenAITool(
       function=tool.run,
       name=tool.name,
       description=tool.description,
       properties={'test_prop': {'description': 'A test property', 'type': 'string'}},
   )

Here the ``run`` method of the ``TestTool`` instance ``tool`` is passed
as the ``function`` parameter to ``OpenAITool``. The ``properties`` is a
dictionary that includes additional data about the tool, such as a
description and type for each property. The ``name`` and ``description``
are self-explanatory.

Limitations
-----------

The OpenAITool provides a basic framework to facilitate the creation and
usage of tools for the OpenAI agent. The actual functionality of the
tool would largely depend on the function passed during its
instantiation. Also, even though it provides a property variable for
additional data storage, it does not inherently provide methods to
handle or manipulate these properties.

Follow-up Questions:
--------------------

-  How are the properties of the OpenAITool used in the toolkit builders
   and eventually by the OpenAI agent?
-  Are there any specific requirements or constraints for the function
   that is passed during the initialisation of an OpenAITool?
