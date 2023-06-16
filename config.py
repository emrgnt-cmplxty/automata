"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- OPENAI_API_KEY: The API key for the OpenAI API.

Note that the environment variables are loaded from a .env file using the `load_dotenv()` function from the `dotenv` library.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Define environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TASK_DB_PATH = os.getenv("TASK_DB_PATH", "tasks.sqlite3")
CONVERSATION_DB_PATH = os.getenv("CONVERSATION_DB_PATH", "interactions.sqlite3")
