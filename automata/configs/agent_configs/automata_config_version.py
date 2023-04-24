from enum import Enum


class AutomataConfigVersion(Enum):
    DEFAULT = "default"
    AUTOMATA_MASTER_V1 = "automata_master_v1"
    AUTOMATA_RETRIEVER_V1 = "automata_retriever_v1"
    AUTOMATA_WRITER_V1 = "automata_writer_v1"

    AUTOMATA_MASTER_V2 = "automata_master_v2"
    AUTOMATA_RETRIEVER_V2 = "automata_retriever_v2"
    AUTOMATA_WRITER_V2 = "automata_writer_v2"

    AUTOMATA_MASTER_V3 = "automata_master_v3"

    AUTOMATA_DOCSTRING_MANAGER_V1 = "automata_docstring_manager_v1"
