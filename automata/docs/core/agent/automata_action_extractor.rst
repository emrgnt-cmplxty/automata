AutomataActionExtractor
=======================

``AutomataActionExtractor`` is a helper class designed to assist in the
extraction of actions from a block of text. Actions are separated by
specific lines that denote the beginning and ending of particular
actions in the text.

Overview
--------

The ``AutomataActionExtractor`` class provides a single primary method,
``extract_actions``, which takes a text input and returns a list of
extracted actions from the text. It can identify and extract tool
actions, agent actions, and result actions. Each action is parsed
individually, and the output contains all the actions found in the text.

Related Symbols
---------------

-  ``symbol.symbol_types.Symbol``
-  ``agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``base.tool.Tool``
-  ``config.config_types.AutomataAgentConfig``
-  ``coding.py_coding.writer.PyCodeWriter``
-  ``config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``symbol.graph.SymbolGraph``
-  ``agent.coordinator.AutomataCoordinator``

Example
-------

Here is an example using the ``AutomataActionExtractor`` to extract
actions from a given text:

.. code:: python

   from automata.core.agent.action import AutomataActionExtractor

   text = """
   ;; [Tool]
   <tool_name> = <tool query>
   <tool_arg1>
   <tool_arg2>

   ;; [Agent]
   c = <agent query>
   <agent_instruction1>
   <agent_instruction2>

   ;; [Result]
   <result_name>
   <result_outputs>
   """

   action_extractor = AutomataActionExtractor()
   actions = action_extractor.extract_actions(text)
   print(actions)

Limitations
-----------

The limitations of ``AutomataActionExtractor`` include its dependency on
specific action indicators, and its inability to detect actions that do
not contain the required indicators. Also, the input text should be
formatted correctly, following the expected syntax for action indicators
and their respective fields.

Follow-up Questions:
--------------------

-  Can AutomataActionExtractor support other formats to describe actions
   in text?
