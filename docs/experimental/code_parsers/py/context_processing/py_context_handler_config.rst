class PyContextHandlerConfig(): ‘The configuration for the
PyContextHandlerConfig’

::

   def __init__(self, top_n_test_matches: int=10, top_n_symbol_rank_matches: int=10, top_n_dependency_matches: int=20) -> None:
       self.top_n_test_matches = top_n_test_matches
       self.top_n_symbol_rank_matches = top_n_symbol_rank_matches
       self.top_n_dependency_matches = top_n_dependency_matches
