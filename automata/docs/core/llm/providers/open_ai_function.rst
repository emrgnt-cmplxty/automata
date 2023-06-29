OpenAIFunction
==============

``OpenAIFunction`` is a class that represents a function callable by the
OpenAI agent. It is designed to provide an interface for conveniently
defining and interacting with functions that can be called by the agent
in various scenarios. The class allows users to define the name,
description, properties, and requirements of the function, making it
easy to create custom functions for specific use cases.

Overview
--------

``OpenAIFunction`` provides a simple way to define and interact with
functions callable by the OpenAI agent. It has methods such as
``__init__`` and ``to_dict``, which allow users to initialize the
function object with the desired properties and convert it into a
dictionary representation, respectively. This class is closely related
to other OpenAI-related symbols like ``OpenAITool``.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.sample_function``
-  ``automata.tests.unit.sample_modules.sample.f``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.tests.unit.test_py_writer.MockCodeGenerator._check_function_obj``
-  ``automata.core.agent.providers.OpenAIAutomataAgent.functions``
-  ``automata.tests.unit.test_py_writer.test_create_function_source_function``
-  ``automata.core.llm.providers.openai.OpenAIAgent._get_available_functions``
-  ``automata.tests.unit.test_py_writer_tool.test_bootstrap_module_with_new_function``
-  ``automata.core.llm.providers.openai.OpenAITool.__init__``
-  ``automata.tests.unit.test_py_writer_tool.test_extend_module_with_new_function``

Usage Example
-------------

.. code:: python

   from automata.core.llm.providers.openai import OpenAIFunction

   function_name = "sample_function"
   function_description = "A sample function that returns a greeting."
   function_properties = {"name": {"type": "string", "description": "Name of the person to greet."}}
   function_required = ["name"]

   sample_function = OpenAIFunction(
       name=function_name,
       description=function_description,
       properties=function_properties,
       required=function_required,
   )

   function_dict = sample_function.to_dict()

Limitations
-----------

``OpenAIFunction`` relies on the correct definition of the callable
functions and their properties. Incorrect definitions or missing
properties may lead to unexpected behavior during execution. This class
also assumes that the agent can access and call the defined functions,
which might not always be the case.

Follow-up Questions:
--------------------

-  How can error checking be improved for the properties and
   requirements of the function?
-  Are there any alternatives for defining callable functions for the
   OpenAI agent?
