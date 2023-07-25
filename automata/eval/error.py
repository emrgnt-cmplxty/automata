from automata.core.base import AutomataError


class EvalLoadingError(AutomataError):
    """Exception raised when there's an issue with loading evaluations."""

    pass


class EvalExecutionError(AutomataError):
    """Raised when there's an issue during task execution."""

    pass
