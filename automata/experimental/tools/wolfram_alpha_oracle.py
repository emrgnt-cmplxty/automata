"""
Module to interface with the Wolfram Alpha API.

Provides a set of enumerations for various query parameters and a class to 
handle querying the API and processing responses.
"""

import logging
import logging.config
import os
import random
import time
from enum import Enum
from typing import Optional

import dotenv
import requests

from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())
dotenv.load_dotenv()


class BasicParameters(Enum):
    """An enum for the basic parameters of the Wolfram Alpha API."""

    INPUT = "input"
    APPID = "appid"
    FORMAT = "format"
    OUTPUT = "output"


class PodSelection(Enum):
    """An enum for the pod selection parameters of the Wolfram Alpha API."""

    INCLUDEPODID = "includepodid"
    EXCLUDEPODID = "excludepodid"
    PODTITLE = "podtitle"
    PODINDEX = "podindex"
    SCANNER = "scanner"


class Location(Enum):
    """An enum for the location parameters of the Wolfram Alpha API."""

    IP = "ip"
    LATLONG = "latlong"
    LOCATION = "location"


class Size(Enum):
    """An enum for the size parameters of the Wolfram Alpha API."""

    WIDTH = "width"
    MAXWIDTH = "maxwidth"
    PLOTWIDTH = "plotwidth"
    MAG = "mag"


class TimeoutsAsync(Enum):
    """An enum for the timeouts and async parameters of the Wolfram Alpha API."""

    SCANTIMEOUT = "scantimeout"
    PODTIMEOUT = "podtimeout"
    FORMATTIMEOUT = "formattimeout"
    PARSETIMEOUT = "parsetimeout"
    TOTALTIMEOUT = "totaltimeout"
    ASYNC = "async"


class Misc(Enum):
    """An enum for the miscellaneous parameters of the Wolfram Alpha API."""

    REINTERPRET = "reinterpret"
    TRANSLATION = "translation"
    IGNORECASE = "ignorecase"
    SIG = "sig"
    ASSUMPTION = "assumption"
    PODSTATE = "podstate"
    UNITS = "units"


class ErrorPrefixes(Enum):
    """An enum for the 501 error prefixes of the Wolfram Alpha API."""

    COULD_NOT_UNDERSTAND = "Wolfram|Alpha could not understand:"
    COULD_NOT_GENERATE = "Wolfram|Alpha could not generate a result for:"
    TIMEOUT = "Wolfram|Alpha was not able to generate a response in the allotted time for:"


class WolframAlphaOracle:
    """Interface for querying the Wolfram Alpha API."""

    BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"
    MAX_RETRIES = 3
    BASE_DELAY = 1
    MAX_DELAY = 10

    @classmethod
    def query(cls, input_str: str, **kwargs) -> Optional[str]:
        """Constructs a query and sends it to the Wolfram Alpha API, checking for errors and suggestions."""

        app_id = os.environ.get("WOLFRAM_APP_ID")
        if not app_id:
            raise ValueError("WOLFRAM_APP_ID environment variable is not set.")

        response_text = cls._send_query(input_str, **kwargs)

        while response_text and cls._has_error_prefix(response_text):
            if suggestion := cls._parse_for_suggestion(response_text):
                response_text = cls._send_query(suggestion, **kwargs)
            elif response_text.startswith(ErrorPrefixes.TIMEOUT.value):
                return (
                    response_text
                    + "\n\nSuggestion: Try a more simplified or related query to get an answer."
                )
            else:
                return response_text

        return response_text

    @classmethod
    def _send_query(cls, input_str: str, **kwargs) -> Optional[str]:
        """Sends a query to the Wolfram Alpha API."""
        params = {
            BasicParameters.INPUT.value: input_str,
            BasicParameters.APPID.value: os.environ.get("WOLFRAM_APP_ID"),
        }

        for key, value in kwargs.items():
            params[key] = value.value if isinstance(value, Enum) else value

        retries = 0
        delay = cls.BASE_DELAY

        while retries < cls.MAX_RETRIES:
            try:
                response = requests.get(cls.BASE_URL, params=params)
                response.raise_for_status()
                return response.text
            except requests.HTTPError as e:
                # If the error is 501 and contains our error prefix, return the content
                if response.status_code == 501 and cls._has_error_prefix(
                    response.text
                ):
                    return response.text
                elif retries < cls.MAX_RETRIES - 1:
                    jitter = random.uniform(0, 0.1 * delay)
                    time_to_wait = delay + jitter
                    logger.warning(
                        f"Error occurred: {e}. Retrying in {time_to_wait:.2f} seconds..."
                    )
                    time.sleep(time_to_wait)
                    delay = min(2 * delay, cls.MAX_DELAY)
                    retries += 1
                else:
                    raise
            except (
                requests.ConnectionError,
                requests.Timeout,
                requests.RequestException,
            ) as e:
                if retries < cls.MAX_RETRIES - 1:
                    jitter = random.uniform(0, 0.1 * delay)
                    time_to_wait = delay + jitter
                    logger.warning(
                        f"Error occurred: {e}. Retrying in {time_to_wait:.2f} seconds..."
                    )
                    time.sleep(time_to_wait)
                    delay = min(2 * delay, cls.MAX_DELAY)
                    retries += 1
                else:
                    raise
        return None

    @classmethod
    def _has_error_prefix(cls, response_text: str) -> bool:
        return any(
            response_text.startswith(prefix.value) for prefix in ErrorPrefixes
        )

    @classmethod
    def _parse_for_suggestion(cls, response_text: str) -> Optional[str]:
        """Parse the response for a suggestion."""
        lines = response_text.split("\n")
        for line in lines:
            if line.startswith("Things to try instead:"):
                if suggestions := line.replace(
                    "Things to try instead:", ""
                ).split(","):
                    return suggestions[0].strip()
        return None
