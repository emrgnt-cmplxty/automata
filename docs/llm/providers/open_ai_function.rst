OpenAIFunction
==============

``OpenAIFunction`` is a class that represents a function callable by the
OpenAI agent. It provides methods to convert this function definition
into a dictionary, and to present the function in a format similar to
the way OpenAI handles it internally.

Overview
--------

The ``OpenAIFunction`` class helps define a function with name,
description, properties, and required fields. After defining this
function, you can use the ``to_dict`` method to transform this function
definition into a dictionary. Additionally, the ``prompt_format``
property can be used to obtain the function definition in the format
used by OpenAI internally.

Related Symbols
---------------

The ``OpenAIFunction`` class typically operates independently and does
not explicitly relate to other symbols.

Example
-------

Here’s an example of defining a new function using ``OpenAIFunction``,
converting it to a dictionary and retrieving its prompt format.

.. code:: python

   from automata.llm.providers.openai_llm import OpenAIFunction

   # define a function
   function = OpenAIFunction(
       name="get_current_weather",
       description="Get the current weather in a given location",
       properties={
           "location": {
               "type": "string",
               "description": "The city and state, e.g. San Francisco, CA",
           },
           "unit": {
               "type": "string",
               "description": "Unit of measurement, either 'celsius' or 'fahrenheit'."
           }
       },
       required=["location"],
   )

   # convert it to a dictionary
   function_dict = function.to_dict()

   # retrieve its prompt format
   function_prompt_format = function.prompt_format

Limitations
-----------

A limitation of ``OpenAIFunction`` is that it assumes the OpenAI’s
internal format while returning the function definition in
``prompt_format`` property.

Follow-up Questions:
--------------------

-  What are the possible types for the parameters in the ``properties``
   dictionary while defining a function using ``OpenAIFunction``?
-  How can complex properties be represented using ``OpenAIFunction``?
