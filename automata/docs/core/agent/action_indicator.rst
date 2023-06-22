ActionIndicator
===============

``ActionIndicator`` is an enum class that represents the action
indicator for the action line of a tool. It is used in
``AutomataActionExtractor`` to help identify and parse actions from a
given text input.

Overview
--------

``ActionIndicator`` provides a simple and standardized way to identify
actions within a text input. It is primarily used by the
``AutomataActionExtractor`` class to extract action details for further
processing. The class offers a single Enum value, ``TOOL_QUERY``, which
represents the action line of a tool.

Related Symbols
---------------

-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.agent.agent_enums.ActionIndicator``
-  ``automata.core.agent.agent_enums.ToolField``
-  ``automata.core.base.tool.ToolkitType``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tests.unit.test_tool.TestTool``

Example
-------

The following example demonstrates how to use the ``ActionIndicator``
enum in conjunction with the ``AutomataActionExtractor`` class to
extract actions from a given text input.

.. code:: python

   from automata.core.agent.action import AutomataActionExtractor
   from automata.core.agent.agent_enums import ActionIndicator
   import textwrap

   input_text = textwrap.dedent(
       f"""
       - thoughts
           - I will use the action indicator {ActionIndicator.TOOL_QUERY.value} to identify actions in the text.
       - actions
           - tool_query_0
               - tool_name
                   - tool_1
               - tool_args
                   - arg1
       """
   )

   extracted_actions = AutomataActionExtractor.extract_actions(input_text)
   print("Extracted action's tool name: ", extracted_actions[0].tool_name)

Limitations
-----------

``ActionIndicator`` has a single enum value (``TOOL_QUERY``)
representing actions for tools. As a result, it might not be adequate
for more complex action extraction scenarios where multiple types of
actions need to be identified and distinguished within a text input.

Follow-up Questions:
--------------------

-  Are there plans to include other types of actions in ActionIndicator,
   and if so, how might they be differentiated from one another?
