ConfigCategory
==============

``ConfigCategory`` is an enumeration class that corresponds to the name
of a folder holding config files in a structured configuration setup.
It’s used within configuration management to facilitate the organization
and retrieval of configuration files.

Overview
--------

``ConfigCategory`` consists of two enum elements:

-  ``PROMPT``: Represents a prompt category.
-  ``SYMBOL``: Represents a symbol category.

These categories can be used within a larger configuration management
system to specify the location and structure of different configurations
for easy retrieval and organization.

Related Symbols
---------------

-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata_docs.cli.commands.cli``
-  ``automata_docs.core.context.py_context.retriever_slim.PyContext``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.Symbol``

Example
-------

The following example demonstrates how to use the ``ConfigCategory``
enum for specifying a configuration category.

.. code:: python

   from automata_docs.config.config_enums import ConfigCategory

   selected_category = ConfigCategory.PROMPT
   print(selected_category)  # Output: ConfigCategory.PROMPT

Limitations
-----------

``ConfigCategory`` is limited to the current enumeration values and
requires modifying the class to add new categories if needed. The
current enum options ``PROMPT`` and ``SYMBOL`` may not suit all
configurations needs for different applications.

Follow-up Questions:
--------------------

-  How can the ``ConfigCategory`` class be extended to support custom
   configuration categories easily?
-  Are there plans to implement more predefined categories to the
   ``ConfigCategory`` enum to cover more potential use cases?
