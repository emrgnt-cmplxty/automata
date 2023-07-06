RepositoryClient
================

Overview
--------

``RepositoryClient`` is an abstract class designed for managing
repositories. Its methods provide essential functionalities for working
with repositories, including checking branch existence, branching,
cloning, committing, pushing changes, creating pull requests, fetching
issues, and staging changes. Other classes that extend this abstract
class must implement these methods as per their specific logic.

Related Symbols
---------------

-  ``automata.core.github_management.client.GitHubClient``
-  ``automata.tests.conftest.MockRepositoryClient``

Dependencies
------------

-  ``abc.ABC``
-  ``abc.abstractmethod``
-  ``typing.Any``
-  ``typing.Optional``
-  ``git.Git``
-  ``git.Repo``
-  ``github.Github``
-  ``github.PullRequest.PullRequest``
-  ``github.Issue.Issue``

Usage
-----

Given that ``RepositoryClient`` is an abstract class, it should not be
instantiated directly. Instead, it should be subclassed. For instance,
``MockRepositoryClient`` and ``GitHubClient`` are examples of subclasses
of ``RepositoryClient``.

.. code:: python

   class MockRepositoryClient(RepositoryClient):
       def clone_repository(self, local_path: str):
           pass

   # ...
   # The other methods from the `RepositoryClient` should be implemented here.   

Limitations
-----------

As ``RepositoryClient`` is an abstract class, it can’t be instantiated
on its own. One has to write the implementation for each of the abstract
methods when subclassing it, making it somewhat less convenient to use
if only a subset of the methods are required.

Follow-up Questions:
--------------------

-  Will we need a default implementation for any of these methods in the
   future?
-  Is it possible to provide some default implementations for common
   operations to reduce boilerplate in subclasses?

Context Footnotes
-----------------

1. The ``MockRepositoryClient`` mentioned here is an object specifically
   designed for testing purposes, mimicking the behavior of
   ``RepositoryClient`` without executing the actual underlying logic.
   Therefore, it’s not presented as a fully viable example of a subclass
   per se.

2. Methods like ``checkout_branch`` or ``stash_all_changes`` in
   ``MockRepositoryClient`` are intentionally shown not returning
   anything, this could be modified to suit your specific test case or
   implementation.
