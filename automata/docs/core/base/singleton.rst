Singleton
=========

``Singleton`` is a metaclass for ensuring only one instance of a class.
This pattern is useful when a class needs to have a single instance
shared across an application or system. Singleton is designed to be used
with other classes by having them inherit from it.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tests.unit.sample_modules.sample.Person``
-  ``automata.tests.unit.sample_modules.sample.OuterClass``
-  ``automata.core.coding.py.module_loader.PyModuleLoader``
-  ``automata.tests.unit.sample_modules.sample.OuterClass.InnerClass``
-  ``automata.core.llm.completion.LLMChatCompletionProvider.__init__``
-  ``automata.tests.conftest.MockRepositoryManager``
-  ``automata.core.base.symbol.Symbol``
-  ``automata.tests.unit.test_py_reader.getter``
-  ``automata.core.coding.py.module_loader.PyModuleLoader.__init__``

Example
-------

The following example demonstrates how to create a Singleton class and
ensure that only one instance of the class is created.

.. code:: python

   import abc
   from automata.core.base.singleton import Singleton

   class MyClass(metaclass=Singleton):
       def __init__(self):
           self.value = 42

   instance1 = MyClass()
   instance2 = MyClass()

   assert instance1 is instance2  # Both instances are the same object

Limitations
-----------

The primary limitation of the Singleton pattern is that it can make code
more difficult to test as it introduces global state into the
application. Unit and integration tests can potentially become
influenced by one another, leading to false negatives or positives.
Developers must be careful when using singletons to ensure that they do
not inadvertently introduce difficult-to-debug issues.

Follow-up Questions:
--------------------

-  Are there any alternative patterns to Singleton that could be used in
   specific contexts to avoid the potential problems associated with
   global state?
