"""Defines all agent-related exceptions."""
from automata.core.base import AutomataError


class AgentMaxIterError(AutomataError):
    """An exception raised when the agent exceeds the maximum number of iterations."""

    pass


class AgentStopIterationError(AutomataError):
    """An exception raised when the agent iteration process terminates."""

    pass


class AgentResultError(AutomataError):
    """An exception raised when the agent fails to produce a result."""

    pass


class AgentGeneralError(AutomataError):
    """An exception raised when there is a general error arises with the agent."""

    pass


class AgentDatabaseError(AutomataError):
    """An exception raised when the agent fails to set the database provider."""

    pass


class OpenAPIError(Exception):
    """An exception raised when there is an error with the OpenAPI specification."""

    pass
