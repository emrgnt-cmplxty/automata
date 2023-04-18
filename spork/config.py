# I am here
"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- OPENAI_API_KEY: The API key for the OpenAI API.
- GITHUB_API_KEY: The API key for the GitHub API.
- DO_RETRY: A boolean value indicating whether to retry failed requests.
- DEFAULT_BRANCH_NAME: The default branch name for the agent to start and finish on.
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
DO_RETRY = bool(os.getenv("DO_RETRY", 1))
DEFAULT_BRANCH_NAME = os.getenv("DEFAULT_BRANCH_NAME", "main")
REPOSITORY_NAME = os.getenv("REPOSITORY_NAME", "maks-ivanov/spork")

# Define constants
PLANNER_AGENT_OUTPUT_STRING = "Planner Agent Output: "
