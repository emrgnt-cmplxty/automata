MockAutomataInstance
====================

``MockAutomataInstance`` is a class that inherits from
``AutomataInstance``. It provides a simple example implementation of the
interface, and has a ``run`` method that takes an ``instruction`` as
input and returns a string indicating that the input instruction was
“run” on the instance.

Overview
--------

The ``MockAutomataInstance`` class demonstrates a basic implementation
of the ``AutomataInstance`` interface. It takes a ``config_name`` (of
type ``AgentConfigName``) and ``description`` (of type ``str``) as
arguments and initializes the instance with these. The ``run`` method
has a simple return statement for executing instructions while
demonstrating the use of the Automata Instance.

Related Symbols
---------------

-  ``automata.core.agent.coordinator.AutomataInstance``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.agent.action.AutomataActionExtractor``

Example
-------

The following is an example demonstrating how to create an instance of
``MockAutomataInstance``, run an instruction, and fetch its response.

.. code:: python

   from automata.tests.unit.test_automata_coordinator import MockAutomataInstance
   from config.config_types import AgentConfigName

   config_name = AgentConfigName.TEST
   description = "This is a mock Automata instance example."

   mock_instance = MockAutomataInstance(config_name=config_name, description=description)
   instruction = "fetch information"

   result = mock_instance.run(instruction)
   print(result)     # Output: "Running fetch information on test."

Limitations
-----------

``MockAutomataInstance`` is a simple example class and does not provide
any actual functionality beyond demonstrating the structure and use of
an Automata Instance. Moreover, it assumes a specific set of related
symbols to be available, which may not cover all cases and use
scenarios.

Follow-up Questions:
--------------------

-  Is there a more realistic example or use case that can be used to
   demonstrate the work of ``MockAutomataInstance``?
