import logging

CLI_OUTPUT_LEVEL = 25
logging.addLevelName(CLI_OUTPUT_LEVEL, "CLI_OUTPUT")


class CustomLogger(logging.Logger):
    """A custom logger which adheres to input specifications."""

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)  # call the base class constructor

    # TODO - Add single-line comment.
    def cli_output(self, message, *args, **kwargs):
        if self.isEnabledFor(CLI_OUTPUT_LEVEL):
            self._log(CLI_OUTPUT_LEVEL, message, args, **kwargs)
