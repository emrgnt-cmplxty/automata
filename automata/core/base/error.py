class AutomataError(Exception):
    """Base class for Automata exceptions."""

    def __init__(self, message=None, details=None):
        super().__init__(message)
        self._message = message
        self.details = details

    @property
    def user_message(self):
        """Returns the underlying `Exception` (base class) message."""
        return self._message or "<empty message>"

    def __str__(self) -> str:
        original_message = self.user_message
        if self.__cause__ is not None:
            return f"{original_message}. Original error: {str(self.__cause__)}"
        return original_message

    def __repr__(self) -> str:
        """Returns a detailed string representation of the error for debugging."""
        return f"{self.__class__.__name__}(message={self.user_message!r}, details={self.details!r})"
