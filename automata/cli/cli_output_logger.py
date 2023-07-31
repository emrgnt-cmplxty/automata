"""A custom logger which adheres to input specifications."""

import logging

CLI_OUTPUT_LEVEL = 25
logging.addLevelName(CLI_OUTPUT_LEVEL, "CLI_OUTPUT")


class CustomLogger(logging.Logger):
    """A custom logger which adheres to input specifications."""

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)  # call the base class constructor

    def cli_output(self, message: str, *args, **kwargs) -> None:
        """Logs a message at the CLI_OUTPUT level."""
        if self.isEnabledFor(CLI_OUTPUT_LEVEL):
            self._log(CLI_OUTPUT_LEVEL, message, args, **kwargs)
