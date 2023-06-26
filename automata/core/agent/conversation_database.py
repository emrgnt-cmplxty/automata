from automata.config import CONVERSATION_DB_PATH
from automata.core.agent.error import AgentDatabaseError
from automata.core.base.database.relational import SQLDatabase


class AutomataAgentConversationDatabase(SQLDatabase):
    def __init__(self, session_id: str, db_path: str = CONVERSATION_DB_PATH) -> None:
        super().__init__()
        self.connect(db_path)
        self.session_id = session_id
        self._init_database()

    def get_last_interaction_id(self) -> int:
        result = self.select(
            "interactions", ["MAX(interaction_id)"], {"session_id": self.session_id}
        )
        return result[0][0] or 0

    def _init_database(self):
        self.create_table(
            "interactions",
            {"session_id": "TEXT", "interaction_id": "INTEGER", "role": "TEXT", "content": "TEXT"},
        )

    def put_message(self, role: str, content: str) -> dict:
        if self.session_id is None:
            raise AgentDatabaseError("The database session_id has not been set.")
        interaction_id = self.get_last_interaction_id() + 1
        interaction = {
            "role": role,
            "content": content,
            "session_id": self.session_id,
            "interaction_id": interaction_id,
        }
        self.insert("interactions", interaction)
        return interaction
