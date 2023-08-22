"""An interface for querying the Wolfram Alpha API."""

import os
import requests
from urllib.parse import quote_plus

class WolframAlphaOracle:
    """An interface for querying the Wolfram Alpha API."""
    
    BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"
    
    @classmethod
    def query(cls, input_str: str) -> str:
        """Performs a query to the Wolfram Alpha API and returns the result."""
        
        app_id = os.environ.get("WOLFRAM_APP_ID", "DEMO")
        encoded_input = quote_plus(input_str)

        url = f"{cls.BASE_URL}?input={encoded_input}&appid={app_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.text

# For demonstration purposes, let's test the WolframAlphaOracle with a sample query
sample_query_result = WolframAlphaOracle.query("10 densest elemental metals")
print(sample_query_result)
