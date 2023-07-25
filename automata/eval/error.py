class EvalLoadingError(Exception):
    """Raised when there's an issue with loading evaluations from the JSON file."""

    pass


class EvalExecutionError(Exception):
    """Raised when there's an issue during task execution."""

    pass
