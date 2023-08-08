OpenAIFunctionCallAction
========================

``OpenAIFunctionCallAction`` is a concrete Action class that represents
a function call from the OpenAI API. The class contains a name and
arguments attribute which store the function name and the arguments that
function requires. It is part of the OpenAI Software Development Kit
used for controlling and managing actions within the Autonomous System.

Overview
--------

``OpenAIFunctionCallAction`` implements functionalities for comparing
instances, hashing, converting itself into readable string format, and
payload processing which includes conversion to and from payload data.
The payload-related functionalities are critical when persisting and
retrieving instances from storage.

Related Symbols
---------------

-  ``automata.eval.agent.openai_function_eval.OpenAIFunctionEval._filter_actions``
-  ``automata.llm.providers.openai_llm.OpenAITool.__init__``
-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionResult.from_args``
-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionResult.get_function_call``
-  ``automata.eval.tool.tool_eval.ToolEval.extract_action``
-  ``automata.llm.providers.openai_llm.OpenAIChatMessage.__init__``
-  ``automata.tools.tool_executor.ToolExecution.execute``
-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionProvider.__init__``
-  ``automata.llm.llm_base.FunctionCall.from_response_dict``
-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionProvider.get_next_assistant_completion``

Examples
--------

Here’s an example of how to instantiate and use
``OpenAIFunctionCallAction``.

   Please note that actual OpenAI function names and arguments have not
   been provided in this example.

.. code:: python

   from automata.eval.agent.openai_function_eval import OpenAIFunctionCallAction

   name = 'fake_openai_function'
   arguments = {'arg1': 'value1', 'arg2': 'value2'}

   OpenAI_action = OpenAIFunctionCallAction(name, arguments)

   print(OpenAI_action)

Limitations
-----------

As a specialized ``Action`` subclass, ``OpenAIFunctionCallAction`` is
tailored for function calls in the OpenAI API, thus it won’t work for
other kinds of actions or function calls in different contexts. The
seamless use of this class assumes a working understanding of the OpenAI
API and its function calls. Furthermore, while it provides a
``from_payload`` method for creating instances from saved data, the
corresponding ``to_payload`` method doesn’t save the whole state of the
object, just the action name and arguments.

Follow-up Questions:
--------------------

-  What are all the available functions for the OpenAI API that can be
   used with ``OpenAIFunctionCallAction``?
-  What are some specific arguments some OpenAI functions take and in
   what format should they be provided?
-  How can the process of saving and retrieving
   ``OpenAIFunctionCallAction`` instances be improved to capture more
   aspects of the object’s state?
