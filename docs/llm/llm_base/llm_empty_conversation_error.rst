class LLMEmptyConversationError(Exception): ‘Raised when the
conversation is empty.’

::

   def __init__(self, message: str='The conversation is empty.') -> None:
       super().__init__(message)
