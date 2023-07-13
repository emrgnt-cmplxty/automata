-  As the ``RepositoryClient`` defines an abstract base class, the
   methods do not have an implementation and instead serves as a base
   for other derived classes. If we are dealing with Git service APIs
   that return data structures different from what the abstract methods
   in ``RepositoryClient`` specify, it’s the responsibility of the
   derived class to handle it properly. When implementing the abstract
   methods, the derived class should process the data returned by the
   API and format it to match the requirements.

-  It is possible to implement some default behavior in the
   ``RepositoryClient``. However, the purpose of using an abstract base
   class is to define a common interface for its subclasses. Adding
   default behavior in the base class might not make sense in all usage
   scenarios and can add unnecessary complexity. If there are common
   operations that are shared across all the subclasses, it might be
   beneficial to define a utility module or class where all these common
   functionalities can be placed. Alternatively, we can have a base
   class that implements these common methods and have other classes
   inherit from this base class.
