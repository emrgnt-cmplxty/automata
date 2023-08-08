AgentEvalSetLoader
==================

Overview
--------

The ``AgentEvalSetLoader`` provides a mechanism for loading a set of
tasks from a specified JSON file. These tasks are used for agent
evaluation in test scenarios, with each task representing a particular
scenario that the agent must execute.

A task consists of an instruction string and an expected actions list,
the format of which are validated during the loading process. If there’s
any inconsistency in the format, ``ValueError`` exceptions are raised.
The class only supports JSON files and will raise ``ValueError`` if a
non-JSON file is passed to it.

The payload of tasks and their expected actions are loaded from the JSON
file in its constructor, and they can be accessed through the ``tasks``
and ``tasks_expected_actions`` instance properties respectively.

Related Symbols
---------------

-  ``automata.eval.tool.tool_eval_harness.ToolEvalSetLoader.load_json``
-  ``automata.eval.tool.tool_eval_harness.ToolEvalSetLoader.__init__``
-  ``automata.cli.cli_utils.initialize_py_module_loader``
-  ``automata.cli.commands.run_tool_eval``
-  ``automata.llm.providers.openai_llm.OpenAIEmbeddingProvider.__init__``
-  ``automata.experimental.scripts.run_update_tool_eval.process_payload``
-  ``automata.experimental.scripts.run_update_tool_eval.main``
-  ``automata.eval.tool.tool_eval.ToolEval._filter_actions``
-  ``automata.experimental.tools.builders.symbol_search_builder.SearchTool``

Example
-------

The following is an example of creating an instance of
``AgentEvalSetLoader``, it assumes that there is a valid JSON file with
the necessary tasks data.

.. code:: python

   from automata.eval.agent.agent_eval_harness import AgentEvalSetLoader

   file_path = "filepath_to_json"
   agent_eval_set_loader = AgentEvalSetLoader(filepath=file_path)

Upon instantiating the ``AgentEvalSetLoader``, the provided JSON file is
read and validated, the tasks and associated expected actions are loaded
and stored in ``tasks`` and ``tasks_expected_actions`` properties
respectively and can be used as needed.

Limitations
-----------

The ``AgentEvalSetLoader`` currently only supports task data in JSON
format and the tasks data should adhere to a particular structure - a
‘instructions’ field that contains a string and an ‘expected_actions’
field that contains a list of dictionaries.

It also doesn’t support variants of JSON like JSONL (or
newline-delimited JSON) or any other data formats like XML or CSV. These
limitations may restrict the applicability of the module for use cases
that store task data in formats other than standard JSON, or structured
differently.

Follow-up Questions:
--------------------

-  Is there a plan for supporting other data formats like XML or CSV, or
   variants of JSON like JSONL?
-  Could we consider extending the functionality to allow for some
   flexibility in the structure of the tasks data?

The class contains an embedded function (``format_values``) only used
within the ``load_json()`` function and it’s not directly accessible
outside the class instance. This design choice may or may not be best, a
follow-up question could be:

-  What was the rationale behind not making the ``format_values``
   function a separate method in the ``AgentEvalSetLoader`` class?
