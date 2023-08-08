class DocstringRemover(NodeTransformer): ‘Removes docstrings from a
class or function.’

::

   def visit(self, node: AST) -> Optional[AST]:
       'Visits a node in the AST.'
       if (isinstance(node, (AsyncFunctionDef, ClassDef, FunctionDef, Module)) and isinstance(node.body[0], Expr) and isinstance(node.body[0].value, Str)):
           node.body.pop(0)
       return super().visit(node)
