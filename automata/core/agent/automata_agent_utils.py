# automata_agent_utils.py
from enum import Enum
from typing import List

class ActionIndicator(Enum):
    ACTION = "- "
    CODE = "```"

SUPPORTED_CODING_LANGUAGES = ["python"]

class ToolField(Enum):
    INDICATOR = "tool_query"
    NAME = "tool_name"
    ARGS = "tool_args"
    QUERY = "tool_query"
    SPEC_LINES = 3

class AgentField(Enum):
    INDICATOR = "agent_query"
    NAME = "agent_name"
    ARGS = "agent_instruction"
    QUERY = "agent_query"
    SPEC_LINES = 3

class ResultField(Enum):
    INDICATOR = "return_result"
    SPEC_LINES = 2
