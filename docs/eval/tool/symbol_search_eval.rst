SymbolSearchEval
================

``SymbolSearchEval`` is a class for evaluating an instance of Language
Learning Model’s (LLM’s) symbol searching ability. It forms a part of
‘automata.eval.tool.search_eval’ in the codebase. Instances of this
class are responsible for evaluating the ability of a correctly
configured Automata system to accurately perform symbol-based searches.

Overview
--------

The ``SymbolSearchEval`` class inherits from ``ToolEval`` and implements
the ability to evaluate the effectiveness of symbol search operations.
It performs this evaluation based on an expected action (which must be
an instance of ``SymbolSearchAction``) and an observed action, which
could either be a ``SymbolSearchAction`` instance or a ``None`` value.

This class facilitates the extraction of search actions implicitly from
input actions and transforms them into ``ToolEvalResult`` objects by
comparing expected and observed actions.

Important methods in this class include ``extract_action``, and
``to_tool_result``.

Related Symbols
---------------

-  ``automata.symbol.graph.symbol_navigator.SymbolGraphNavigator._get_symbol_references_in_scope``
-  ``automata.symbol.symbol_base.Symbol.from_string``
-  ``automata.symbol.symbol_utils.get_rankable_symbols``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._symbol_code_similarity_search_processor``
-  ``automata.experimental.search.symbol_search.SymbolSearch.retrieve_source_code_by_symbol``
-  ``automata.symbol.symbol_parser._SymbolParser.accept_identifier``
-  ``automata.symbol.graph.symbol_navigator.process_symbol_bounds``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder.process_query``
-  ``automata.symbol.graph.symbol_graph.SymbolGraph.get_references_to_symbol``
-  ``automata.symbol.symbol_parser.new_local_symbol``

Example
-------

The following is an example demonstrating how to use the
``SymbolSearchEval`` class.

.. code:: python

   from automata.eval.tool.search_eval import SymbolSearchEval
   from automata.common.action import FunctionCall

   # Example FunctionCall and query result
   func_call = FunctionCall(name='symbol-search', arguments={'query': 'symbol_xyz'})
   search_result = "Searching for symbol...\n'xyz': {'rank': 1, 'symbol': 'symbol_xyz'}"
   input_action_tuple = (func_call, search_result)

   # Instantiate SymbolSearchEval
   sybmol_search_eval = SymbolSearchEval()

   # Extract action
   symbol_search_action = sybmol_search_eval.extract_action(input_action_tuple)

   # To tool result
   tool_eval_result = sybmol_search_eval.to_tool_result(expected_action=symbol_search_action, observed_action=None)

This example demonstrates how the ``SymbolSearchEval`` class can be used
to evaluate a symbol search operation. It first sets up a tuple of a
``FunctionCall`` and the expected result of the search. It then
instantiates the ``SymbolSearchEval`` class, and uses this to extract
the expected action from the input tuple, and to evaluate the expected
versus the observed action (in this case, None was used for simplicity).

Limitations
-----------

The ``SymbolSearchEval`` class currently only supports
``symbol-rank-search``, ``symbol-similarity-search``, and
``llm-facilitated-search`` operations. Any other operation will raise a
``ValueError``.

Follow-up Questions:
--------------------

1. How can we extend the class to support other types of search
   operations?
2. Do we have mechanisms in place to handle edge cases and errors during
   the search process?
3. How can we improve the evaluation accuracy or provide comparative
   analysis between different evaluation measures?
4. Are there plans in place for supporting parallel evaluations in
   large-scale systems, and if so, how will potential synchronisation
   issues be handled?
