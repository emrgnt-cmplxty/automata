OpenAIFunction
==============

``OpenAIFunction`` represents a callable function in the OpenAI agent.
It encapsulates required information related to a function such as its
name, description, properties, and optional parameters.

Detailed Description
--------------------

The ``OpenAIFunction`` class encapsulates the necessary details needed
to define a function that can be used by the OpenAI agent. The
information includes the name, description, properties, and a list of
required properties for the function. The class also provides the
``to_dict`` method to get the information about the function in a
dictionary format.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.sample_function``: An
   example of a function that can be represented by ``OpenAIFunction``.
-  ``automata.agent.providers.OpenAIAutomataAgent.functions``: A
   method that returns a list of ``OpenAIFunction`` instances
   representing the available functions for the agent.
-  ``automata.llm.providers.openai.OpenAITool``: A class
   representing a tool that can be used by the OpenAI agent which
   utilizes ``OpenAIFunction``.

Usage Example
-------------

The following is an example demonstrating how to create an instance of
``OpenAIFunction`` and get its data in dictionary format using
``to_dict`` method:

.. code:: python

   from automata.llm.providers.openai import OpenAIFunction

   # Initialize OpenAIFunction object
   function = OpenAIFunction(
       name="Sample Function",
       description="This is a sample function",
       properties={"Parameter 1": {"description": "Description for parameter 1"}},
       required=["Parameter 1"]
   )

   # Get function information in a dictionary format
   function_info = function.to_dict()
   print(function_info)  

In the above example, we first import the ``OpenAIFunction`` class. We
then create an instance of ``OpenAIFunction`` named ``function``,
providing its necessary details such as the name, description,
properties, and the list of required properties. Finally, we get the
information about ``function`` in the form of a dictionary using the
``to_dict`` method, and print this information.

Limitations
-----------

The main limitation of ``OpenAIFunction`` is that it strictly assumes
the defined function resides in the OpenAI agent. Externally defined
functions cannot be passed directly, and need to be encapsulated in
``OpenAIFunction`` for the agent to use them.

Next, note that the ``properties`` argument in
``OpenAIFunction.__init__()`` expects a dictionary where each key-value
pair defines a parameter. We can probably make this more specific to
provide better context about the parameters.

Follow-up Questions:
--------------------

-  Can we include an example demonstrating how to define a function that
   can be utilized by ``OpenAIFunction``?
-  What are the specific attributes that should be included in the
   ``properties`` argument when defining an ``OpenAIFunction`` instance?
