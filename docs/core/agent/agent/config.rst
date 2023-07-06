AgentInstance
=============

``AgentInstance`` is an abstract class used for implementing a specific
instance of an agent. An instance of an agent can be used to perform a
set of instructions multiple times without having to reinitialize the
agent each time.

Overview
--------

The agent instance object is created by ``create`` class method of
``AgentInstance`` by passing a config_name and description. It can be
run multiple times without having to reinitialize the agent each time.

Related Symbols
---------------

-  ``automata.agent.agent.Agent``
-  ``automata.agent.agent.AgentInstance.Config``
-  ``automata.agent.agent.AgentInstance.create``
-  ``automata.agent.providers.OpenAIAutomataAgent``
-  ``automata.agent.instances.OpenAIAutomataAgentInstance``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``

Example
-------

As ``AgentInstance`` is an abstract class, it can’t be instantiated
directly. However, you can create an instance of a class that inherits
from ``AgentInstance``. Here is how you can create an instance of
``OpenAIAutomataAgentInstance``.

.. code:: python

   from automata.agent.instances import OpenAIAutomataAgentInstance
   from automata.agent.config_enums import AgentConfigName

   config_name = AgentConfigName.TEST
   description = "This is a test instance"

   agent_instance = OpenAIAutomataAgentInstance.create(config_name=config_name, description=description)

Limitations
-----------

A critical limitation of ``AgentInstance`` is that it cannot handle
interactive instructions where user input may modify the subsequent
instructions. Also, as this is an abstract class, only classes that
inherit from ``AgentInstance`` can be instantiated and used.

Follow-up Questions:
--------------------

-  What are the responsibilities of the AgentInstance?
-  Can one create an instance of custom Agent that inherits from
   AgentInstance?
-  How does one implement their own version of ``AgentInstance``?
