OpenAIAutomataAgentToolkitRegistry
==================================

``OpenAIAutomataAgentToolkitRegistry`` is a singleton class that
registers and manages different types of tool builders within the
toolkit. It provides an interface to register a new toolkit builder,
fetch a list of all registered builder types, and initialize the
registry by importing modules from the builders’ package.

Overview
--------

``OpenAIAutomataAgentToolkitRegistry`` uses a metaclass Singleton to
manage and maintain the lifecycle of tool builders, ensuring there is
only a single instance of registry across the application. The class
uses two static data variables:

-  ``_all_builders``: A set that holds instances of the
   ``OpenAIAgentToolkitBuilder`` class.
-  ``_is_initialized``: A boolean value indicating if the registry is
   initialized.

This class exposes three static methods to manage the registry:

-  ``register_tool_manager(cls)``: Adds a builder class to the
   ``_all_builders`` set.
-  ``get_all_builders()``: Returns a list of all registered builders.
   Initializes the registry if it is not initialized yet.
-  ``initialize()``: Imports modules from the builder package,
   triggering the registration of the builders.

Related Symbols
---------------

This class references the following symbols in its implementation:

-  ``Type[OpenAIAgentToolkitBuilder]``: The expected type of the tool
   builders that are registerable with
   ``OpenAIAutomataAgentToolkitRegistry``.
-  ``automata.experimental.tools.builders``
-  ``automata.tools.builders``

Example
-------

Below is an example of how to use the
``OpenAIAutomataAgentToolkitRegistry``. In this example, a custom
builder class CustomToolkitBuilder is registered and retrieved using the
``OpenAIAutomataAgentToolkitRegistry``.

.. code:: python

   from automata.singletons.toolkit_registry import OpenAIAutomataAgentToolkitRegistry

   class CustomToolkitBuilder:
       pass

   # Register a new Builder
   OpenAIAutomataAgentToolkitRegistry.register_tool_manager(CustomToolkitBuilder)

   # Get all registered Builders
   all_builders = OpenAIAutomataAgentToolkitRegistry.get_all_builders()

   print(all_builders)  # This will print [<class '__main__.CustomToolkitBuilder'>]

Limitations
-----------

There is a limitation to ensure that the tool builders are set up
properly and the correct modules are imported during the initialization
of the ``OpenAIAutomataAgentToolkitRegistry``. If builders are not
imported correctly during initialization, they might not be registered
correctly to the Toolkit Registry.

Further, this class requires all builder classes to be compliant with
the ``OpenAIAgentToolkitBuilder`` type. Tool builders not meeting this
requirement might not be registered correctly.

Follow-up Questions:
--------------------

-  How can we ensure all required module builders are imported correctly
   during the initialization?
-  Can we handle the registration of toolkit builders that are not
   compliant with the ``OpenAIAgentToolkitBuilder`` type? How can we
   validate the classes being registered to the Toolkit Registry?
-  How efficient is the Toolkit Registry when registering and fetching a
   large number of builder instances? Is there any room for performance
   optimizations?
-  It’s unclear what the primary use cases for retrieving all toolkit
   builders are. What scenarios or functions rely on the capability to
   get all registered builders? When should a builder be retrieved
   individually vs. collectively?
