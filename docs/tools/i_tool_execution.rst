class IToolExecution(ABC): ‘Interface for executing tools.’

::

   @abstractmethod
   def execute(self, function_call: 'FunctionCall') -> str:
       pass
