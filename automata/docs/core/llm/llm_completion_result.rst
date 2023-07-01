LLMCompletionResult
===================

``LLMCompletionResult`` is a base class for different types of LLM
completion results. Subclasses can represent various completion sources,
such as the OpenAI API. The class provides methods to access the content
and role of the completion result.

Overview
--------

``LLMCompletionResult`` is an abstract base class that provides a common
interface for working with completion results from various sources. It
includes methods such as ``get_content()`` and ``get_role()``, which
return the content and role of the completion result, respectively. It
is meant to be subclassed and extended by specific completion result
types like ``OpenAIChatCompletionResult``.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``
-  ``automata.core.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``

Example
-------

The following example demonstrates how to subclass
``LLMCompletionResult`` to create a custom completion result class.

.. code:: python

   from automata.core.llm.foundation import LLMCompletionResult

   class CustomCompletionResult(LLMCompletionResult):
       def __init__(self, role: str, content: str, custom_data: Any):
           super().__init__(role=role, content=content)
           self.custom_data = custom_data

       def get_custom_data(self) -> Any:
           return self.custom_data

   # Usage:
   custom_completion = CustomCompletionResult(role="assistant", content="Hello, world!", custom_data={"extra": "data"})
   print(custom_completion.get_content())  # Output: Hello, world!
   print(custom_completion.get_role())  # Output: assistant
   print(custom_completion.get_custom_data())  # Output: {'extra': 'data'}

Limitations
-----------

As an abstract base class, ``LLMCompletionResult`` cannot be
instantiated directly and requires a subclass to implement the specific
details for a particular completion source. It also does not currently
provide support for additional metadata or functionality beyond the
content and role of the completion result.

Follow-up Questions:
--------------------

-  Are there any additional features or functionality that would be
   useful to include in the base ``LLMCompletionResult`` class?
-  How can this class be extended to support more diverse completion
   result types and sources?
