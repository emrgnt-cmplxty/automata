-  If new search tools are developed, they would need to be manually
   added as new enumerators to the ``SearchTool`` class. As
   ``SearchTool`` is an enumerator, it doesn’t provide built-in
   functions to dynamically add or remove members. However, the
   developers can extend the functionality as they continue to introduce
   new search tools.

-  If a user tries to specify a search tool that isn’t available, it
   would result in an ``AttributeError``. The Python Enum module will
   raise this error when trying to access an attribute that does not
   exist in the enumeration. Ideally, the application should handle this
   exception to provide a user-friendly error message. It could be
   further enhanced by providing a list of available search tools to the
   user.
