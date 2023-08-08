class ToolEvalResult(EvalResult): ‘An abstract class to represent the
result of a tool eval.’

::

   def __init__(self, expected_action: Action, observed_action: Optional[Action], *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.expected_action = expected_action
       self.observed_action = observed_action
