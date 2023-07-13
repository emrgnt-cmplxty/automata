-  The bounding box of a source code can be calculated by counting the
   number of physical lines from the beginning to the end of an
   ``ASTNode``. This can be done by traversing the syntax tree and
   tracking the start and end positions of each node.

-  In cases like line wrapping, comments, or multiline strings where the
   statement extends across multiple lines, the bounding box will simply
   include all those lines. The definition of ``bounding_box`` is the
   number of physical lines the ``ASTNode`` spans, regardless of whether
   they contain code, comments, or strings.

-  The bounding box approach does not distinguish between parts of a
   multiline statement that are comments and parts that are actual
   execution lines. It considers the ``ASTNode`` as a whole and
   determines how many lines it occupies.

-  The approach does not specifically account for individual formatting
   styles enforced by tools like Black or PEP8 guidelines. However, as
   it is based on the ``ASTNode``, its results would vary based on the
   visual representation of the code.

-  In the case of compound statements like loops and conditionals, each
   statement within the compound statement would have its own
   ``ASTNode`` and by extension its own ``LineItem``. The bounding box
   of the top-level compound statement would encompass all of its child
   statements.
