ConfigCategory
==============

``ConfigCategory`` is an enumeration class that corresponds to the name
of a folder holding config files in a Python project. It contains two
variables: ``PROMPT`` and ``SYMBOL``.

Overview
--------

``ConfigCategory`` is a simple enumeration class that helps define the
type of configuration being dealt with in the ``config.config_enums``
module. The two available options are ``PROMPT`` and ``SYMBOL``, where
``PROMPT`` represents configurations related to prompts in the project,
while ``SYMBOL`` represents configurations related to symbols.

Related Symbols
---------------

-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata_docs.tests.unit.sample_modules.sample.EmptyClass``

Example
-------

.. code:: python

   from automata_docs.config.config_enums import ConfigCategory

   config_type = ConfigCategory.PROMPT

Limitations
-----------

``ConfigCategory`` is limited to just two configuration types,
``PROMPT`` and ``SYMBOL``. If additional configuration categories are
needed in the future, they must be added to the enumeration class.

Follow-up Questions:
--------------------

-  Are there any other common configuration categories that should be
   included in this enumeration module?
