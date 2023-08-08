class ITaskExecution(ABC): ‘Interface for task execution behaviors.’

::

   @abstractmethod
   def execute(self, task: Task) -> Any:
       pass
