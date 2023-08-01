Currently, how the exceptions are handled depends largely on the code
execution flow of the project. The best practices for handling these
exceptions, including ``VariableNotFoundError``, would involve
encapsulating the code block where an error could potentially occur in a
``try``/``catch`` block and dealing with exceptions as they arise.

To provide more detailed error information, for instance, specifying the
variable that was not found, the ``VariableNotFoundError`` could
potentially have a ``message`` property that contains information about
the variable. This would allow developers to write more detailed and
helpful error messages. For example:

.. code:: python

   from automata.eval.code_writing_eval import VariableNotFoundError

   try:
       # Hypothetically, "code_execution_function" is a function where the code execution takes place.
       code_execution_function()
   except VariableNotFoundError as error:
       print(f"Variable '{error.variable_name}' not found. Please check.")

   # Prints out: "Variable 'example_variable' not found. Please check."

In this case, the ``VariableNotFoundError`` would need to be defined
with an additional ``variable_name`` property:

.. code:: python

   class VariableNotFoundError(AutomataError):
       def __init__(self, variable_name):
           self.variable_name = variable_name
           super().__init__(f"Variable '{self.variable_name}' not found.")

However, this kind of modification would need to be considered carefully
based on the overall design of the Automata system and its exception
handling strategy.
