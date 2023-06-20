AgentAction
===========

``AgentAction`` is a class that represents an action to be executed by
an AutomataAgent. It contains the agent configuration version, the agent
query, and the instructions for the agent. It also provides a method to
create an instance of ``AgentAction`` from a list of lines and an index
from a configuration file.

Overview
--------

The ``AgentAction`` class provides a way to represent and create an
instance of an action for an AutomataAgent. It’s useful in scenarios
where you want to specify the agent configuration version, agent query,
and instructions to be executed by the agent. The class also provides a
method to create an instance of ``AgentAction`` from a list of lines and
an index, allowing for easy parsing of agent action configurations.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``config.config_types.AutomataAgentConfig``

Example
-------

Here’s an example demonstrating how to create an instance of
``AgentAction``:

.. code:: python

   from automata.core.agent.action import AgentAction
   from config.config_types import AgentConfigName

   agent_version = AgentConfigName.AUTOMATA_MAIN
   agent_query = "Perform Code Analysis"
   agent_instruction = ["Analyze the code to find potential issues"]

   agent_action = AgentAction(agent_version, agent_query, agent_instruction)
   print(agent_action)

Limitations
-----------

The primary limitation of ``AgentAction`` is that it assumes a specific
format and structure for the input configuration lines and index when
using the ``from_lines`` method. If the format is not as expected, it
might not work correctly.

Follow-up Questions:
--------------------

-  How can ``AgentAction`` accommodate different configuration formats
   or custom configuration files when creating an instance from lines
   and an index?
