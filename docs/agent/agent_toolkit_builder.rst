class AgentToolkitBuilder(ABC): ‘:raw-latex:`\n    `AgentToolkitBuilder
is an abstract class for building tools for
providers.:raw-latex:`\n    `Each builder builds the tools associated
with a specific AgentToolkitNames.:raw-latex:`\n    `’ TOOL_NAME:
Optional[AgentToolkitNames] = None LLM_PROVIDER: Optional[LLMProvider] =
None

::

   @abstractmethod
   def build(self) -> List['Tool']:
       'Builds the tools associated with the `AgentToolkitBuilder`.'
       pass
