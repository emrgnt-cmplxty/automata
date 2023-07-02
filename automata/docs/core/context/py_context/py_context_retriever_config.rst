PyContextRetrieverConfig
========================

``PyContextRetrieverConfig`` is a configuration class for
``PyContextRetriever``. It contains various attributes such as
``spacer``, ``max_dependencies_to_process``,
``max_related_symbols_to_process``, ``model_name``, and others to
provide the necessary setup and settings for retrieving context in a
Python project.

Overview
--------

``PyContextRetrieverConfig`` sets up the configuration for the
``PyContextRetriever`` class, which is used to retrieve the context of a
symbol in a Python project. It includes settings for indentation
(spacer), limits on the number of dependencies and related symbols to
process, the model name to use for encoding, and the maximum context
length.

Related Symbols
---------------

-  ``automata.core.context.py_context.retriever.PyContextRetriever``
-  ``automata.core.toolss.tool_utils.DependencyFactory.create_py_context_retriever``
-  ``automata.core.code_handling.py_coding.retriever.PyCodeRetriever``

Example
-------

The following is an example demonstrating how to create an instance of
``PyContextRetrieverConfig`` with custom attributes.

.. code:: python

   from automata.core.context.py_context.retriever import PyContextRetrieverConfig

   config = PyContextRetrieverConfig(
       spacer="    ",
       max_dependencies_to_process=5,
       max_related_symbols_to_process=5,
       model_name="gpt-4",
       max_context=6_500,
   )

Limitations
-----------

``PyContextRetrieverConfig`` assumes default values for all its
attributes. If a user provides new values for the attributes, it may
lead to unintended behavior or compatibility issues with other parts of
the system.

Follow-up Questions:
--------------------

-  What are the consequences of setting the
   ``max_dependencies_to_process`` and
   ``max_related_symbols_to_process`` to a value larger or smaller than
   the default?
