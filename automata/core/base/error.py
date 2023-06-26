class AgentExcetion(Exception):
    """Base class for Agent Exceptions in this module."""

    pass


class MaxIterError(AgentExcetion):
    """An exception raised when the agent exceeds the maximum number of iterations."""

    pass
