LLMCompletionResult
===================

``LLMCompletionResult`` is a base class designed to manage different
types of LLM completion results. With two principal methods:
``get_content()`` and ``get_role()``, this class aids in fetching the
content and role associated with a completion result.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``
-  ``automata.llm.foundation.LLMConversation.get_latest_message``
-  ``automata.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
-  ``automata.config.base.LLMProvider``
-  ``automata.llm.providers.openai.OpenAIConversation.get_latest_message``
-  ``automata.llm.providers.openai.OpenAIChatMessage``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.llm.foundation.LLMChatCompletionProvider.get_next_assistant_completion``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``

Example
-------

In situations where it’s required to extract the content or role from a
completion result, ``LLMCompletionResult`` is applicable. Below is an
example illustrating its functionality.

.. code:: python

   from automata.llm.foundation import LLMCompletionResult

   # create an instance of LLMCompletionResult with defined role and content attributes
   completion_result = LLMCompletionResult(content="content of the completion result", role="assistant")

   # fetch the content
   content = completion_result.get_content()
   print(content)  # output should be "content of the completion result"

   # fetch the role
   role = completion_result.get_role()
   print(role)  # output should be "assistant"

Limitations
-----------

This class serves as a base class and it may not provide any specific
functionality beyond providing an interface for subclasses. Hence, if a
feature is not supported in this class, check the subclasses to see if
they have the feature needed.

Follow-up Questions:
--------------------

-  What are some practical use-cases of the ``LLMCompletionResult``?
-  Are there specific types of completion results this class can’t
   handle? If so, what alternative methods or classes should we use for
   such cases?
-  Are there any constraints or prerequisites for the content or the
   role of the completion result?
-  How does the ``LLMCompletionResult`` integrate with other components
   of Automata? What’s its role in the broader scheme?
