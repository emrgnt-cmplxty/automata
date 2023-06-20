GitHubManager
=============

``GitHubManager`` is a utility class that helps manage GitHub
repositories and perform common GitHub-related tasks such as branch
management, cloning repositories, committing and pushing changes,
creating pull requests, and more. It uses the GitHub Python API to
interact with repositories and execute required operations.

Related Symbols
---------------

-  ``abc.ABC``
-  ``typing.List``
-  ``git.Git``
-  ``git.Repo``
-  ``github.Github``
-  ``github.PullRequest``

Example
-------

The following is an example demonstrating how to create an instance of
``GitHubManager`` and use its basic features.

.. code:: python

   from automata.core.base.github_manager import GitHubManager

   access_token = "your_access_token"
   remote_name = "your_remote_name"
   primary_branch = "main"

   manager = GitHubManager(access_token, remote_name, primary_branch)

   # Check if a branch exists
   branch_name = "feature-branch"
   branch_exists = manager.branch_exists(branch_name)

   # Create a new branch if it doesn't exist
   if not branch_exists:
       manager.create_branch(branch_name)

   # Clone the repository to a local path
   local_path = "/path/to/clone"
   manager.clone_repository(local_path)

   # Checkout the branch
   manager.checkout_branch(local_path, branch_name)

   # Stage all changes, commit, and push
   commit_message = "Update feature-branch"
   manager.stage_all_changes(local_path)
   manager.commit_and_push_changes(local_path, branch_name, commit_message)

   # Create a pull request
   pull_request_title = "Feature branch PR"
   pull_request_body = "This is a pull request for the feature branch."
   pull_request = manager.create_pull_request(branch_name, pull_request_title, pull_request_body)

Limitations
-----------

``GitHubManager`` relies on the ``github`` and ``git`` libraries to
perform its operations. Ensure that these libraries are installed and
properly set up before using ``GitHubManager``. It also assumes that you
have the necessary permissions to execute operations on the specified
repository and requires a valid access token for authentication.

Follow-up Questions:
--------------------

None.
