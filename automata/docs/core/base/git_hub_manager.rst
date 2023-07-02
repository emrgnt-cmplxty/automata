GitHubClient
=============

``GitHubClient`` is a utility class that provides an interface for
interacting with GitHub repositories. It includes functions to clone a
repository, create and checkout a branch, stage, commit, and push
changes, and create issues and pull requests.

Overview
--------

``GitHubClient`` makes it easy to interact with GitHub repositories
using a simple and intuitive API. It abstracts the underlying GitHub API
and Git operations into easy-to-understand methods.

Related Symbols
---------------

-  ``automata.tests.conftest.MockRepositoryClient``
-  ``automata.core.base.github_management.client.RepositoryClient``
-  ``automata.core.tasks.environment.AutomataTaskEnvironment``

Example
-------

The following example demonstrates how to use the ``GitHubClient`` to
clone a repository, create a branch, add changes, commit and push
changes, and create a pull request.

.. code:: python

   from automata.core.base.github_management.client import GitHubClient

   access_token = "your-github-access-token"
   remote_name = "your-remote-repo"
   local_path = "your/local/path"

   github_manager = GitHubClient(access_token, remote_name)

   # Clone the repository locally
   github_manager.clone_repository(local_path)

   # Create a new branch
   branch_name = "feature/my-feature"
   github_manager.create_branch(branch_name)

   # Checkout the branch
   github_manager.checkout_branch(local_path, branch_name)

   # Stage and commit changes
   github_manager.stage_all_changes(local_path)
   commit_message = "Add a new feature"
   github_manager.commit_and_push_changes(local_path, branch_name, commit_message)

   # Create a pull request
   title = "Add my feature"
   body = "This pull request adds a new feature."
   pull_request = github_manager.create_pull_request(branch_name, title, body)

Limitations
-----------

The primary limitation of ``GitHubClient`` is its reliance on the
provided access token for authentication. A user must have a valid
access token for interacting with the remote repository.

Follow-up Questions:
--------------------

-  How can we improve the authentication methods for ``GitHubClient``?
