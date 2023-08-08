AutomataTaskEnvironment
=======================

``AutomataTaskEnvironment`` is a concrete implementation of the
``Abstract TaskEnvironment`` specifically designed for Automata
providers. The class provides avenue for setting-up, validating,
resetting and tearing down environments for tasks during its execution
within an Automata environment.

Instances of ``AutomataTaskEnvironment`` are associated with a Github
Manager and an ``EnvironmentMode``, and provide features for setting-up
the environment (modeled on a Github repository in the ``GITHUB`` mode),
as well as committing executed tasks to the remote repository.

The ``AutomataTaskEnvironment`` works best with instances of
``AutomataTask`` and raises exceptions when operations involve
invalid/incorrect task instances.

Related Symbols
---------------

-  ``TaskEnvironment``
-  ``GitHubClient``
-  ``EnvironmentMode``
-  ``Task``
-  ``AutomataTask``
-  ``TaskStateError``
-  ``TaskGeneralError``

Usage Example
-------------

In the example below, we create an instance of
``AutomataTaskEnvironment`` using a ``GITHUB`` ``EnvironmentMode`` and
then set up an ``AutomataTask``.

.. code:: python

   from automata.tasks.task_environment import AutomataTaskEnvironment
   from automata.github.client import GitHubClient
   from automata.tasks.task_enum import EnvironmentMode
   from automata.tasks.automata_task import AutomataTask

   github_manager = GitHubClient(token="<your-github-token>", owner="<github-owner>", repository="<repository-name>")
   environment = AutomataTaskEnvironment(github_manager, EnvironmentMode.GITHUB)

   # Assume a valid AutomataTask instance created earlier
   task = AutomataTask(session_id="654321")
   environment.setup(task)

Limitations
-----------

``AutomataTaskEnvironment`` requires valid ``AutomataTask`` instances
and a proper ``GitHubClient`` initialised with the correct Github token,
owner name and repository name for it to function correctly. It also
expects the Github repository to be available and accessible. Commits on
Github could fail if the branch already exists or if there are checkout
or commit failures.

Follow-up Questions:
--------------------

-  How can the ``AutomataTaskEnvironment`` handle recovery/resumption of
   tasks interrupted during execution?
-  Could the class be extended to support other ``EnvironmentMode``
   apart from Github? If yes, how would this affect the existing methods
   and how could they be made more generic?
-  What would be the expected behavior of ``AutomataTaskEnvironment``
   when there are network failures during Github operations?
