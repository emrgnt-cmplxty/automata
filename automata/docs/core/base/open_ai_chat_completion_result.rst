OpenAIChatCompletionResult
==========================

``OpenAIChatCompletionResult`` is a class that handles the results
obtained from OpenAI’s chat completion API. It encapsulates the raw data
returned from the API and provides a convenient method to extract the
completion message. The class inherits from
``OpenAIBaseCompletionResult``.

Overview
--------

``OpenAIChatCompletionResult`` simplifies working with the results
obtained from the OpenAI chat completion API by making it easy to
extract the completion message from the raw API response. This class is
typically used by the ``AutomataAgent`` while interacting with the
OpenAI API.

Related Symbols
---------------

-  ``automata.core.base.openai.OpenAIBaseCompletionResult``
-  ``automata.core.base.openai.OpenAIChatMessage``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

The following example demonstrates how an instance of
``OpenAIChatCompletionResult`` can be created and used.

.. code:: python

   from automata.core.base.openai import OpenAIChatCompletionResult

   raw_data = {
       "choices": [
           {
               "message": {
                   "content": "This is a completion message from the OpenAI API."
               }
           }
       ]
   }

   result = OpenAIChatCompletionResult(raw_data)
   completion_message = result.get_completion()
   print(completion_message)

Limitations
-----------

``OpenAIChatCompletionResult`` relies on the specific structure of the
API response returned by the OpenAI chat completion API. If there are
any changes to the API response format, this class would need to be
updated to handle them. Additionally, it assumes that the completion
message is present in the ``raw_data`` dictionary at the ``"choices"``
key’s first element, and in cases where this is not accurate, it may
cause issues.

Follow-up Questions:
--------------------

-  How can we handle cases when there are multiple completion messages
   available in the API response?
