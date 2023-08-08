class OpenAIIncorrectMessageTypeError(Exception):

::

   def __init__(self, message: Any) -> None:
       super().__init__(f'Expected message to be of type OpenAIChatMessage, but got {type(message)}')
