ConfigCategory
==============

Overview
--------

``ConfigCategory`` is an enumeration class in the
``automata.config.base`` module of the Automata applications. These are
used to represent different categories of configuration options in the
context of the application. Current categories include ``AGENT``,
``PROMPT``, ``SYMBOL``, and ``INSTRUCTION``. The string values
correspond to the names of configuration folders in the
``automata/configs`` directory.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.core.agent.agent.AgentInstance.Config``
-  ``automata.tests.unit.test_task_environment.TestURL``
-  ``automata.core.agent.instances.OpenAIAutomataAgentInstance.Config``
-  ``automata.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata.core.tools.base.Tool.Config``
-  ``automata.config.base.AgentConfig.Config``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU.__init__``

Example
-------

To use a ``ConfigCategory``, import it from ``automata.config.base`` and
you can use one of the predefined categories.

.. code:: python

   from automata.config.base import ConfigCategory

   def access_config(category: ConfigCategory):
       # example function using ConfigCategory enum
       pass

   access_config(ConfigCategory.AGENT)

In this example, the ``access_config`` function is an example function
that uses ``ConfigCategory`` as an argument. The function is then called
with ``ConfigCategory.AGENT``.

Limitations
-----------

One possible limitation for the ``ConfigCategory`` is that adding a new
category requires modification to the enum class. The new category
follows the pattern of having a corresponding folder in
``automata/configs``.

Follow-up Questions:
--------------------

-  What is the best way to handle the addition of a new category to the
   ``ConfigCategory`` enum?
