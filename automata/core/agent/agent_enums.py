from enum import Enum

SUPPORTED_CODING_LANGUAGES = ["python"]


class ActionIndicator(Enum):
    """The action indicator for the action line of a tool."""

    ACTION = "- "
    CODE = "```"


class ToolField(Enum):
    """The fields of a tool."""

    INDICATOR = "tool_query"
    NAME = "tool_name"
    ARGS = "tool_args"
    QUERY = "tool_query"
    SPEC_LINES = 3


class AgentField(Enum):
    """The fields of an agent."""

    INDICATOR = "agent_query"
    NAME = "agent_version"
    ARGS = "agent_instruction"
    QUERY = "agent_query"
    SPEC_LINES = 3


class ResultField(Enum):
    """The fields of a result."""

    INDICATOR = "return_result"
    SPEC_LINES = 2
