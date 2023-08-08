class ToolExecution(IToolExecution): ‘Class for executing tools.’

::

   def __init__(self, tools: Sequence[Tool]) -> None:
       self.tools = {tool.name: tool for tool in tools}

   def execute(self, function_call: 'FunctionCall') -> str:
       if (tool := self.tools.get(function_call.name)):
           return tool.run(function_call.arguments)
       else:
           raise Exception(f'No tool found for function call: {function_call.name}')
