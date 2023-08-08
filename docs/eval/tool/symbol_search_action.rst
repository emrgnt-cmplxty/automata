SymbolSearchAction
==================

Overview
--------

``SymbolSearchAction`` is a concrete class that represents a symbol
search operation in the codebase. It can be initialized with a query
string and an optional list of search results. The class enables
comparison of ``SymbolSearchAction`` instances and uniquely identifies
each instance based on its hash.

This class provides two key methods, ``to_payload()`` and
``from_payload()``. The ``to_payload()`` method generates a serializable
payload from the instance’s query and search results, suitable for
storage or transmission. The ``from_payload()`` method, a class method,
takes such a payload and reconstructs the ``SymbolSearchAction``
instance from it.

Related Symbols
---------------

-  DependencyFactory.create_symbol_search: Creates a ``SymbolSearch``
   instance.
-  SymbolSearchToolkitBuilder.\__init\_\_: Creates an instance of
   ``SymbolSearchToolkitBuilder``.
-  SymbolDocEmbeddingBuilder._generate_search_list: Generates a search
   list.
-  AgentifiedSearchToolkitBuilder.\__init\_\_: Creates an instance of
   ``AgentifiedSearchToolkitBuilder``.
-  SymbolSearch.exact_search: Performs an exact search across the
   indexed codebase.

Usage Example
-------------

The following example illustrates how to create and work with an
instance of SymbolSearchAction.

.. code:: python

   from automata.eval.tool.search_eval import SymbolSearchAction

   # Create a SymbolSearchAction
   sym_search_action = SymbolSearchAction(query="MyQuery")

   # Now, let's simulate a search operation that returned some results
   sym_search_action.search_results = ["result1", "result2"]

   # Create a payload from the SymbolSearchAction
   payload = sym_search_action.to_payload()

   # The payload should look something like {'type': 'SymbolSearchAction', 'query': 'MyQuery', 'search_results': 'result1,result2'}
   print(payload)

   # Now, create a SymbolSearchAction from the payload
   sym_search_action_reconstructed = SymbolSearchAction.from_payload(payload)

   # The original and reconstructed SymbolSearchAction should be equivalent
   assert sym_search_action == sym_search_action_reconstructed

Limitations and Follow-up Questions
-----------------------------------

``SymbolSearchAction`` doesn’t actually perform any search operations -
it is simply a representation of a search action that can be serialised
or deserialised.

This class makes a strong assumption about the payload format,
specifically that ‘query’ and ‘search_results’ are both strings. This
may limit its compatibility with other systems or future extensions.

-  How does this class interact with the rest of the search
   functionality provided in Automata for codebase exploration?
-  Is there a need for more flexible payload schemas?
-  How should this class handle errors in payload conversion?
