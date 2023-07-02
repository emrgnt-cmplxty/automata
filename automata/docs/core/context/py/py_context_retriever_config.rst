PyContextRetrieverConfig
========================

``PyContextRetrieverConfig`` is a configuration class for the
``PyContextRetriever``, which retrieves the context of a symbol in a
Python project. It includes several attributes such as ``spacer``,
``max_dependencies_to_process``, ``max_related_symbols_to_process``, and
``max_context``. These attributes can be set during the instantiation of
the class or can be passed as arguments.

Overview
--------

``PyContextRetrieverConfig`` provides the necessary settings for the
``PyContextRetriever`` to limit the context retrieval process and
visualize the output context. With predefined default values, the class
offers an easy way to adjust the configuration of any
``PyContextRetriever`` instance.

Related Symbols
---------------

-  ``automata.core.retrievers.py.context.PyContextRetriever``
-  ``automata.tests.unit.test_py_reader_tool.python_retriever_tool_builder``
-  ``automata.tests.unit.test_py_writer.py_writer``
-  ``automata.core.singletons.dependency_factory.create_py_context_retriever``
-  ``automata.tests.unit.test_py_reader.getter``
-  ``automata.core.code_handling.py.reader.PyReader``
-  ``automata.tests.unit.test_py_reader_tool.test_init``
-  ``automata.tests.unit.test_py_reader_tool.test_tool_execution``
-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance.Config``
-  ``automata.tests.unit.test_py_reader_tool.test_build``

Example
-------

The following example demonstrates how to create an instance of
``PyContextRetrieverConfig`` with custom values for its attributes.

.. code:: python

   from automata.core.retrievers.py.context import PyContextRetrieverConfig

   config = PyContextRetrieverConfig(
       spacer="\t",
       max_dependencies_to_process=20,
       max_related_symbols_to_process=15,
       max_context=8_000,
   )

Limitations
-----------

The primary limitation of ``PyContextRetrieverConfig`` is that it only
focuses on configuring the context retrieval process and doesn’t support
other aspects of the retrieval process like custom symbol matching or
filtering. Additionally, its default values might not be suitable for
all use cases, and users may need to experiment with different settings
to achieve the desired context retrieval output.

Follow-up Questions:
--------------------

-  What are the use cases where the default values of
   ``PyContextRetrieverConfig`` might not be suitable?
-  Are there any plans to include other configuration options in
   ``PyContextRetrieverConfig`` to support additional features?
