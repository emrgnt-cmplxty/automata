PyWriterOpenAIToolkitBuilder
============================

``PyWriterOpenAIToolkitBuilder`` is a component of Automata’s toolkit
for building configurations for OpenAI agent tools. It’s primarily
designed to assist in writing or modifying python source files such as
scripts or jupyter notebooks.

Overview
--------

``PyWriterOpenAIToolkitBuilder`` extends from the base
``OpenAIAgentToolkitBuilder``. It provides a method
``build_for_open_ai`` which returns a list of OpenAI tools. These tools
are expected to contain functions, descriptions and properties and are
represented by instances of the ``OpenAITool`` class. The main
characteristic of ``PyWriterOpenAIToolkitBuilder`` is that the tools it
builds are used by the OpenAI agent to modify python files.

Related Symbols
---------------

-  ``automata.agent.providers.OpenAIAgentToolkitBuilder``: The base
   class this builder extends from.
-  ``automata.llm.providers.openai.OpenAITool``: This class
   represents tools that ``PyWriterOpenAIToolkitBuilder`` builds.

Example
-------

Here’s an illustrative example of how to use the
PyWriterOpenAIToolkitBuilder:

.. code:: python

   from automata.code_handling.py.writer import PyWriter
   from automata.tools.builders.py_writer import PyWriterOpenAIToolkitBuilder

   py_writer = PyWriter()
   toolkit_builder = PyWriterOpenAIToolkitBuilder(py_writer)

   openai_tools = toolkit_builder.build_for_open_ai()  # Returns a list of OpenAITool instances

Here, ``openai_tools`` is a list of ``OpenAITool``\ s that can be
utilized in your OpenAI agent.

Limitations
-----------

The ``PyWriterOpenAIToolkitBuilder`` is largely dependent on the
``PyWriter`` tool, which operates on an abstraction layer, meaning the
writer might not be perfect in handling all edge cases of modifying
python code.

Furthermore, the ``PyWriterOpenAIToolkitBuilder`` currently only
requires the ``module_dotpath`` and ``code`` properties to be present in
the tools. These might not be sufficient for complex manipulations of
python code.

Follow-up Questions:
--------------------

-  Is there a way to handle more complex code manipulations that require
   additional properties?
-  Are there any safety measures taken while writing or modifying python
   files to ensure no breaking changes are introduced?
