from enum import Enum


class AgentToolProviders(Enum):
    PY_READER = "py_reader"
    PY_WRITER = "py_writer"
    SYMBOL_SEARCH = "symbol_search"
    CONTEXT_ORACLE = "context_oracle"


class LLMPlatforms(Enum):
    OPENAI = "openai"
