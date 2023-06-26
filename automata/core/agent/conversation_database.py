import json
from typing import Dict, Optional

from automata.config import CONVERSATION_DB_PATH
from automata.core.agent.error import AgentDatabaseError
from automata.core.base.database.relational import SQLDatabase


class AutomataAgentConversationDatabase(SQLDatabase):
    """Conversation database for an Automata agent."""

    def __init__(self, session_id: str, db_path: str = CONVERSATION_DB_PATH) -> None:
        """
        Args:
            session_id (str): The session id for the database.
            db_path (str, optional): The path to the database. Defaults to CONVERSATION_DB_PATH.
        """
        super().__init__()
        self.connect(db_path)
        self.session_id = session_id
        self.create_table(
            "interactions",
            {
                "session_id": "TEXT",
                "interaction_id": "INTEGER",
                "role": "TEXT",
                "content": "TEXT",
                "function_call": "TEXT",
            },
        )

    def get_last_interaction_id(self) -> int:
        """
        Returns:
            The last interaction id for the current session.
        """
        result = self.select(
            "interactions", ["MAX(interaction_id)"], {"session_id": self.session_id}
        )
        return result[0][0] or 0

    def put_message(self, role: str, content: str, function_call: Optional[Dict] = None) -> None:
        """
        Puts a message into the database.

        Args:
            role (str): The role of the message.
            content (str): The content of the message.
            function_call (Optional[Dict], optional): The function call of the message. Defaults to None.

        """
        if function_call is None:
            function_call = {}
        if self.session_id is None:
            raise AgentDatabaseError("The database session_id has not been set.")
        interaction_id = self.get_last_interaction_id() + 1
        interaction = {
            "role": role,
            "content": content,
            "session_id": self.session_id,
            "interaction_id": interaction_id,
            "function_call": json.dumps(function_call),
        }
        self.insert("interactions", interaction)
