1. Variables are considered “not found” when the code attempts to access
   them, but they haven’t been defined in the current scope. This
   includes both variables that have not been instantiated and those
   that are out of scope.

2. ``VariableNotFoundError`` is commonly used within the automata
   framework where dynamic execution of user-written or auto-generated
   code takes place. It often occurs in scenarios where the system needs
   to access a variable for a certain operation (either for calculation,
   modification, or returning data), but it does not exist in the
   current context or execution environment.

3. When a ``VariableNotFoundError`` is thrown, error handling strategies
   highly depend on the specific implementation and how these exceptions
   are handled in that context. General approaches include defining a
   fallback or default value for the variable, prompting the user to
   define the variable if possible, or simply logging the error for
   debugging. However, it is usually best to avoid these errors in the
   first place by ensuring that all variables are appropriately
   initialized and made available in the correct context before they are
   used. This could involve systematic code verification and testing
   procedures.
