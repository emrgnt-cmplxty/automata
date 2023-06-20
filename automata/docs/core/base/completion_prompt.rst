CompletionPrompt
================

``CompletionPrompt`` is a class that allows compatibility between chat
models and non-chat models, such as the ones used with
``openai.Completion.create``. It works by wrapping a provided prompt and
ensures the appropriate format is used depending on whether the model
accepts chat or non-chat prompts.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.base.tool.Tool``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``

Example
-------

Here’s an example showing how to use the ``CompletionPrompt`` class:

.. code:: python

   from automata.core.base.openai import CompletionPrompt

   raw_prompt = "Write a function that adds two numbers in Python."
   prompt_object = CompletionPrompt(raw_prompt)

   formatted_prompt = prompt_object.to_formatted_prompt()
   print(formatted_prompt)  # Output: "Write a function that adds two numbers in Python."

Limitations
-----------

The primary limitation of ``CompletionPrompt`` is that it doesn’t handle
model-specific prompt formatting, such as tokenization or special
formatting requirements that may be necessary for some models. However,
it provides a convenient way to switch between chat and non-chat prompts
quickly and with minimal changes to the input prompt.

Follow-up Questions:
--------------------

-  Are there any additional formatting requirements for specific models
   that should be handled by ``CompletionPrompt``?
