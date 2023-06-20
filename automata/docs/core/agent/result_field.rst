ResultField
===========

``ResultField`` is an enumeration class that represents the fields of a
result in the ``automata.core.agent.agent_enums`` module.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.symbol.graph.SymbolGraph``

Usage Example
-------------

.. code:: python

   from automata.core.agent.agent_enums import ResultField

   # Accessing a ResultField value
   result_field = ResultField.STATUS
   print(result_field.name)  # Output: STATUS
   print(result_field.value)  # Output: 1

Overview
--------

This enumeration is used in the context of the ``AutomataAgent`` and
other related classes during their processing and reporting stages to
access and manipulate specific fields in the generated result.

Limitations
-----------

``ResultField`` is a simple enumeration class with a limited set of
values. If more fields are required in the future, they need to be added
manually to this enumeration.

Follow-up Questions:
--------------------

-  Are there any plans to expand the list of fields in the
   ``ResultField`` enumeration?
