FunctionCall
============

``FunctionCall`` is a class representing a function call to be made by
the OpenAI agent within the ``automata.llm.providers.openai`` module.

Overview
--------

``FunctionCall`` allows the OpenAI agent to perform a function call
within a conversation. It does this by encapsulating the name of the
function to be called and the arguments to be passed in the
conversation, if any. The class provides methods to create an instance
from the response dictionary received (``from_response_dict``), to
handle termination of a function call (``handle_termination``), and to
convert a function call into a dictionary representation (``to_dict``).

Related Symbols
---------------

-  ``automata.llm.providers.openai.OpenAIChatCompletionResult.get_function_call``
-  ``automata.llm.providers.openai.OpenAIChatMessage.__init__``
-  ``automata.tests.unit.sample_modules.sample.Person``
-  ``automata.tests.unit.sample_modules.sample.Person.run``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tasks.base.ITaskExecution.execute``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
-  ``automata.tests.unit.sample_modules.sample.sample_function``
-  ``automata.code_handling.py.writer.PyWriter.InvalidArguments``

Examples
--------

Below is a simple example to demonstrate interaction with
``FunctionCall``.

.. code:: python

   from automata.llm.providers.openai import FunctionCall

   # Creating an instance of FunctionCall
   fn_call = FunctionCall(name="functionName", arguments={"arg1":"value1", "arg2":"value2"})

   # Printing function call as dictionary
   print(fn_call.to_dict())

Discussion
----------

The class relies on JSON for serialization. One of the limitations of
``FunctionCall`` is the method ``handle_termination`` while parsing the
return format, especially with Markdown where JSON decode errors may
occur. This solution is considered hacky and needs to be more robust and
generalizable.

Follow-up Questions
-------------------

-  What is the exact role of ``FunctionCall`` in managing conversational
   flow, especially in terms of error recovery and edge cases?
-  How can ``FunctionCall`` be extended or customized for different
   conversation control models?
