AgentField
==========

``AgentField`` is an enumeration class representing the fields of an
agent in the Automata ecosystem. It is primarily used to work with and
organize the information required to initialize and manage providers.

Overview
--------

``AgentField`` consists of a set of field names that help identify,
categorize, and manage agent-related information. As a part of the
automata.core.agent.agent_enums module, it works together with other
enums like ``ResultField`` and ``ToolField`` to provide a comprehensive
and consistent way to work with agent-related data. This also makes it
easier to update or extend the agent fields as needed.

Related Symbols
---------------

-  ``automata.core.agent.agent_enums.ResultField``
-  ``automata.core.agent.agent_enums.ToolField``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``

Example
-------

The following example demonstrates how to use ``AgentField`` to extract
specific information from a dictionary containing agent-related data.

.. code:: python

   from automata.core.agent.agent_enums import AgentField

   agent_data = {
       "name": "SampleAgent",
       "status": "running",
       "completion_status": "in_progress",
   }

   # Accessing agent fields using AgentField enumeration
   agent_name = agent_data[AgentField.NAME.value]
   agent_status = agent_data[AgentField.STATUS.value]
   agent_completion = agent_data[AgentField.COMPLETION_STATUS.value]

   print("Agent Name:", agent_name)
   print("Agent Status:", agent_status)
   print("Agent Completion Status:", agent_completion)

Limitations
-----------

``AgentField`` is primarily used for working with agent-related
information, and its usage scope is limited to working with agent
fields. It may not be sufficient for handling more complex or customized
data structures.

Follow-up Questions:
--------------------

-  Are there any other use-cases or broader applications of
   ``AgentField`` that may be relevant in the future?
