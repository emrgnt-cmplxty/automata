AutomataActionExtractor
=======================

``AutomataActionExtractor`` is a class that is designed to extract
actions from a given input text. Actions can be of various types, such
as tool actions, agent actions, and result actions. The class provides
convenient methods to process the input text and return a list of
extracted actions.

Overview
--------

``AutomataActionExtractor`` processes input text and extracts the
relevant actions, which can be tool actions, agent actions, or result
actions. It is responsible for understanding and returning a list of
actions to be executed by an Automata Agent. The primary method of the
class is ``extract_actions``, which takes the input text and returns a
list of extracted actions.

Related Symbols
---------------

-  ``automata.core.agent.action.AutomataAction``
-  ``automata.core.agent.action.ToolAction``
-  ``automata.core.agent.action.AgentAction``
-  ``automata.core.agent.action.ResultAction``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.agent.agent_enums.ActionIndicator``
-  ``automata.core.agent.agent_enums.ResultField``
-  ``automata.core.agent.agent_enums.ToolField``
-  ``automata.config.config_types.AgentConfigName``

Example
-------

The following example demonstrates how to use
``AutomataActionExtractor`` to extract actions from a given input text:

.. code:: python

   from automata.core.agent.action import AutomataActionExtractor

   input_text = """
   - thoughts
       - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
   - actions
       - tool_query_0
           - tool_name
               - automata-indexer-retrieve-code
           - tool_args
               - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
   """

   actions = AutomataActionExtractor.extract_actions(input_text)
   print(actions[0].tool_name)  # Output: "automata-indexer-retrieve-code"
   print(actions[0].tool_args[0])  # Output: "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."

Limitations
-----------

The primary limitation of ``AutomataActionExtractor`` is that it relies
on a predefined format and structure of the input text. It expects the
actions to be specified in a certain way, and if the input text does not
conform to this format, the extraction of actions may fail or provide
incorrect results.

Follow-up Questions:
--------------------

-  How can we make ``AutomataActionExtractor`` more flexible and
   adaptable to varied input formats?
-  Are there more efficient ways to extract actions from the input text
   other than using string parsing and regex?
