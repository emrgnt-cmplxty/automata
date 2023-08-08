class ToolExecutor(): ‘Class for using IToolExecution behavior to
execute a tool.’

::

   def __init__(self, execution: IToolExecution) -> None:
       self.execution = execution

   def execute(self, function_call: 'FunctionCall') -> str:
       return self.execution.execute(function_call)
