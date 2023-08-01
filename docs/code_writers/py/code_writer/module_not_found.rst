-  In which specific scenarios is ``ModuleNotFound`` exception typically
   raised?

Discussion:
-----------

``ModuleNotFound`` exception would typically be raised when a module
that was expected to be found in the module dictionary was not located.
This could occur due to misspelling the module name, trying to access a
module that does not exist in the dictionary, or if there was an issue
with module loading or import.

Troubleshooting this error would involve several steps such as:

-  Ensure that the required module is installed properly and can be
   successfully imported in the Python environment.
-  Verify that the module name being searched matches exactly with the
   one in the module dictionary, including letter case.
-  Checking whether the module dictionary has been updated or not after
   the module installation.
-  If the error persists, one would have to trace the stack trace
   provided along with the exception for further details on what went
   wrong.

Mishandling the exceptions can cause unpredictable behavior, therefore
it’s recommended to accurately implement relevant error handling around
code blocks which can potentially raise this exception and provide
meaningful message to handle the exception.
