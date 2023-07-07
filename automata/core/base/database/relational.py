import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List

from automata.config import CONVERSATION_DB_PATH


class RelationalDatabase(ABC):
    """Abstract base class for different types of relational databases."""

    @abstractmethod
    def connect(self, db_path: str):
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def close(self):
        """Close the connection to the database."""
        pass

    @abstractmethod
    def create_table(self, table_name: str, fields: Dict):
        """Create a new table."""
        pass

    @abstractmethod
    def insert(self, table_name: str, data: dict):
        """Insert data into a table."""
        pass

    @abstractmethod
    def select(self, table_name: str, fields: List, conditions: Dict):
        """Select data from a table."""
        pass

    @abstractmethod
    def update_entry(self, table_name: str, data: Dict, conditions: Dict):
        """Update data in a table."""
        pass

    @abstractmethod
    def delete(self, table_name: str, conditions: Dict):
        """Delete data from a table."""
        pass


class SQLDatabase(RelationalDatabase):
    """Concrete class to provide a SQL database."""

    def connect(self, db_path: str = CONVERSATION_DB_PATH) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self, table_name: str, fields: Dict):
        fields_str = ", ".join([f"{k} {v}" for k, v in fields.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})")
        self.conn.commit()

    def insert(self, table_name: str, data: Dict):
        keys_str = ", ".join(data.keys())
        values_str = ", ".join(["?" for _ in data.values()])
        self.cursor.execute(
            f"INSERT INTO {table_name} ({keys_str}) VALUES ({values_str})", tuple(data.values())
        )
        self.conn.commit()

    def select(self, table_name: str, fields: List, conditions: Dict = {}):
        fields_str = ", ".join(fields)
        query = f"SELECT {fields_str} FROM {table_name}"
        if conditions:
            conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
            query += f" WHERE {conditions_str}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_entry(self, table_name: str, data: Dict, conditions: Dict = {}):
        data_str = ", ".join([f"{k} = ?" for k in data])
        conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"UPDATE {table_name} SET {data_str} WHERE {conditions_str}",
            tuple(list(data.values()) + list(conditions.values())),
        )
        self.conn.commit()

    def delete(self, table_name: str, conditions: Dict = {}):
        conditions_str = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE {conditions_str}", tuple(conditions.values())
        )
        self.conn.commit()
