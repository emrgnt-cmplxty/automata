-  Could there be more specific subclasses of ``EvalLoadingError``? For
   example, could there be a ``EvalFileNotFoundError``,
   ``EvalInvalidFormatError``, or ``EvalEmptyError`` to differentiate
   between different types of loading issues?
-  Are there ways to handle ``EvalLoadingError`` in the code itself,
   perhaps by attempting to reload the evaluation or proceeding with a
   backup evaluation if the primary one fails to load?
-  Where should the logs for ``EvalLoadingError`` be stored? Are they
   recorded in a consistent way that allows for easy debugging later on?
