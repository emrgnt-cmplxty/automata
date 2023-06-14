PyCodeWriter.ClassOrFunctionNotFound
====================================

``PyCodeWriter.ClassOrFunctionNotFound`` is an exception that is raised
when a class or function is not found in the module. This exception is
primarily used in the ``PyCodeWriter`` class.

Overview
--------

The ``PyCodeWriter.ClassOrFunctionNotFound`` exception is used within
the ``PyCodeWriter`` class to indicate that a requested class or
function could not be located in the module. This might happen, for
instance, when you try to update or retrieve the code or docstring of a
non-existent class or function in the module.

Related Symbols
---------------

-  ``PyCodeWriter``
-  ``PyCodeRetriever``
-  ``MockCodeGenerator``
-  ``PyContextRetriever``
-  ``Symbol``

Example
-------

The following is an example demonstrating how the
``PyCodeWriter.ClassOrFunctionNotFound`` exception might be raised.

.. code:: python

   from automata_docs.core.coding.py_coding.writer import PyCodeWriter
   from automata_docs.core.coding.py_coding.retriever import PyCodeRetriever

   # Create PyCodeWriter instance with a PyCodeRetriever
   retriever = PyCodeRetriever()
   writer = PyCodeWriter(python_retriever=retriever)

   # Assume "sample_module" has only one class: "SampleClass"
   try:
       writer.update_class("sample_module", "NonExistentClass", "def new_method(self): pass")
   except PyCodeWriter.ClassOrFunctionNotFound as e:
       print(f"Exception: {e}")

This code snippet demonstrates how the
``PyCodeWriter.ClassOrFunctionNotFound`` exception is raised when trying
to update a class that does not exist in the module.

Limitations
-----------

The ``PyCodeWriter.ClassOrFunctionNotFound`` exception is specific to
the ``PyCodeWriter`` class and its use-cases, and it cannot be utilized
for other code retrieving or writing scenarios. It depends on the
implementation and handling of the ``PyCodeWriter`` and other related
symbols.

Follow-up Questions:
--------------------

-  Are there other scenarios where this exception might be raised,
   outside the scope of the ``PyCodeWriter`` class?
