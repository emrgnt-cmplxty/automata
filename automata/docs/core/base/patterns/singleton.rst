Singleton
=========

Overview
--------

The ``Singleton`` class is a metaclass designed to ensure only one
instance of a class is created. It follows a creational pattern which is
commonly used in situations where a class must control the number of
instances created, e.g. for memory management or ensuring unique
communication points in a system.

The core functionality of this class resides under the ``__call__``
method, which checks if an instance of the class already exists before
creating a new one. If the instance already exists, it returns the
existing instance.

This class is a part of ``automata.core.base.patterns`` and is defined
using abstract base class (``abc``) module of Python’s standard library
for creating abstract base classes.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``, a
   unit test sample module.
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``, a unit test
   sample module with an empty class.
-  ``automata.core.context_providers.symbol_synchronization.SymbolProviderSynchronizationContext``,
   a context provider for symbol synchronization.
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU.__init__``,
   initializer for the ``CsSWU`` class.
-  ``automata.tests.unit.sample_modules.sample.Person``, a sample class
   for unit testing.
-  ``automata.core.symbol.base.ISymbolProvider.__init__``, initializer
   for the ``ISymbolProvider`` Interface.
-  ``automata.tests.unit.sample_modules.sample.OuterClass``, a sample
   outer class with an inner class for unit testing.
-  ``automata.core.symbol.base.Symbol``, core class for creating,
   managing, and manipulating symbols.
-  ``automata.tests.unit.sample_modules.sample.OuterClass.InnerClass``,
   a sample inner class located within an outer class for unit testing.

Example
-------

The following is an example demonstrating how to create a class with
Singleton as metaclass.

.. code:: python

   import abc
   from automata.core.base.patterns.singleton import Singleton

   class MyClass(metaclass=Singleton):
       def __init__(self, name):
           self.name = name

   # Create a new instance
   instance1 = MyClass("MyClass1")
   print(instance1.name)  # Outputs: MyClass1

   # Try to create another instance
   instance2 = MyClass("MyClass2")
   print(instance2.name)  # Outputs: MyClass1

   # Confirm both instances are the same 
   print(instance1 is instance2)  # Outputs: True

Limitations
-----------

The Singleton pattern restricts the instantiation of a class to a single
object. It ensures a class has only one instance and provides a global
point of access to it.

One main drawback is that you can’t create a second instance of your
Singleton class. If your application needs to have multiple instances of
a class, then the Singleton pattern is not suitable. Also, complex tests
can become difficult with Singleton if not handled carefully.

Follow-up Questions:
^^^^^^^^^^^^^^^^^^^^

-  Are there instances when the Singleton pattern might not be desired,
   or possibly harmful?
-  Does Singleton thread safe?
-  How do initializers (``__init__``) behave when used with the
   Singleton pattern?
