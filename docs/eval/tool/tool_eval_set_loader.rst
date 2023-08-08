ToolEvalSetLoader
=================

``ToolEvalSetLoader`` is a class that loads a list of function calls and
their expected actions from a JSON file. This class is mainly used for
loading evaluation tasks for testing the functionality and performance
of tools. It provides developers with an efficient way of loading,
formatting, and accessing the JSON payloads for function calls and the
expected actions associated with them.

Overview
--------

``ToolEvalSetLoader`` constitutes two major parts of operation: loading
JSON payloads and parsing them for instantiating function calls and
expected actions. It implements validation checks to ensure that JSON
files are loaded, and the payloads formed are dictionaries. It also
provides a formatter to apply to all string values in the loaded data
recursively. The class offers validation for the payloads, ensuring the
loaded information is in the correct format for further processing.

In summary, ``ToolEvalSetLoader`` constitutes a fundamental part of the
tool evaluation process by streaming the function calls and expected
actions from a JSON file and validating the payloads.

Related Symbols
---------------

-  ``automata.symbol_embedding.vector_databases.JSONSymbolEmbeddingVectorDatabase.__init__``
-  ``automata.cli.cli_output_logger.CustomLogger.__init__``
-  ``automata.tools.tool_error.UnknownToolError.__init__``
-  ``automata.config.config_base.SerializedDataCategory``
-  ``automata.experimental.code_parsers.py.context_processing.context_utils.get_all_classes``
-  ``automata.singletons.py_module_loader.PyModuleLoader._load_module_from_fpath``
-  ``automata.symbol.graph.symbol_graph.SymbolGraph.__init__``
-  ``automata.singletons.dependency_factory.DependencyFactory.create_py_context_retriever``
-  ``automata.core.ast_handlers.ImportRemover``
-  ``automata.core.utils.set_openai_api_key``

Example
-------

Here is an example demonstrating how to instantiate the
``ToolEvalSetLoader`` and load a JSON file of function calls and
expected actions.

.. code:: python

   from automata.eval.tool.tool_eval_harness import ToolEvalSetLoader

   # Path to the JSON file of function calls and expected actions.
   filepath = "path/to/json/file"

   # Create an instance of ToolEvalSetLoader
   tool_eval_set_loader = ToolEvalSetLoader(filepath)

   # Load the JSON file
   payloads = tool_eval_set_loader.load_json()

The above code will load the JSON file and parse it into
``FunctionCall`` and ``Action`` objects that can be further used in the
evaluation process.

Limitations
-----------

-  ``ToolEvalSetLoader`` can only process JSON files. If any other file
   type is provided, it will raise a ``ValueError``.
-  It assumes that each payload consists of a ‘template’ and ‘entries’.
   If the structure of the payloads in the JSON file varies from this,
   then an error may occur.

Follow-up Questions:
--------------------

-  What is the data structure of ‘template’ and ‘entries’ that are
   expected in each payload?
-  Is there a specific format for the function call and expected action
   dictionaries?
-  What exceptions does the class handle? What happens if an exception
   is raised during the loading or parsing of the JSON file?
-  Could other file types (e.g., YAML, XML) be supported in the future?
