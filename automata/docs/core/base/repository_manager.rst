RepositoryManager
=================

``RepositoryManager`` is an abstract base class that defines interface
methods for managing repositories. It provides a set of abstract methods
such as ``clone_repository``, ``create_branch``, ``checkout_branch``,
``commit_and_push_changes``, and others that are implemented by
subclasses like ``GitHubManager``.

Related Symbols
---------------

-  ``automata.core.base.github_manager.GitHubManager``
-  ``automata.core.agent.task.environment.AutomataTaskEnvironment``
-  ``config.automata_agent_config.AutomataAgentConfig``
-  ``automata.core.agent.agent.AutomataAgent``

Usage Example
-------------

.. code:: python

   from automata.core.base.github_manager import GitHubManager

   access_token = "your_github_access_token"
   remote_name = "your/remote_repository"
   primary_branch = "main"

   github_manager = GitHubManager(access_token, remote_name, primary_branch)

Methods
-------

-  ``branch_exists``: Checks if a branch with a given name exists in the
   repository.
-  ``checkout_branch``: Switches to a given branch in the repository.
-  ``clone_repository``: Clones the remote repository to a specified
   local path.
-  ``commit_and_push_changes``: Commits and pushes changes made to a
   branch in the repository.
-  ``create_branch``: Creates a new branch with a given name in the
   repository.
-  ``create_pull_request``: Creates a pull request from a specified
   branch.
-  ``fetch_issue``: Fetches an issue in the repository by issue number.
-  ``stage_all_changes``: Stages all changes made to the repository.

Limitations
-----------

The primary limitation of ``RepositoryManager`` is that it is an
abstract base class and cannot directly interact with repositories. It
needs to be subclassed, and the abstract methods need to be implemented
for specific repository services like GitHub or GitLab.

Follow-up Questions:
--------------------

-  How are the underlying git and GitHub operations managed with the
   ``RepositoryManager`` abstract methods?
-  Are there other related symbols that need to be included in the
   documentation?
