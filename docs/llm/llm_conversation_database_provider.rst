LLMConversationDatabaseProvider
===============================

Overview
--------

``LLMConversationDatabaseProvider`` is an abstract base class
implemented from Observer, SQLDatabase, and Abstract Base Class (ABC).
Being designed as an interface, this class provides an outline for other
database providers to follow. It is used to manage a database of
conversations in the Look Listen and Model (LLM) framework which
provides interactive communication with users using LLMChatMessage
objects.

The class itself includes multiple methods such as ``update``,
``save_message``, and ``get_messages``. The ``update`` method is a
concrete ``Observer`` method that updates the database whenever the
conversation changes. ``save_message`` and ``get_messages`` are abstract
methods that should be implemented in the child classes for saving a
message to the database and retrieving all messages from database with
the original session id, respectively.

Related Symbols
---------------

-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.update_entry``
-  ``automata.singletons.github_client.RepositoryClient.stage_all_changes``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase._prepare_entry_for_insertion``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase._prepare_entries_for_insertion``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.batch_update``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase._check_duplicate_entry``
-  ``automata.cli.env_operations.update_graph_type``
-  ``automata.symbol.graph.symbol_graph_base.GraphProcessor.process``
-  ``automata.core.utils.get_embedding_data_fpath``
-  ``automata.singletons.github_client.RepositoryClient.branch_exists``

Example
-------

A standard usage example cannot be provided because
``LLMConversationDatabaseProvider`` is an abstract base class and cannot
be directly instantiated. Instead, a concrete class should inherit from
``LLMConversationDatabaseProvider`` and implement its abstract methods.
Here is a general pattern for this:

.. code:: python

   class MyDatabaseProvider(LLMConversationDatabaseProvider):
       def save_message(self, session_id: str, message: LLMChatMessage) -> None:
           # Implement the method as necessary for your class

       def get_messages(self, session_id: str) -> List[LLMChatMessage]:
           # Implement the method as necessary for your class

Limitations
-----------

The primary limitation of this class is that it cannot be used
straightaway due to its abstract nature. It needs to be inherited and
its abstract method need to be overridden for it to be useful. Also, the
class methods mainly handle ``LLMChatMessage`` objects and as such, it
might not be suitable for different types of message objects.

Follow-up Questions
-------------------

-  How can the class handle more different type of message objects (not
   only ``LLMChatMessage``)?
-  Could the updates be made in a more efficient or optimized way?
