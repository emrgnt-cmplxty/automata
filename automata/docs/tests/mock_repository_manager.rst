MockRepositoryManager
=====================

``MockRepositoryManager`` is a mock implementation of the
``RepositoryManager`` class used for testing purposes. It derives from
the ``RepositoryManager`` class and provides empty implementations for
the various methods. This allows for simplified testing of classes and
methods that rely on a ``RepositoryManager`` without needing an actual
working implementation.

Related Symbols
---------------

-  ``automata.core.base.github_manager.RepositoryManager``
-  ``automata.core.base.github_manager.GitHubManager``

Overview
--------

``MockRepositoryManager`` provides empty implementations for the
following methods:

-  ``clone_repository(local_path: str)``
-  ``create_branch(branch_name: str)``
-  ``checkout_branch(repo_local_path: str, branch_name: str)``
-  ``stage_all_changes(repo_local_path: str)``
-  ``commit_and_push_changes(repo_local_path: str, branch_name: str, commit_message: str)``
-  ``create_pull_request(branch_name: str, title: str, body: str)``
-  ``branch_exists(branch_name: str) -> bool``
-  ``fetch_issue(issue_number: int) -> Any``

Example
-------

The following example demonstrates how to use the
``MockRepositoryManager`` in a test case.

.. code:: python

   from automata.tests.conftest import MockRepositoryManager
   from automata.core.agent.task import AutomataTask
   from config.config_enums import AgentConfigName

   # Create a MockRepositoryManager instance
   repo_manager = MockRepositoryManager()

   # Instantiate an AutomataTask using the MockRepositoryManager
   task = AutomataTask(
       repo_manager,
       main_config_name=AgentConfigName.TEST.value,
       generate_deterministic_id=False,
       instructions="This is a test.",
   )

Limitations
-----------

``MockRepositoryManager`` is designed to be used in test cases and not
in actual production code. As a result, providing it as
``RepositoryManager`` in production code will not provide any actual
functionality.

Follow-up Questions:
--------------------

-  Are there any methods in ``MockRepositoryManager`` that need
   additional mock implementations for better testing coverage?
-  Can the ``MockRepositoryManager`` class be further improved to
   provide better support for test cases?
