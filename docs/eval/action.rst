class Action(ABC): ‘An arbitrary action to be taken by an LLM, like an
OpenAI function call’

::

   @abstractmethod
   def __init__(self) -> None:
       pass

   @abstractmethod
   def to_payload(self) -> Payload:
       'Converts the Action to a dictionary.'
       pass

   @staticmethod
   @abstractmethod
   def from_payload(dct: Payload) -> 'Action':
       'Creates an Action from a dictionary.'
       pass
