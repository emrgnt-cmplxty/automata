RepositoryManager
=================

``RepositoryManager`` is an abstract class serving as an interface for
working with remote code repositories, such as Git and GitHub. It
provides a set of abstract methods to perform common actions, such as
checking if a branch exists, checking out a branch, cloning a
repository, committing and pushing changes, creating a branch, and
creating a pull request. You can implement this abstract class to work
with a specific code repository host and APIs.

``RepositoryManager`` includes the following methods:

.. code:: python

   @abstractmethod
   def branch_exists(self, branch_name: str) -> bool:
       pass

   @abstractmethod
   def checkout_branch(self, repo_local_path: str, branch_name: str):
       pass

   @abstractmethod
   def clone_repository(self, local_path: str):
       pass

   @abstractmethod
   def commit_and_push_changes(self, repo_local_path: str, branch_name: str, commit_message: str):
       pass

   @abstractmethod
   def create_branch(self, branch_name: str):
       pass

   @abstractmethod
   def create_pull_request(self, branch_name: str, title: str, body: str):
       pass

   @abstractmethod
   def stage_all_changes(self, repo_local_path: str):
       pass

Related Symbols
---------------

-  ``automata.core.base.github_manager.GitHubManager``
-  ``git.Repo``
-  ``github.Github``
-  ``github.PullRequest.PullRequest``

Example
-------

The following example demonstrates how to implement the
``RepositoryManager`` abstract class to work with a GitHub repository:

.. code:: python

   from automata.core.base.github_manager import RepositoryManager
   from git import Repo
   from github import Github, PullRequest

   class GitHubManager(RepositoryManager):
       def __init__(self, access_token: str, remote_name: str, primary_branch: str = "main"):
           self.access_token = access_token
           self.client = Github(access_token)
           self.remote_name = remote_name
           self.repo = self.client.get_repo(self.remote_name)
           self.primary_branch = primary_branch

       def branch_exists(self, branch_name: str) -> bool:
           # Implement the branch_exists method here

       def checkout_branch(self, repo_local_path: str, branch_name: str):
           # Implement the checkout_branch method here

       def clone_repository(self, local_path: str):
           # Implement the clone_repository method here

       def commit_and_push_changes(self, repo_local_path: str, branch_name: str, commit_message: str):
           # Implement the commit_and_push_changes method here

       def create_branch(self, branch_name: str):
           # Implement the create_branch method here

       def create_pull_request(self, branch_name: str, title: str, body: str):
           # Implement the create_pull_request method here

       def stage_all_changes(self, repo_local_path: str):
           # Implement the stage_all_changes method here

Limitations
-----------

-  The base ``RepositoryManager`` class only provides an interface and
   no actual functionality unless implemented for a specific repository
   host.
-  Each implementation of the ``RepositoryManager`` depends on the
   assumptions and limitations of the specific Git APIs used. For
   example, while using the GitHub API and PyGitHub, the rate limits,
   authentication mechanisms, and availability of endpoints may impact
   the functionality of the implementation.

Follow-up Questions:
--------------------

-  How can we create a unified interface that supports different
   repository hosts (e.g., GitLab, Bitbucket) alongside GitHub without
   making separate classes or implementations for each?
