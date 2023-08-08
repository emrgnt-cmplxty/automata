OpenAIChatMessage
=================

``OpenAIChatMessage`` is a class that acts as a representation for a
processed message that is sent TO or FROM the OpenAI LLM Chat API.

Overview
--------

``OpenAIChatMessage`` inherits from the superclass ``LLMChatMessage``.
It is initialized with the role, content, and optionally a function
call. It provides methods to represent the message as a string, convert
it to a dictionary and create a chat message from a completion result.

Related Symbols
---------------

-  ``automata.singletons.github_client.GitHubClient.remove_label``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.entry_to_key``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.add``
-  ``automata.cli.scripts.run_doc_embedding.parse_dotpaths``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.batch_add``
-  ``automata.core.utils.is_sorted``

Usage Example
-------------

.. code:: python

   from automata.llm.providers.openai_llm import OpenAIChatMessage, OpenAIChatCompletionResult

   # Create a completion result
   completion_result = OpenAIChatCompletionResult(role="system", content="Hello, I'm an AI.")

   # Create a chat message from a completion result
   message = OpenAIChatMessage.from_completion_result(completion_result)

   # Convert the message to a string
   print(str(message))  # Outputs: "OpenAIChatMessage(role=system, content=Hello, I'm an AI., function_call=None)"

   # Convert the message to a dictionary
   print(message.to_dict())  # Outputs: {'role': 'system', 'content': "Hello, I'm an AI."}

Limitations
-----------

The methods within ``OpenAIChatMessage`` are all directly related to the
OpenAI LLM Chat API and do not have wider applications outside of their
specific context. The class is designed to specifically interact with
the OpenAI LLM Chat API, so it cannot be used as a general-purpose chat
message manipulator.

Follow-up Questions
-------------------

-  Can this class be modified to support more general use, outside of
   the OpenAI LLM Chat API?
-  How can we extend the functionality to incorporate more features of
   the Chat API, like message logs or instructions?
