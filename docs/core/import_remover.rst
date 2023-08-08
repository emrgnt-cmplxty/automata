class ImportRemover(NodeTransformer): ‘Removes import statements from a
module, class or function.’

::

   def visit(self, node):
       if (isinstance(node, (AsyncFunctionDef, ClassDef, FunctionDef, Module)) and isinstance(node.body[0], (Import, ImportFrom))):
           node.body.pop(0)
       return super().visit(node)
