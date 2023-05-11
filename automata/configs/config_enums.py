from enum import Enum


class ConfigCategory(Enum):
    AGENT = "agent_configs"
    INSTRUCTION = "instruction_configs"
    EVAL = "eval_configs"


class InstructionConfigVersion(Enum):
    AGENT_INTRODUCTION_DEV = "agent_introduction_dev"
    AGENT_INTRODUCTION_PROD = "agent_introduction_prod"


class AgentConfigVersion(Enum):
    DEFAULT = "default"
    TEST = "test"
    # The initializer is a dummy agent used to spoof the initial message context.
    AUTOMATA_INITIALIZER = "automata_initializer"
    AUTOMATA_INDEXER_DEV = "automata_indexer_dev"
    AUTOMATA_WRITER_DEV = "automata_writer_dev"
    AUTOMATA_MASTER_DEV = "automata_main_dev"
    AUTOMATA_COVERAGE_DEV = "automata_coverage_dev"
    AUTOMATA_INDEXER_PROD = "automata_indexer_prod"
    AUTOMATA_WRITER_PROD = "automata_writer_prod"
    AUTOMATA_MASTER_PROD = "automata_main_prod"
