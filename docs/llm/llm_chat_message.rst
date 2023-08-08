class LLMChatMessage(BaseModel): ‘Base class for different types of LLM
chat messages.’ role: str content: Optional[str] = None

::

   def to_dict(self) -> Dict[(str, Any)]:
       return {'role': self.role, 'content': self.content}
