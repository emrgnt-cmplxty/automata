-  Implementation/s of ``Eval`` suitable for ``EvaluationHarness`` would
   typically be those that can take a task and can evaluate it against a
   set of expected outputs. For instance, one might imagine an
   implementation that can understand Natural Language Processing tasks
   and actions.

-  Similarly, suitable implementations of ``AutomataTaskExecutor`` would
   be those that can execute the provided tasks. For instance, in the
   context of a chatbot, an ``AutomataTaskExecutor`` might take an input
   sentence and return a response based on a set chatbot model.

-  Tasks and expected actions should typically be formatted to match the
   expected inputs and outputs of the ``Eval`` and
   ``AutomataTaskExecutor`` instances used. For example, if the ``Eval``
   instance is expecting linguistically formatted tasks and actions
   (like sentences or phrases), then tasks and actions should ideally be
   formatted in this way. Exact formats can vary significantly based on
   the specific implementations used.
