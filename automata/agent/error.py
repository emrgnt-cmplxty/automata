class AgentMaxIterError(Exception):
    """An exception raised when the agent exceeds the maximum number of iterations."""

    pass


class AgentStopIteration(StopIteration):
    """An exception raised when the agent stops iterating."""

    pass


class AgentResultError(Exception):
    """An exception raised when the agent fails to produce a result."""

    pass


class AgentGeneralError(Exception):
    """An exception raised when there is a general error arises with the agent."""

    pass


class AgentDatabaseError(Exception):
    """An exception raised when the agent fails to set the database provider."""

    pass


class AgentTaskGeneralError(Exception):
    """An exception raised when a general error occurs during task execution."""

    pass


class AgentTaskStateError(Exception):
    """An exception raised when the task is not in the correct state for the operation."""

    pass


class AgentTaskGitError(Exception):
    """An exception raised when the task encounters a git error."""

    pass


class AgentTaskInstructionsError(Exception):
    """An exception raised when there is an error with the task instructions."""

    pass


class UnknownToolError(Exception):
    """An exception for when an unknown tools type is provided."""

    ERROR_STRING = "Unknown tools type: %s"

    def __init__(self, tool_kit: str) -> None:
        super().__init__(self.ERROR_STRING % (tool_kit))
