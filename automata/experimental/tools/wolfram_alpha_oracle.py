"""
Module to interface with the Wolfram Alpha API.

Provides a set of enumerations for various query parameters and a class to 
handle querying the API and processing responses.
"""

import os
import requests
from enum import Enum

# Define the enums for the parameters

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

class WolframAlphaOracle:
    """Interface for querying the Wolfram Alpha API."""
    BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"
    
    @classmethod
    def query(cls, input_str: str, **kwargs) -> str:
        """Sends a query to the Wolfram Alpha API."""

        # Check if app_id is available
        app_id = os.environ.get("WOLFRAM_APP_ID")
        if not app_id:
            raise ValueError("WOLFRAM_APP_ID environment variable is not set.")

        params = {
            BasicParameters.INPUT.value: input_str,
            BasicParameters.APPID.value: app_id
        }
        
        for key, value in kwargs.items():
            params[key] = value.value if isinstance(value, Enum) else value
        
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.text
        except requests.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Wolfram Alpha API: {e}") from e
        except requests.Timeout as e:
            raise TimeoutError(f"Request to Wolfram Alpha API timed out: {e}") from e
        except requests.RequestException as e:
            raise RuntimeError(f"An error occurred while querying the Wolfram Alpha API: {e}") from e

    
# For demonstration purposes
sample_query_result = WolframAlphaOracle.query(
    "Temperature of liquid nitrogen", 
    format=BasicParameters.FORMAT,
)
print(sample_query_result)