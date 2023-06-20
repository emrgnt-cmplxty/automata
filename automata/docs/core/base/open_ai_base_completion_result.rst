OpenAIBaseCompletionResult
==========================

``OpenAIBaseCompletionResult`` is an abstract base class that provides
an interface for interacting with and extracting completions from
different OpenAI API completion results. Classes inheriting this
interface should implement the ``get_completions`` method to retrieve
the completion results.

Related Symbols
---------------

-  ``automata.core.base.openai.CompletionResult``

Example
-------

The following is an example demonstrating how to create an instance of a
class that inherits from ``OpenAIBaseCompletionResult`` and implements
the ``get_completions`` method.

.. code:: python

   from automata.core.base.openai import OpenAIBaseCompletionResult

   class MyCompletionResult(OpenAIBaseCompletionResult):
       def __init__(self, raw_data):
           super().__init__(raw_data)

       def get_completions(self) -> list[str]:
           return self.raw_data["choices"][0]["text"]

   # Assume raw_data is the response from an OpenAI API call
   raw_data = {
       'choices': [
           {
               'text': '...generated completion text...'
           }
       ]
   }

   completion_result = MyCompletionResult(raw_data)
   completions = completion_result.get_completions()
   print(completions)

Limitations
-----------

The primary limitation of ``OpenAIBaseCompletionResult`` is that it does
not provide any implementations for extracting completions from OpenAI
API results by default. Classes inheriting from this interface should
provide their own implementation of the ``get_completions`` method to
extract completions based on the specific API response format.

Follow-up Questions:
--------------------

-  How do we handle different API response formats when extracting
   completions from an inherited class of
   ``OpenAIBaseCompletionResult``?
