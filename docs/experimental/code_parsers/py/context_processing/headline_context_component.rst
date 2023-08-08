class HeadlineContextComponent(BaseContextComponent):

::

   def generate(self, symbol: 'Symbol', ast_object: AST, *args, **kwargs) -> str:
       'Convert a symbol into a headline.'
       return self.process_entry(symbol.dotpath)
