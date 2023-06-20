ToolkitType
===========

``ToolkitType`` is an enumeration that helps identify the type of
toolkit used in certain toolkit wrapper classes. It provides enumeration
values to easily work with various toolkits in a consistent and
efficient manner.

Overview
--------

``ToolkitType`` is used to categorize different types of toolkits used
within the Automata ecosystem. This enumeration is useful in maintaining
a robust system where each toolkit can be identified by its
corresponding ``ToolkitType``. It is primarily used in managing the
mapping of toolkits to their respective types.

Related Symbols
---------------

-  ``automata.core.base.tool.Toolkit``
-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

The following is an example of how to use ``ToolkitType``:

.. code:: python

   from automata.core.base.tool import ToolkitType

   def process_toolkit(toolkit_type: ToolkitType):
       if toolkit_type == ToolkitType.TEXT_PREPROCESSING:
           print("This is a text preprocessing toolkit.")
       elif toolkit_type == ToolkitType.DATA_PROCESSING:
           print("This is a data processing toolkit.")
       else:
           print("Unknown toolkit type.")

   process_toolkit(ToolkitType.TEXT_PREPROCESSING)

Limitations
-----------

``ToolkitType`` is a simple enumeration for categorizing different
toolkit types. The primary limitation is that it is limited to the types
of toolkits defined within this enumeration.

Follow-up Questions:
--------------------

-  Are there any plans to add more enumeration values to ``ToolkitType``
   for further categorization of toolkits?
