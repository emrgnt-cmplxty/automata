from automata.core.base import AutomataError


class TaskGeneralError(AutomataError):
    """An exception raised when a general error occurs during task execution."""

    pass


class TaskStateError(AutomataError):
    """An exception raised when the task is not in the correct state for the operation."""

    pass


class TaskInstructionsError(AutomataError):
    """An exception raised when there is an error with the task instructions."""

    pass
