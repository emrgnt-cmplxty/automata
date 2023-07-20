import json
from typing import List

from automata.config import CONVERSATION_DB_PATH
from automata.llm import (
    FunctionCall,
    LLMChatMessage,
    LLMConversationDatabaseProvider,
    OpenAIChatMessage,
)


# TODO - Remove db_path and go with dependency injection,
# e.g. pass in a database provider instance
class OpenAIAutomataConversationDatabase(LLMConversationDatabaseProvider):
    """A conversation database for an Automata agent."""

    PRIMARY_TABLE_NAME = "interactions"

    def __init__(
        self, session_id: str, db_path: str = CONVERSATION_DB_PATH
    ) -> None:
        self.connect(db_path)
        self.session_id = session_id
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

    @property
    def last_interaction_id(self) -> int:
        result = self.select(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME,
            ["MAX(interaction_id)"],
            {"session_id": self.session_id},
        )
        return result[0][0] or 0

    def save_message(self, message: LLMChatMessage) -> None:
        """Save a message to the database."""
        if not isinstance(message, OpenAIChatMessage):
            raise ValueError("Expected an OpenAIChatMessage instance.")
        """TODO - Think about how to handle function calls, e.g. OpenAIChatMessage, and other chat message providers"""
        if self.session_id is None:
            raise ValueError("The database session_id has not been set.")
        interaction_id = self.last_interaction_id + 1
        interaction = {
            "role": message.role,
            "content": message.content,
            "function_call": str(message.function_call)
            if message.function_call
            else None,
            "session_id": self.session_id,
            "interaction_id": interaction_id,
        }
        self.insert(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME, interaction
        )

    def get_messages(
        self,
    ) -> List[LLMChatMessage]:
        """Get all messages with the original session id."""
        """TODO - Test ordering and etc. around this method."""
        result = self.select(
            OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME,
            ["*"],
            {"session_id": self.session_id},
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
