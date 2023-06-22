Action
======

``Action`` is an abstract class representing an action to be performed
by an Automata Agent. It is the base class for various action classes,
such as ``ToolAction``, ``ResultAction``, and ``AgentAction``. An action
can be created from a given configuration and supports creating an
instance of an Action subclass via the ``from_lines`` class method.

Related Symbols
---------------

-  ``automata.core.agent.action.ToolAction``
-  ``automata.core.agent.action.ResultAction``
-  ``automata.core.agent.action.AgentAction``

Example
-------

The following examples demonstrate how to create instances of
``ToolAction`` and ``ResultAction`` subclasses using the ``from_lines``
method:

.. code:: python

   from automata.core.agent.action import ToolAction, ResultAction
   from automata.tests.unit.test_automata_helpers import ActionExtractor

   # Creating a ToolAction instance
   input_text = textwrap.dedent(
       """
       - thoughts
           - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
       - actions
           - tool_query_0
               - tool_name
                   - automata-indexer-retrieve-code
               - tool_args
                   - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
       """
   )

   actions = ActionExtractor.extract_actions(input_text)
   tool_action = ToolAction.from_lines(actions[0])

   # Creating a ResultAction instance
   input_text = textwrap.dedent(
       """
       *Assistant*
           - thoughts
               - Having successfully written the output file, I can now return the result.
           - actions
               - return_result_0
                   - Function 'run' has been added to core.tests.sample_code.test.
       """
   )

   actions = ActionExtractor.extract_actions(input_text)
   result_action = ResultAction.from_lines(actions[0])

Limitations
-----------

The ``Action`` class is an abstract class and cannot be instantiated
directly. It relies on concrete subclass implementations, such as
``ToolAction``, ``ResultAction``, and ``AgentAction``. These subclasses
follow a specific configuration format and may not cover all possible
use cases.

Follow-up Questions:
--------------------

-  How can custom action classes be implemented and integrated into the
   system?
