ResultField
===========

``ResultField`` is an enumeration class that represents the fields of a
result. These fields are essential for identifying and accessing
different parts of a result returned by a ``Tool``, ``Agent``, or
execution of a specific action like ``ResultAction``. The class provides
a fixed set of options that can be used to programmatically interact
with the results.

Related Symbols
---------------

-  ``automata.core.agent.agent_enums.ToolField``
-  ``automata.core.agent.agent_enums.AgentField``
-  ``automata.core.agent.action.ResultAction``
-  ``automata.core.base.openai.CompletionResult``

Example
-------

Here’s an example demonstrating how to use the ``ResultField`` enum to
process and access specific fields in a result:

.. code:: python

   from automata.core.agent.action import ResultAction
   from automata.core.agent.agent_enums import ResultField

   result_action = ResultAction(result_name="test_result", result_outputs=["output1", "output2", "output3"])

   if ResultField.NAME in result_action.result_outputs:
       print("The result name exists in the outputs:", result_action.result_name)

Limitations
-----------

The primary limitation of ``ResultField`` is that it provides a fixed
set of fields that are applicable to the results returned by ``Tool``,
``Agent``, or the execution of actions. Custom fields may not be
directly supported and might require extending the enumeration with
additional options.

Mock objects were referenced in the context. These have been replaced or
removed, as they are used only for testing purposes and should not be
relevant to the documentation.

Follow-up Questions:
--------------------

-  How can we extend the ``ResultField`` enum to support custom fields
   in results?
-  What other underlying objects might be worth highlighting for their
   interaction with ``ResultField``?
