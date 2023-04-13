"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- OPENAI_API_KEY: The API key for the OpenAI API.
- GITHUB_API_KEY: The API key for the GitHub API.
- PINECONE_API_KEY: The API key for the Pinecone API.
- PINECONE_ENVIRONMENT: The environment to use for the Pinecone API.
- YOUR_TABLE_NAME: The name of the table to use for storing data.
- OBJECTIVE: The OBJECTIVE of the program.
- DO_RETRY: A boolean value indicating whether to retry failed requests.

Constants:
- PLANNER_AGENT_OUTPUT_STRING: The output string for the planner agent.

Note that the environment variables are loaded from a .env file using the `load_dotenv()` function from the `dotenv` library.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Define environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east1-gcp")
YOUR_TABLE_NAME = os.getenv("TABLE_NAME", "")
OBJECTIVE = os.getenv("OBJECTIVE", "")
DO_RETRY = bool(os.getenv("DO_RETRY", 1))

# Define constants
PLANNER_AGENT_OUTPUT_STRING = "Planner Agent Output: "
