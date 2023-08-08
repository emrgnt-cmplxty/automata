CodeWritingEval
===============

Overview
--------

The ``CodeWritingEval`` class is designed to evaluate an LLM’s (Language
Learning Model) code writing ability. The LLMs are language learning
models designed for various language learning tasks.

The class provides functionalities to extract coding actions using the
``extract_action`` method, parsing code snippets and fetching relevant
details using the ``_parse_code_snippet`` method and filtering the
actions based on a specified condition using the ``_filter_actions``
method.

The class is inherited from ``AgentEval``, which is an abstract base
class for evaluating agent’s performance. The ``CodeWritingEval`` class
needs to implement the abstract methods of the parent class in order to
function correctly.

Related Symbols
---------------

-  ``automata.eval.agent.agent_eval.AgentEval``: Base class for Agent
   evaluation.
-  ``automata.eval.agent.openai_function_eval.OpenAIFunctionEval``: A
   concrete class for evaluating OpenAI messages for function call
   actions.

Example
-------

Below is an example of how to use the ``CodeWritingEval`` class:

.. code:: python

   from automata.eval.agent.code_writing_eval import CodeWritingEval
   from automata.llm.base_llm_message import LLMChatMessage

   # initialize CodeWritingEval with target variables
   code_eval = CodeWritingEval(target_variables=['x', 'y'])

   # Create a mock LLMChatMessage
   chat_message = LLMChatMessage(role='mock_role', content='x = 10; y = 20')

   # Extract coding action
   actions = code_eval.extract_action(chat_message)
   print(actions)  # it will print list of actions

Please note that ``LLMChatMessage`` is a mock object, which means, it’s
often impractical to create an instance in real environment. Production
usage of this class will generally involve actual data received from
LLM.

Limitations
-----------

Currently, the ``CodeWritingEval`` class assumes that the raw content
passed for parsing code snippets is in markdown format. So, it may fail
if the format is different. Furthermore, it expects the target variable
names to be available in advance before initializing
``CodeWritingEval``.

In terms of error handling, more specific exceptions could be thrown for
different error cases, currently, most of the errors throw
``CodeExecutionError`` which might not provide enough context to the
error.

Follow-up Questions:
--------------------

-  Is there a way for the ``CodeWritingEval`` class to handle other data
   formats apart from markdown?
-  What should be the correct approach in the case when the target
   variables are not known in advance?
-  Can there be a mechanism to provide more specific exceptions for
   different error cases?
