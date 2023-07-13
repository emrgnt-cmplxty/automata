-  The default recursion depth in ``PyContextRetriever`` is likely set
   as a constant in the class or module. To override this value, you
   would likely need to modify the source code in the class or module
   itself. However, it’s important to note that increasing the recursion
   depth could lead to longer processing times or potential memory
   issues if the depth is made significantly larger. It’s generally best
   to adjust such values with caution.

-  Currently, ``PyContextRetriever`` is designed specifically for Python
   code. That being said, the overall design of a context retriever
   could potentially be adapted to other languages. This would likely
   involve creating new classes that follow a similar structure but
   implement the specific practices and nuances of the target language.
   For example, a ``JavaContextRetriever`` would need to account for
   Java’s syntax, conventions, and way of managing context. This would
   be a non-trivial amount of work and would likely require intimate
   knowledge of the target language.
