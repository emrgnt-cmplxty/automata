AutomataOpenAIAgentInstance
===========================

``AutomataOpenAIAgentInstance`` is a class representing an instance of
an Automata OpenAI agent. It inherits from the ``AgentInstance``
abstract class and implements the ``run`` method, which dictates how the
agent operates given a set of instructions.

Overview
--------

The ``AutomataOpenAIAgentInstance`` class is responsible for executing
specified instructions on an agent built from the instance’s
configuration and returning the result. The ``run`` method uses the
``AutomataAgentConfigFactory`` to dynamically create an agent
configuration.

Related Symbols
---------------

-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance``
-  ``automata.config.agent_config_builder.AutomataAgentConfigFactory``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.base.agent.AgentInstance``
-  ``automata.core.agent.agents.AutomataOpenAIAgent``
-  ``automata.config.agent_config_builder``

Example
-------

The following example demonstrates how to create and run an
``AutomataOpenAIAgentInstance``.

.. code:: python

   from automata.core.agent.instances import AutomataOpenAIAgentInstance
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   instance = AutomataOpenAIAgentInstance(config_name)
   instructions = "Get the summary of Python programming language."
   result = instance.run(instructions)
   print(result)

Method
------

run
~~~

The ``run`` method takes an ``instructions`` argument and returns the
output produced by the agent.

.. code:: python

   def run(self, instructions: str) -> str:
       pass

Args
^^^^

-  ``instructions`` (``str``): The instructions to be executed by the
   agent.

Returns
^^^^^^^

-  ``str``: The output produced by the agent.

Raises
^^^^^^

-  ``Exception``: If any error occurs during agent execution.

Limitations
-----------

The primary limitation of ``AutomataOpenAIAgentInstance`` is that it
depends on the OpenAI API, which may change over time and require
adjustments to the Automata agent configuration or usage. It also relies
on the predefined configuration files based on ``AgentConfigName``. In
addition, it assumes a specific directory structure for the
configuration files.

Follow-up Questions:
--------------------

-  How can we include custom configuration files for loading into the
   ``AutomataAgentConfigFactory``?
-  How can we handle changes in the OpenAI API, while maintaining
   compatibility with the ``AutomataOpenAIAgentInstance`` class?
