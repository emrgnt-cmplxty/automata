-  In the Automata framework, task states are updated by the
   AutomataTaskEnvironment class and the updates mainly depend on the
   lifecycle of the task. When a task is created, it’s in a “CREATED”
   state. When it’s currently running, it’s in a “RUNNING” state. After
   it’s finished, it’s in a “COMPLETED” state and so on.

-  Actions in response to a ``TaskStateError`` can vary depending on the
   operation that caused the error and the specific task at hand.
   Generally, it can involve retrying the operation (especially if it
   involves network requests), checking for and fixing any mistakes in
   the code that’s managing the task, contacting a subsystem that may be
   managing the state incorrectly, or changing program flow to not
   attempt the operation until the task is in the correct state. In some
   cases, it might be necessary to log the error for future
   troubleshooting, or to notify the user or system administrator.
