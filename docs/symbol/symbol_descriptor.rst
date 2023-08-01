-  The ``unparse()`` method of the ``SymbolDescriptor`` class encodes
   unusual or special characters in the symbol string as Unicode
   escapes. This is done to ensure proper conversion of symbols into URI
   strings that can be transmitted and received without errors. However,
   it’s important to handle these characters carefully to avoid possible
   misinterpretation.
-  Future additions to the ``DescriptorProto``, which contains the
   suffixes for the ``SymbolDescriptor``, would largely depend on the
   potential use cases that may arise. The current set of suffixes (such
   as ``METHOD``, ``TYPE``, etc.) covers a broad range of symbols types.
   However, there is a possibility that more specific or different types
   of symbols might be required in future iterations or versions of the
   software.
-  Using unrecognized descriptor suffixes can lead to parsing errors
   when trying to unparse the symbol, and it may raise a ``ValueError``.
   This could cause scripts or programs that use the
   ``SymbolDescriptor`` to stop abruptly or behave unexpectedly. It is
   important to use only recognized and properly defined symbol
   descriptors to prevent such issues.
