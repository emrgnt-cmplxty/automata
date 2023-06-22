CompletionResult
================

``CompletionResult`` is an abstract base class representing the result
of an OpenAI API completion request. It serves as a base model for
different types of completion results, such as
``OpenAIBaseCompletionResult`` and ``OpenAIChatCompletionResult``. The
primary method exposed by the class is ``get_completions``, which
returns a list of generated completions based on the API response.

Related Symbols
---------------

-  ``automata.core.base.openai.OpenAIBaseCompletionResult``
-  ``automata.core.base.openai.OpenAIChatCompletionResult``

Example
-------

The following example demonstrates how to get completions from an
instance of ``OpenAIBaseCompletionResult``.

.. code:: python

   from automata.core.base.openai import OpenAIBaseCompletionResult

   # Assume `raw_data` is the API response data containing choice objects
   raw_data = {
       "choices": [
           {
               "text": "This is the first completion."
           },
           {
               "text": "This is the second completion."
           }
       ]
   }

   completion_result = OpenAIBaseCompletionResult(raw_data)
   completions = completion_result.get_completions()

   assert completions == [
       "This is the first completion.",
       "This is the second completion."
   ]

Limitations
-----------

``CompletionResult`` serves as an abstract base class, and its usability
is limited to its subclasses, which provide specific implementations for
handling various completion scenarios. When dealing with different types
of API responses and desired output formats, using the subclass that
handles those specific requirements is necessary.

Follow-up Questions:
--------------------

-  What are some common use cases for different subclasses of
   ``CompletionResult`` that handle unique circumstances or
   requirements?
-  Are there other limitations or nuances when working with
   ``CompletionResult`` missing from this documentation?
