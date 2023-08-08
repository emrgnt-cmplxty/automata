Agent Class
===========

Overview
--------

The ``Agent`` is an abstract class for creating autonomous agents. These
agents can perform actions and communicate with other providers. During
instantiation, an agent is initialized with a set of instructions and
can optionally be linked with a database provider.

An ``Agent`` works by advancing through a sequence of tasks. It
implements iterator methods (``__iter__`` and ``__next__``) for this
purpose. Each iteration corresponds to a step of the task that the
``Agent`` has been designed to accomplish. This step could be a
conversation turn, which involves generating a new message from the
‘assistant’ and then parsing the reply from the ‘user’. The ``run``
method can be used to execute these tasks until completion, with the
task being deemed complete when the ``__next__`` method returns
``None``.

It has abstract properties for fetching its responses, associated
conversation, and tools, whose concrete implementation is instantiated
by subclasses. It also has an abstract method for setting a database
provider, essential for managing conversations with the user.

Usage Example:
--------------

The following example shows a basic creation of a subclass of ``Agent``:

.. code:: python

   class SimpleAgent(Agent):
       """Implements the abstract Agent class for a simple specific agent."""

       def __init__(self, instructions: str) -> None:
           super().__init__(instructions)

       def __iter__(self):
           ...

       def __next__(self) -> str:
           ...

       @property
       def conversation(self) -> LLMConversation:
           ...

       @property
       def agent_responses(self) -> List[LLMChatMessage]:
           ...

       @property
       def tools(self) -> Sequence[Tool]:
           ...

       def run(self) -> str:
           ...

This example shows a simple implementation of the ``Agent`` abstract
class. The ``...`` represents sections of code that must be implemented
to define the specific behaviour of the ``SimpleAgent``.

Related Symbols
---------------

-  ``LLMChatMessage``, ``LLMConversation``: Models for handling and
   representing chat messages and conversations.
-  ``Tool``: An abstraction for different types of tools associated with
   the agent.
-  ``LLMConversationDatabaseProvider``: Abstract base class for database
   providers.

Limitations
-----------

The ``Agent`` abstract class doesn’t provide an easy method to modify or
control the flow of execution. It assumes that all tasks are to be
performed in a cyclical manner and that they complete after a specific
number of steps.

Follow-up Questions:
--------------------

-  How to handle more complex workflows that require non-linear
   execution paths?
-  Is it possible to dynamically adjust the maximum number of iterations
   based on the task complexity?
