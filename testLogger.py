import logging
import logging.config

from automata.core.utils import get_logging_config

logger_1 = logging.getLogger(__name__)
logger_1.setLevel(
    logging.INFO
)  # <--- We can attempt to set the level here, but we haven't set a handler yet

print("Testing configuration without setting the logging configuration:")
logger_1.setLevel(logging.DEBUG)
logger_1.debug("debug message")
logger_1.info("info message")

logger_1.setLevel(logging.INFO)
logger_1.debug("debug message")
logger_1.info("info message")


logger_2 = logging.getLogger(__name__)
logging.config.dictConfig(
    get_logging_config()
)  # <--- This line was in run_agent_config_validation.py and a few others

print("Testing configuration while setting the logging configuration")
logger_2.setLevel(logging.DEBUG)
logger_2.debug("debug message")
logger_2.info("info message")

logger_2.setLevel(logging.INFO)
logger_2.debug("debug message")
logger_2.info("info message")


logger_3 = logging.getLogger(__name__)
logger_3.setLevel(
    logging.INFO
)  # <--- We havent set a handler yet, but since we did above, it will carry the context to this logger!

print("Testing configuration while setting the logging configuration")
logger_3.setLevel(logging.DEBUG)
logger_3.debug("debug message")
logger_3.info("info message")

logger_3.setLevel(logging.INFO)
logger_3.debug("debug message")
logger_3.info("info message")
