from typing import List

from automata.config import CONVERSATION_DB_PATH
from automata.core.agent.error import AgentDatabaseError
from automata.core.llm.completion import LLMChatMessage, LLMConversationDatabaseProvider


class AutomataAgentConversationDatabase(LLMConversationDatabaseProvider):
    """Conversation database for an Automata agent."""

    def __init__(self, session_id: str, db_path: str = CONVERSATION_DB_PATH) -> None:
        """
        Args:
            session_id (str): The session id for the database.
            db_path (str, optional): The path to the database. Defaults to CONVERSATION_DB_PATH.
        """
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

    @property
    def last_interaction_id(self) -> int:
        """
        Returns:
            The last interaction id for the current session.
        """
        result = self.select(
            "interactions", ["MAX(interaction_id)"], {"session_id": self.session_id}
        )
        return result[0][0] or 0

    def save_message(
        self, message: LLMChatMessage
    ) -> None:  # role: str, content: str, function_call: Optional[Dict] = None) -> None:
        """
        Puts a message into the database.

        Args:
            role (str): The role of the message.
            content (str): The content of the message.
            function_call (Optional[Dict], optional): The function call of the message. Defaults to None.

        TODO - Think about how to handle function calls, e.g. OpenAIChatMessage, and other chat message providers
        """
        if self.session_id is None:
            raise AgentDatabaseError("The database session_id has not been set.")
        interaction_id = self.last_interaction_id + 1
        interaction = {
            "role": message.role,
            "content": message.content,
            "session_id": self.session_id,
            "interaction_id": interaction_id,
        }
        self.insert("interactions", interaction)

    def get_messages(
        self,
    ) -> List[LLMChatMessage]:
        """
        Get all messages of a specific session.

        Args:
            session_id (str): The ID of the session.

        Returns:
            List of messages for the session. Each message is represented as a dictionary.

        TODO - Test ordering and etc. around this method.
        """
        result = self.select("interactions", ["*"], {"session_id": self.session_id})

        # Sort the results by interaction_id, which is the second element of each row
        sorted_result = sorted(result, key=lambda row: row[1])

        # Convert the sorted results to a list of LLMChatMessage instances
        return [LLMChatMessage(role=row[2], content=row[3]) for row in sorted_result]
