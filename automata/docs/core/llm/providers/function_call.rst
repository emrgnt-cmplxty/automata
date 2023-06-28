FunctionCall
============

``FunctionCall`` is a class representing a function call to be made by
the OpenAI agent. It provides methods to create a function call from a
response dictionary, handle the termination of a conversation, and
convert a ``FunctionCall`` object to a dictionary. The class is designed
to help process function call information, representing a function name
and its corresponding arguments as attributes.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.Person``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.core.base.task.ITaskExecution.execute``
-  ``automata.tests.unit.sample_modules.sample.Person.run``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage.__init__``
-  ``automata.tests.unit.sample_modules.sample.sample_function``
-  ``automata.core.base.task.TaskStatus``
-  ``automata.tests.unit.test_task_environment.test_commit_task``
-  ``automata.core.llm.completion.LLMChatCompletionProvider.__init__``
-  ``automata.tests.unit.sample_modules.sample.f``

Example
-------

Here’s an example of creating a ``FunctionCall`` object from a response
dictionary:

.. code:: python

   from automata.core.llm.providers.openai import FunctionCall

   response_dict = {
       "name": "sample_function",
       "arguments": '{"name": "John Doe"}',
   }

   function_call = FunctionCall.from_response_dict(response_dict)

Limitations
-----------

The handling of conversation termination in ``FunctionCall`` relies on a
hacky solution due to the problem of parsing Markdown with JSON. This
solution needs to be made more robust and generalizable. Further
improvements are required to ensure that the solution is adequate to
solve all possible problems associated with adopting a Markdown return
format.

Follow-up Questions:
--------------------

-  How can we improve the handling of conversation termination and
   parsing Markdown with JSON?
-  Is the current implementation sufficient to handle all possible
   cases, or are there any edge cases that might cause issues?
