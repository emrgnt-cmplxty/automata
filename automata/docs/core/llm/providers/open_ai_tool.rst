OpenAITool
==========

``OpenAITool`` is a class that allows you to create custom tools that
interact with the OpenAI API. This is particularly useful when you want
your OpenAI-based agent to perform tasks using specific functionalities
provided by these tools. The ``OpenAITool`` class inherits from the
``Tool`` class and incorporates the ``OpenAIFunction`` class to specify
the function callable by the OpenAI agent.

Overview
--------

``OpenAITool`` takes in a ``function``, ``name``, ``description``, and
``properties`` during instantiation. The ``function`` is the main
callable that the tool needs to execute. The ``name``, ``description``,
and ``properties`` are used to describe the tool and its functions.

The main method provided by the ``OpenAITool`` class is the ``run``
method, which takes a ``tool_input`` dictionary as its parameter and
returns the output of the ``function``.

Related Symbols
---------------

-  ``automata.core.base.tool.Tool``
-  ``automata.core.llm.providers.openai.OpenAIFunction``
-  ``automata.core.agent.tool.builder.context_oracle.ContextOracleOpenAIToolkit``
-  ``automata.core.agent.tool.builder.py_writer.PyWriterOpenAIToolkit``

Example
-------

The following is an example demonstrating how to create an instance of
``OpenAITool``.

.. code:: python

   from automata.core.base.tool import OpenAITool

   def example_function(tool_input):
       return f"Example tool response: {tool_input['input_text']}"

   example_tool = OpenAITool(
       function=example_function,
       name="ExampleTool",
       description="An example tool for demonstration purposes",
       properties={
           "input_text": {
               "type": "string",
               "description": "The input text for the example tool",
           }
       },
   )

   tool_input = {"input_text": "Hello, World!"}
   response = example_tool.run(tool_input)
   print(response)  # "Example tool response: Hello, World!"

Limitations
-----------

The main limitation of the ``OpenAITool`` class is that it assumes a
specific structure for the ``properties`` parameter, which should be a
dictionary of dictionaries with specific keys. Moreover, the
``function`` parameter should be easily serializable, as it might be
passed to the OpenAI API.

Follow-up Questions:
--------------------

-  How can we extend the functionality of ``OpenAITool`` to handle more
   complex ``properties`` structures?
-  Are there any performance or security concerns when passing the
   ``function`` parameter to the OpenAI API?
