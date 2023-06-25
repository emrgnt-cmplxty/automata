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

    def close(self):
        """Close the connection to the database."""
        if self.conn:
            self.conn.close()

    def create_table(self, table_name: str, fields: dict):
        fields_str = ", ".join([f"{k} {v}" for k, v in fields.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})")
        self.conn.commit()

    def insert(self, table_name: str, data: dict):
        keys_str = ", ".join(data.keys())
        values_str = ", ".join(["?" for _ in data.values()])
        self.cursor.execute(
            f"INSERT INTO {table_name} ({keys_str}) VALUES ({values_str})", tuple(data.values())
        )
        self.conn.commit()

    def select(self, table_name: str, fields: list, conditions: dict = None):
        fields_str = ", ".join(fields)
        query = f"SELECT {fields_str} FROM {table_name}"
        if conditions:
            conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
            query += f" WHERE {conditions_str}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name: str, data: dict, conditions: dict):
        data_str = ", ".join([f"{k} = ?" for k in data])
        conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"UPDATE {table_name} SET {data_str} WHERE {conditions_str}",
            tuple(list(data.values()) + list(conditions.values())),
        )
        self.conn.commit()

    def delete(self, table_name: str, conditions: dict):
        conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE {conditions_str}", tuple(conditions.values())
        )
        self.conn.commit()
