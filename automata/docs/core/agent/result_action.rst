ResultAction
============

``ResultAction`` is a class that represents a specific action to be
performed by an ``AutomataAgent``. It is primarily used in the context
of agent instructions and interactions. ResultAction instances are
created from a name and a list of outputs.

Overview
--------

This class inherits from the base ``Action`` class and implements its
abstract methods. The main capabilities of ``ResultAction`` include
initialization, conversion to a string representation, and creating an
instance from a list of lines and an index. The ``from_lines`` method
provides a convenient way to extract ResultAction instances from a
provided sequence of lines in the AutomataActions configuration format.

Related Symbols
---------------

-  ``automata.core.agent.agent_enums.ActionIndicator``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.tests.unit.test_automata_helpers``

Usage Example
-------------

Here’s an example of how to create an instance of ``ResultAction`` and
display its string representation:

.. code:: python

   from automata.core.agent.action import ResultAction

   result_name = "return_result_0"
   result_outputs = ["Function 'run' has been added to core.tests.sample_code.test."]
   result_action = ResultAction(result_name, result_outputs)

   print(str(result_action))

This would output:

::

   ResultAction(name=return_result_0, outputs=['Function \'run\' has been added to core.tests.sample_code.test.'])

Limitations
-----------

It’s important to note that the ``ResultAction`` class assumes a
specific format for the provided sequence of lines when parsing for
ResultAction instances. Any changes in the format would require updating
the parsing logic in the ``from_lines`` method.

Follow-up Questions:
--------------------

-  How can we make the ``from_lines`` method more flexible to handle
   changes in the AutomataActions configuration format?
