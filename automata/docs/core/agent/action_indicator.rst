ActionIndicator
===============

``ActionIndicator`` is an enumeration that represents the action
indicator used in the action line of a tool. It provides a simple way to
define the type of action or operation performed by the tool.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.action.AutomataActionExtractor``

Example
-------

Here is an example of how to use the ``ActionIndicator`` enumeration in
your code:

.. code:: python

   from automata.core.agent.agent_enums import ActionIndicator

   action = ActionIndicator.ACTION_1
   print(action)
   # Output: ACTION_1

Limitations
-----------

``ActionIndicator`` is a simple enumeration and does not provide any
additional functionality or methods. It is only used for defining the
action indicator for a tool.

Follow-up Questions:
--------------------

-  What are the specific use cases for this enumeration in the context
   of tools and agents?
-  Are there any plans for extending the functionality of this
   enumeration in the future?
