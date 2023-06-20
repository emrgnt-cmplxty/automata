AutomataAgentConfigFactory
==========================

``AutomataAgentConfigFactory`` is a class that provides a method for
creating ``AutomataAgentConfig`` instances with the given arguments in a
flexible and easy-to-use way. The main method provided by this class is
``create_config`` which takes variable-length argument lists and
arbitrary keyword arguments.

Overview
--------

The ``AutomataAgentConfigFactory`` class contains one static method,
``create_config``, which creates an ``AutomataAgentConfig`` instance
based on the given arguments. Internally, ``create_config`` uses the
``AutomataAgentConfigBuilder`` class to interactively set required agent
configurations and instantiate the agent accordingly.

Related Symbols
---------------

-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.config.agent_config_builder.build_llm_toolkits``

Example
-------

The following example demonstrates how to create an instance of
``AutomataAgentConfig`` using the ``AutomataAgentConfigFactory``.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigFactory
   from automata.config.config_types import AgentConfigName

   config = AutomataAgentConfigFactory.create_config(main_config_name=AgentConfigName.AUTOMATA_MAIN)

Limitations
-----------

``AutomataAgentConfigFactory`` relies on the
``AutomataAgentConfigBuilder`` class, which in turn depends on the
predefined configuration files based on ``AgentConfigName``. Thus,
``AutomataAgentConfigFactory`` can only create configurations from those
files and cannot create custom configurations that are not defined
within the existing configuration files.

Follow-up Questions:
--------------------

-  Is there a way to provide a custom configuration file to the
   ``AutomataAgentConfigFactory`` in order to create an agent with a
   custom configuration?
