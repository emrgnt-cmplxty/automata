import json
from typing import List

from automata.config import CONVERSATION_DB_PATH
from automata.llm import (
    FunctionCall,
    LLMChatMessage,
    LLMConversationDatabaseProvider,
    OpenAIChatMessage,
)


# TODO - Should the database be a function of session_id in constructor?
class OpenAIAutomataConversationDatabase(LLMConversationDatabaseProvider):
    """A conversation database for an Automata agent."""

    PRIMARY_TABLE_NAME = "interactions"

    def __init__(self, db_path: str = CONVERSATION_DB_PATH) -> None:
        self.connect(db_path)
        self.create_table(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME,
            {
                "session_id": "TEXT",
                "interaction_id": "INTEGER",
                "role": "TEXT",
                "content": "TEXT",
                "function_call": "TEXT",
            },
        )

    @staticmethod
    def _check_session_id(session_id: str) -> bool:
        """Checks if the session ID is valid."""

        return isinstance(session_id, str)

    def save_message(self, session_id: str, message: LLMChatMessage) -> None:
        """Save a message to the database."""

        if not OpenAIAutomataConversationDatabase._check_session_id(
            session_id
        ):
            raise ValueError("The session_id must be a string.")

        if not isinstance(message, OpenAIChatMessage):
            raise ValueError("Expected an OpenAIChatMessage instance.")
        """TODO - Think about how to handle function calls, e.g. OpenAIChatMessage, and other chat message providers"""
        if session_id is None:
            raise ValueError("The database session_id has not been set.")
        interaction_id = self._get_last_interaction_id(session_id) + 1
        interaction = {
            "role": message.role,
            "content": message.content,
            "function_call": str(message.function_call)
            if message.function_call
            else None,
            "session_id": session_id,
            "interaction_id": interaction_id,
        }
        self.insert(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME, interaction
        )

    def _get_last_interaction_id(self, session_id: str) -> int:
        """Get the last interaction ID for a session."""

        result = self.select(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME,
            ["MAX(interaction_id)"],
            {"session_id": session_id},
        )
        return result[0][0] or 0

    def get_messages(
        self,
        session_id: str,
    ) -> List[LLMChatMessage]:
        """Get all messages with the original session id."""

        if not OpenAIAutomataConversationDatabase._check_session_id(
            session_id
        ):
            raise ValueError("The session_id must be a string.")

        """TODO - Test ordering and etc. around this method."""
        result = self.select(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME,
            ["*"],
            {"session_id": session_id},
        )

        # Sort the results by interaction_id, which is the second element of each row
        sorted_result = sorted(result, key=lambda row: row[1])

        # Convert the sorted results to a list of LLMChatMessage instances
        return [
            OpenAIChatMessage(
                role=row[2],
                content=row[3],
                function_call=FunctionCall(**json.loads(row[4]))
                if row[4] is not None
                else None,
            )
            for row in sorted_result
        ]
