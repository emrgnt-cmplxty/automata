class LLMCompletionResult(BaseModel): ‘Base class for different types of
LLM completion results.’ role: str content: Optional[str] = None

::

   def get_role(self) -> str:
       'Get the role of the completion result.'
       return self.role

   def get_content(self) -> Any:
       'Get the content of the completion result.'
       return self.content
