SymbolSearchEvalResult
======================

Overview
--------

The SymbolSearchEvalResult class inherits from ToolEvalResult. It is a
specific implementation tailored to represent the result of a symbol
search evaluation. Instances of this class store the expected and
observed actions which pertain to symbol searches as well as the top
match and top k matches from the observed action’s search results. It
also stores the first match from expected action’s search results as
expected match.

Throughout its methods and properties, the checks and interactions are
primarily concerned with these aforementioned actions and matches.
Furthermore, it offers functionality to check for full and partial match
occurrences and to convert the SymbolSearchEvalResult instance into a
serializable format or create an SymbolSearchEvalResult instance from a
serializable format.

Related Symbols
---------------

-  ``automata.cli.scripts.run_code_embedding.collect_symbols``
-  ``automata.symbol.graph.symbol_navigator.SymbolGraphNavigator.get_references_to_symbol``
-  ``automata.symbol.symbol_parser._SymbolParser.parse_descriptors``
-  ``automata.symbol.symbol_base.Symbol.py_kind``
-  ``automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.total_partial_matches``
-  ``automata.symbol.symbol_parser._SymbolParser.error``
-  ``automata.symbol.symbol_base.Symbol.parent``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder.build``
-  ``automata.symbol.graph.symbol_references.ReferenceProcessor``

Example
-------

The following is an example demonstrating instantiation of an
SymbolSearchEvalResult object with an expected and observed action of
type SymbolSearchAction.

.. code:: python

   from automata.eval.tool.search_eval import SymbolSearchEvalResult
   from automata.eval.action import SymbolSearchAction

   expected_action = SymbolSearchAction(...)
   observed_action = SymbolSearchAction(...)

   result = SymbolSearchEvalResult(expected_action, observed_action)

**Note:** This is the most basic usage example. It is assumed that you
replace the ellipsis (…) with the required parameters to construct a
SymbolSearchAction. The expected and observed actions must be of type
SymbolSearchAction, and each should ideally hold a list of symbol search
results sorted in the order of relevance.

Limitations
-----------

Due to dependency on third-party terminologies like ‘Symbol’, ‘Action’,
etc. from external modules, changes made to these dependencies in future
can impact the working of this class. The class logic is strongly
coupled with the order of the ‘search_results’ list in the expected and
observed actions, having the first entry as the most important/ relevant
search result. If this order is not maintained, the logic of this class
might not work as expected.

Follow-up Questions:
--------------------

-  How can we handle instances where the expected or observed actions
   are not of type ``SymbolSearchAction``? Is there a functionality to
   fall back on a default action or should it strictly require a
   ``SymbolSearchAction``?
-  Is there a way to customize the number of top matches
   (``TOP_K_MATCHES``) that the class considers for a partial match?
