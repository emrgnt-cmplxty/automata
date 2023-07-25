class UnknownToolError(Exception):
    """An exception for when an unknown tools type is provided."""

    ERROR_STRING = "Unknown tools type: %s"

    def __init__(self, tool_kit: str) -> None:
        super().__init__(self.ERROR_STRING % (tool_kit))
