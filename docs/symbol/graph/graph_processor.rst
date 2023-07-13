``GraphProcessor`` interacts with classes like ``CallerCalleeProcessor``
and ``ReferenceProcessor`` by being a parent class to them.
``CallerCalleeProcessor`` and ``ReferenceProcessor`` are specific
instances of a ``GraphProcessor`` that implement the ``process`` method
according to the specific processing they need to do on a
``MultiDiGraph``. For example, the ``CallerCalleeProcessor`` might
implement the ``process`` method to process edges representing
caller-callee relationships while the ``ReferenceProcessor`` may process
edges representing reference relationships.

As for the question about the need for the ``process`` function in a
child class, since it’s declared as an abstract method in the
``GraphProcessor`` class, all child classes are obliged to implement
this method. Abstract methods enforce a specific contract or interface
for a class which the subclasses HAVE to follow. This enforces a design
where all graph processors WILL have a ``process`` method, thereby
giving certainty about the existence of a processing interface
irrespective of what specific type of ``GraphProcessor`` it is. However,
the exact nature of the processing done in the ``process`` method would
depend on the respective child class. If a use-case does not need a
process method, it probably should not inherit from ``GraphProcessor``.

Follow-up Questions:
~~~~~~~~~~~~~~~~~~~~

-  Can you provide examples on how ``CallerCalleeProcessor`` and
   ``ReferenceProcessor`` implement the ``process`` method?
-  Is there an operator overloading happening in the base or child class
   to accommodate multiple types of ‘graph processing’?
-  How do you decide on which ``GraphProcessor`` to use and when?
