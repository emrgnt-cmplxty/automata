class AgentMaxIterError(Exception):
    """An exception raised when the agent exceeds the maximum number of iterations."""

    pass


class AgentStopIteration(StopIteration):
    """An exception raised when the agent iteration process terminates."""

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
