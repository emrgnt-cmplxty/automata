import sqlite3
from typing import List

from automata.config import CONVERSATION_DB_PATH
from automata.core.base.openai import OpenAIChatMessage


class AutomataConversationDatabase:
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.conn = sqlite3.connect(CONVERSATION_DB_PATH)
        self.cursor = self.conn.cursor()
        self._init_database()

    def __del__(self):
        """Close the connection to the agent."""
        if self.conn:
            self.conn.close()

    def put_message(self, role: str, content: str, interaction_id: int):
        """
        Inserts the message into the appropriate session and interaction id
        Args:
            role (str): The role of the message sender (e.g., "user" or "assistant").
            content (str): The content of the message.

        Returns:
            OpenAIChatMessage: The saved interaction.
        """
        assert self.session_id is not None, "Session ID is not set."
        assert self.conn is not None, "Database connection is not set."
        interaction = OpenAIChatMessage(role=role, content=content)
        self.cursor.execute(
            "INSERT OR REPLACE INTO interactions (session_id, interaction_id, role, content) VALUES (?, ?, ?, ?)",
            (self.session_id, interaction_id, role, content),
        )
        self.conn.commit()

        return interaction

    def get_conversations(self) -> List[OpenAIChatMessage]:
        """Loads previous interactions from the database and populates the messages list."""
        self.cursor.execute(
            "SELECT role, content FROM interactions WHERE session_id = ? ORDER BY interaction_id ASC",
            (self.session_id,),
        )
        return [
            OpenAIChatMessage(role=role, content=content)
            for (role, content) in self.cursor.fetchall()
        ]

    def _init_database(self):
        """Initializes the database connection and creates the interactions table if it does not exist."""
        self.conn = sqlite3.connect(CONVERSATION_DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "\n            CREATE TABLE IF NOT EXISTS interactions (\n                session_id INTEGER,\n                interaction_id INTEGER,\n                role TEXT,\n                content TEXT,\n                PRIMARY KEY (session_id, interaction_id)\n            )\n            "
        )
        self.conn.commit()
