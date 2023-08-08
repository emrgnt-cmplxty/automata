DocumentOracleOpenAIToolkitBuilder
==================================

``DocumentOracleOpenAIToolkitBuilder`` is an intricate part of the
automata toolkit designed to function as a manager of document oracle
tools in the context of the OpenAI API. This tool builder inherits from
``DocumentOracleToolkitBuilder`` and ``OpenAIAgentToolkitBuilder``. It
is responsible for generating tools related to OpenAI’s document oracle
tasks such as query creation, data retrieval, and data processing.

Overview
--------

The ``DocumentOracleOpenAIToolkitBuilder`` class registers itself within
the toolkit registry and defines its associated methods. Specifically,
the ``build_for_open_ai`` method builds the tools for the OpenAI API
context. These tools are packaged with properties like ‘query’, which
receives a string representing the query to search for in the document.
The ‘query’ property is mandatory for each tool.

Related Symbols
---------------

-  ``automata.singletons.github_client.RepositoryClient.create_pull_request``
-  ``automata.symbol.symbol_utils.load_data_path``
-  ``automata.singletons.github_client.RepositoryClient.create_branch``
-  ``automata.llm.providers.openai_llm.OpenAIFunction.to_dict``
-  ``automata.llm.llm_base.LLMConversationDatabaseProvider.update``
-  ``automata.llm.llm_base.LLMConversationDatabaseProvider.save_message``
-  ``automata.singletons.github_client.GitHubClient.clone_repository``
-  ``automata.tasks.task_base.Task.notify_observer``
-  ``automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler.flush``
-  ``automata.symbol.symbol_base.Symbol.module_path``

Usage Example
-------------

.. code:: python

   from automata.experimental.tools.builders.document_oracle_builder import DocumentOracleOpenAIToolkitBuilder
   from automata.llm.providers.lml_provider import LLMProvider 

   doc_oracle_builder = DocumentOracleOpenAIToolkitBuilder()

   # print the name of the toolkit associated with the builder
   print(doc_oracle_builder.TOOL_NAME)

   # print the lml provider used by the builder
   print(doc_oracle_builder.LLM_PROVIDER)

   # Build tools for an OpenAI Document Oracle
   tools = doc_oracle_builder.build_for_open_ai()

   # print the properties and requirements of each tool
   for tool in tools:
       print(tool.properties)
       print(tool.required)

Limitations
-----------

The ``DocumentOracleOpenAIToolkitBuilder`` is currently limited by the
predefined properties and methods it inherits from
``DocumentOracleToolkitBuilder`` and ``OpenAIAgentToolkitBuilder``.
Customizations or extensions might be limited or require significant
alterations to the component’s base classes.

Follow-up Questions:
--------------------

-  How can we extend ``DocumentOracleOpenAIToolkitBuilder`` to
   accommodate a broader range of OpenAI’s document oracle tasks?
-  Is there a way to customize or extend the properties of the tools
   created by ``DocumentOracleOpenAIToolkitBuilder``?
-  How does ``DocumentOracleOpenAIToolkitBuilder`` interact with
   OpenAI’s document oracle in real-time applications?
