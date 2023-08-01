"""Encapsulates the functionality of a relational database."""
import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from automata.config import CONVERSATION_DB_PATH


class RelationalDatabase(ABC):
    """Abstract base class for different types of relational databases."""

    @abstractmethod
    def connect(self, db_path: str) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    def create_table(self, table_name: str, fields: Dict) -> None:
        """Create a new table."""
        pass

    @abstractmethod
    def insert(self, table_name: str, data: dict) -> None:
        """Insert data into a table."""
        pass

    @abstractmethod
    def select(self, table_name: str, fields: List, conditions: Dict) -> None:
        """Select data from a table."""
        pass

    @abstractmethod
    def update_entry(
        self, table_name: str, data: Dict, conditions: Dict
    ) -> None:
        """Update data in a table."""
        pass

    @abstractmethod
    def delete(self, table_name: str, conditions: Dict) -> None:
        """Delete data from a table."""
        pass


class SQLDatabase(RelationalDatabase):
    """Concrete class to provide a SQL database."""

    class NullConnection:
        """A null connection to a database."""

        def commit(self) -> Any:
            """Commit a transaction."""
            raise NotImplementedError("This is a null connection.")

    class NullCursor:
        """A null cursor to a database."""

        def execute(self, *args, **kwargs) -> Any:
            """Execute a query."""
            raise NotImplementedError("This is a null cursor.")

        def fetchall(self) -> Any:
            """Fetch all results from a query."""
            raise NotImplementedError("This is a null cursor.")

    def __init__(self):
        self.conn: Union[
            sqlite3.Connection, SQLDatabase.NullConnection
        ] = SQLDatabase.NullConnection()
        self.cursor: Union[
            sqlite3.Cursor, SQLDatabase.NullCursor
        ] = SQLDatabase.NullCursor()

    def connect(self, db_path: str = CONVERSATION_DB_PATH) -> None:
        """Establish a connection to the database."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.db_path = db_path

    def close(self) -> None:
        """Close the connection to the database."""
        if isinstance(self.conn, sqlite3.Connection):
            self.conn.close()
        self.conn = SQLDatabase.NullConnection()
        self.cursor = SQLDatabase.NullCursor()

    def create_table(self, table_name: str, fields: Dict) -> None:
        """Create a new table."""
        if not self.conn or not self.cursor:
            raise ValueError("Valid connection to database required.")

        fields_to_create = ", ".join([f"{k} {v}" for k, v in fields.items()])
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_to_create})"
        )
        self.conn.commit()

    def insert(self, table_name: str, data: Dict) -> None:
        """Insert data into a table."""
        keys = ", ".join(data.keys())
        values = ", ".join(["?" for _ in data.values()])
        self.cursor.execute(
            f"INSERT INTO {table_name} ({keys}) VALUES ({values})",
            tuple(data.values()),
        )
        self.conn.commit()

    def select(
        self, table_name: str, fields: List, conditions: Optional[Dict] = None
    ) -> Any:
        """Select data from a table."""
        if conditions is None:
            conditions = {}
        field_names = ", ".join(fields)
        query = f"SELECT {field_names} FROM {table_name}"
        if conditions:
            conditions_query = " AND ".join([f"{k} = ?" for k in conditions])
            query += f" WHERE {conditions_query}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_entry(
        self, table_name: str, data: Dict, conditions: Optional[Dict] = None
    ) -> None:
        """Update data in a table."""
        if conditions is None:
            conditions = {}

        data_squery = ", ".join([f"{k} = ?" for k in data])
        conditions_query = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"UPDATE {table_name} SET {data_squery} WHERE {conditions_query}",
            tuple(list(data.values()) + list(conditions.values())),
        )
        self.conn.commit()

    def delete(
        self, table_name: str, conditions: Optional[Dict] = None
    ) -> None:
        """Delete data from a table."""
        if conditions is None:
            conditions = {}

        conditions_query = " AND ".join([f"{k} = ?" for k in conditions])
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE {conditions_query}",
            tuple(conditions.values()),
        )
        self.conn.commit()
