GitHubClient
============

Overview
--------

``GitHubClient`` is a class under the
``automata.singletons.github_client`` package that provides an interface
for interacting with GitHub repositories. Its main function is to manage
operations directly related to the GitHub repository, such as creating
new branches, checking out branches, staging all changes to the
repository, committing changes, pushing changes to the repository,
creating pull requests, and others.

This powerful and flexible client can be used to wrap all interactions
with GitHub, allowing for clean and maintainable code. It accomplishes
its tasks using the ``GitHub API``, alongside libraries ``gitpython``
and ``PyGitHub``.

Related Symbols
---------------

-  ``automata.tests.conftest.MockRepositoryClient``
-  ``automata.tests.conftest.environment``
-  ``automata.tasks.environment.AutomataTaskEnvironment.__init__``
-  ``automata.tests.unit.test_task_environment.test_commit_task``
-  ``automata.tests.conftest.task``
-  ``automata.singletons.github_client.RepositoryClient``
-  ``automata.tests.unit.test_py_reader_tool.test_tool_execution``
-  ``automata.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata.tasks.environment.AutomataTaskEnvironment``
-  ``automata.tests.unit.test_task_environment.TestURL``

Example
-------

Assume you’ve initialized a ``GitHubClient`` instance using your GitHub
``access_token``, the ``remote_name`` of your repository and
``primary_branch`` name:

.. code:: python

   access_token = "<your github access token>"
   remote_name = "<your github remote name>"
   primary_branch = "main"
   github_client = GitHubClient(access_token, remote_name, primary_branch)

One can check if a branch exists in the repository as follows:

.. code:: python

   branch_name = "feature_branch"
   print(github_client.branch_exists(branch_name))

If you need to clone a repository to a local path:

.. code:: python

   local_path = "<destination local path>"
   github_client.clone_repository(local_path)

The methods of the ``GitHubClient`` class can be conveniently combined
to perform complex tasks. For example, you could create a new branch,
checkout that branch, stage all changes, commit and push changes:

.. code:: python

   repo_local_path = "<your local repository path>"
   branch_name = "feature_branch"
   commit_message = "Initial commit"

   # Checking out a new branch and performing some changes
   github_client.create_branch(branch_name)
   github_client.checkout_branch(repo_local_path, branch_name)

   # Stage all changes and commit them
   github_client.stage_all_changes(repo_local_path)
   github_client.commit_and_push_changes(repo_local_path, branch_name, commit_message)

You can even create a pull request:

.. code:: python

   title = "Feature pull request"
   body = "This is a description of the changes introduced by this pull request"
   github_client.create_pull_request(branch_name, title, body)

Limitations
-----------

While ``GitHubClient`` provides a very convenient way to interact with
GitHub repositories, it does not cover all the possible interactions
that GitHub’s REST API v3 offers.

It only provides a limited number of functions and is not meant to be a
complete replacement for the functionality provided by the official
GitHub API.

It also lacks the capability to manage organizations, users, and other
entities beyond repositories.

The ``GitHubClient`` does not provide support for handling rate limits,
pagination, or retries on failure.

Follow-up Questions:
--------------------

-  Can we extend ``GitHubClient`` to provide comprehensive coverage of
   GitHub’s REST API v3?
-  Are there plans to include support for handling rate limits,
   pagination, or retries on failure?
