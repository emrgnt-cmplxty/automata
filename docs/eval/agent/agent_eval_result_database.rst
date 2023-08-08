AgentEvalResultDatabase
=======================

``AgentEvalResultDatabase`` is a subclass of ``SQLDatabase`` that is
specifically designed to write agent evaluation results to a SQLite
database. It serves as a reliable storage system for recording and
retrieving evaluation results from different sessions and runs.

Attributes of the class include a table name, entry name, and a table
schema which constitutes session ID and run ID. These properties are
used to structure the SQLite database that the class interacts with.

Overview
--------

The ``AgentEvalResultDatabase`` class has two key methods:
``write_result`` and ``get_results``.

The ``write_result`` method takes an ``AgentEvalResult`` object as input
and writes it to the database. During this process, it checks if a
session ID has been set for the evaluation result, raising a
``ValueError`` if none exist.

The ``get_results`` method provides a way to retrieve evaluation results
from the database, accepting either a ``session_id`` or ``run_id`` as
parameters. Without these parameters, the method raises a
``ValueError``. If successful, the method returns a list of
``AgentEvalResult`` objects.

Related Symbols
---------------

-  ``automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.total_evaluations``
-  ``automata.experimental.tools.builders.agentified_search_builder.AgentifiedSearchToolkitBuilder._agent_selected_best_match``
-  ``automata.eval.tool.search_eval.SymbolSearchEval.to_tool_result``
-  ``automata.eval.agent.agent_eval_metrics.AgentEvaluationMetrics.__str__``

Example
-------

Here is a simple example explaining how to use
``AgentEvalResultDatabase``:

.. code:: python

   from automata.eval.agent.agent_eval_database import AgentEvalResultDatabase
   from automata.eval.agent.agent_eval_result import AgentEvalResult

   # Initialization
   db = AgentEvalResultDatabase(db_path="/path/to/database")

   # Creating an AgentEvalResult object
   eval_result = AgentEvalResult(session_id="123", run_id="456", total_evaluations=10)

   # Writing the result to the database
   db.write_result(eval_result)

   # Getting the results from the database by session_id
   results = db.get_results(session_id="123")

Please replace “/path/to/database” with the actual path where you want
to store your SQLite database file.

Limitations
-----------

The ``AgentEvalResultDatabase`` class only accepts ``AgentEvalResult``
objects. Therefore, it cannot directly handle other types of evaluation
results unless they are transformed into ``AgentEvalResult`` instances.
Furthermore, this class does not support concurrent database access
which may result in a locked database error.

Follow-up Questions:
--------------------

-  Could there be a form of support for handling other kinds of
   evaluation results directly?
-  How might concurrent database access be supported by
   ``AgentEvalResultDatabase`` to prevent database lock issues?
-  What happens if a non-existent ``session_id`` or ``run_id`` is used
   in ``get_results`` function?
