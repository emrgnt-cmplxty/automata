"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- GITHUB_API_KEY: The API key for the GitHub API.
- OPENAI_API_KEY: The API key for the OpenAI API.
- CONVERSATION_DB_PATH: The abs path to use for storing conversation data.
- TASK_OUTPUT_PATH: The output path for new tasks.
- MAX_WORKERS: The maximum number of workers to run concurrently.

Note that the environment variables are loaded from a .env file using the `load_dotenv()` function from the `dotenv` library.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Define environment variables
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CONVERSATION_DB_PATH = os.getenv("CONVERSATION_DB_PATH", "interactions.sqlite3")
TASK_OUTPUT_PATH = os.getenv("TASK_OUTPUT_PATH", "tasks")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 8))
