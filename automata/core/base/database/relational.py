import sqlite3
from abc import ABC, abstractmethod
from automata.config import CONVERSATION_DB_PATH


class RelationalDatabase(ABC):
    """Abstract base class for different types of relational databases."""

    @abstractmethod
    def connect(self, db_path: str):
        """
        Establish a connection to the database.

        Args:
            db_path (str): The name or path of the database to connect to.
        """
        pass

    @abstractmethod
    def close(self):
        """Close the connection to the database."""
        pass

    @abstractmethod
    def create_table(self, table_name: str, fields: dict):
        """
        Create a new table.

        Args:
            table_name (str): Name of the table.
            fields (dict): Dictionary where the key is the field name and the value is the data type.
        """
        pass

    @abstractmethod
    def insert(self, table_name: str, data: dict):
        """
        Insert data into a table.

        Args:
            table_name (str): Name of the table.
            data (dict): Dictionary where the key is the field name and the value is the data value.
        """
        pass

    @abstractmethod
    def select(self, table_name: str, fields: list, conditions: dict = None):
        """
        Select data from a table.

        Args:
            table_name (str): Name of the table.
            fields (list): List of fields to retrieve.
            conditions (dict, optional): Dictionary where the key is the field name and the value is the condition value.
        """
        pass

    @abstractmethod
    def update(self, table_name: str, data: dict, conditions: dict):
        """
        Update data in a table.

        Args:
            table_name (str): Name of the table.
            data (dict): Dictionary where the key is the field name and the value is the new data value.
            conditions (dict): Dictionary where the key is the field name and the value is the condition value.
        """
        pass

    @abstractmethod
    def delete(self, table_name: str, conditions: dict):
        """
        Delete data from a table.

        Args:
            table_name (str): Name of the table.
            conditions (dict): Dictionary where the key is the field name and the value is the condition value.
        """
        pass


class SQLDatabase(RelationalDatabase):
    """Concrete class to provide a SQL database."""

    def connect(self, db_path: str = CONVERSATION_DB_PATH) -> None:
        """
        Establish a connection to the database.
        Args:
            db_path (str, optional): The name or path of the database to connect to. Defaults to CONVERSATION_DB_PATH.
            session_id (str): The session ID of the conversation.
        """

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def set_session_id(self, session_id: str) -> None:
        """Set the session ID of the conversation."""
        self.session_id = session_id

    @abstractmethod
    def close(self):
        """Close the connection to the database."""
        if self.conn:
            self.conn.close()


# from typing import List

# from automata.config import CONVERSATION_DB_PATH
# from automata.core.base.llm.openai import OpenAIChatMessage


# class AutomataAgentDatabase:
#     def __init__(self, session_id: str, db_path: str = CONVERSATION_DB_PATH) -> None:
#         self.session_id = session_id
#         self.conn = sqlite3.connect(db_path)
#         self.cursor = self.conn.cursor()
#         self._init_database()

#     def __del__(self) -> None:
#         """Close the connection to the agent."""
#         if self.conn:
#             self.conn.close()

#     def put_message(self, role: str, content: str, interaction_id: int) -> OpenAIChatMessage:
#         """
#         Inserts the message into the appropriate session and interaction id
#         Args:
#             role (str The role of the message sender (e.g., "user" or "assistant").
#             content (str The content of the message.

#         Returns:
#             OpenAIChatMessage: The saved interaction.
#         """
#         assert self.session_id is not None, "Session ID is not set."
#         assert self.conn is not None, "Database connection is not set."
#         interaction = OpenAIChatMessage(role=role, content=content)
#         self.cursor.execute(
#             "INSERT OR REPLACE INTO interactions (session_id, interaction_id, role, content) VALUES (?, ?, ?, ?)",
#             (self.session_id, interaction_id, role, content),
#         )
#         self.conn.commit()

#         return interaction
