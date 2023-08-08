class LoggingConfig(TypedDict, total=False): ‘A dictionary representing
the logging configuration’ version: int disable_existing_loggers: bool
formatters: dict handlers: dict[(str, Union[(HandlerDict, dict)])] root:
RootDict
