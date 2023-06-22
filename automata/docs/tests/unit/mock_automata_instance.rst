MockAutomataInstance
====================

``MockAutomataInstance`` is a mock implementation of the
``AutomataInstance`` class. It provides a test-friendly representation
of a working ``AutomataInstance`` object, mainly for use with unit
tests. This class can be used to create instances that can simulate the
behavior of an ``AutomataInstance`` object, which can be helpful in the
context of unit testing.

Overview
--------

The main purpose of the ``MockAutomataInstance`` class is to act as a
test-friendly implementation of ``AutomataInstance``. By providing an
implementation of the ``.run()`` method, it allows users to create a
mock ``AutomataInstance`` that can simulate its behavior in unit
tests [1]_.

Related Symbols
---------------

-  ``automata.core.agent.coordinator.AutomataInstance``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.core.agent.coordinator.AutomataCoordinator``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

The following example demonstrates how to create a
``MockAutomataInstance`` and use it to simulate the behavior of an
``AutomataInstance`` object in a test environment.

.. code:: python

   from automata.tests.unit.test_automata_coordinator import MockAutomataInstance
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.TEST
   mock_instance = MockAutomataInstance(config_name=config_name, description="Mock Instance for Testing")
   result = mock_instance.run("sample_instruction")

   print(result)  # Output: Running sample_instruction on test.

Limitations
-----------

The ``MockAutomataInstance`` class is meant for testing purposes only
and should not be used in production code. It is a simplified
implementation and may not accurately represent all the behavior of a
real ``AutomataInstance``. In general, users should work with
``AutomataInstance`` objects directly.

Follow-up Questions:
--------------------

-  Are there other mock objects that should be included for testing
   purposes in the documentation?

.. [1]
   Mock objects are used in testing to simplify working with complex
   objects. The provided example uses a mock object which is meant for
   testing purposes only and should not be used in production code.
