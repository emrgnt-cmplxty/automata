OpenAIFunctionEval
==================

``OpenAIFunctionEval`` is an agent evaluator that interacts with OpenAI
messages for function call actions, stemming from the base class
AgentEval.

Overview
--------

``OpenAIFunctionEval`` provides an implementation to evaluate OpenAI
messages that include a function call action. The evaluator extracts the
function call action from the message and filters irrelevant actions,
returning a list of necessary actions meant for the OpenAI function in
the message.

Related Symbols
---------------

-  ``automata.llm.providers.openai_llm.OpenAIChatMessage.__str__``
-  ``automata.experimental.code_parsers.py.context_processing.context_utils.get_all_methods``
-  ``automata.agent.openai_agent.OpenAIAutomataAgent._get_next_user_response``
-  ``automata.experimental.code_parsers.py.context_processing.context_utils.is_private_method``
-  ``automata.tools.tool_base.Tool.run``
-  ``automata.llm.providers.openai_llm.OpenAIFunction.prompt_format``
-  ``automata.llm.providers.openai_llm.OpenAIChatCompletionResult.__str__``
-  ``automata.core.ast_handlers.find_syntax_tree_node.find_syntax_tree_node_pyast``
-  ``automata.llm.providers.openai_llm.OpenAIChatMessage.from_completion_result``

Example
-------

Below is an example of how to use ``OpenAIFunctionEval``:

.. code:: python

   from automata.eval.agent.openai_function_eval import OpenAIFunctionEval
   from automata.llm.providers.openai_llm import OpenAIChatMessage
   from automata.llm.model.llm import FunctionCallLLM

   # Instantiate an evaluator
   evaluator = OpenAIFunctionEval()

   # Create an OpenAIChatMessage with a function call
   message = OpenAIChatMessage(
       function_call=FunctionCallLLM(name="print_hello", arguments={})
   )

   # Extract actions from the message
   actions = evaluator.extract_action(message)

   # Now actions contains the action for the function call in the OpenAIChatMessage

Limitations
-----------

-  The ``OpenAIFunctionEval`` class depends on the ``OpenAIChatMessage``
   format and is tailored specifically for extracting function call
   actions. If a message does not conform to this format or if a
   function call is not included, it will not return any actions.
-  Since the evaluation is based on the assumption that the function
   call is found in a message, the presence of actions other than OpenAI
   function calls would not be recognized.

Follow-up Questions:
--------------------

-  How can this class be adapted or extended to handle different or more
   complex scenarios?
-  Is it possible to modify ``OpenAIFunctionEval`` to handle other types
   of actions beyond function calls?
