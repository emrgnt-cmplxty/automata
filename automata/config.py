# I am here
"""Configuration file for the program.

This file defines environment variables that are used by the program to interact with various APIs, as well as constants that are used throughout the program.

Environment variables:
- OPENAI_API_KEY: The API key for the OpenAI API.
- GITHUB_API_KEY: The API key for the GitHub API.
- YOUR_TABLE_NAME: The name of the table to use for storing data.

Note that the environment variables are loaded from a .env file using the `load_dotenv()` function from the `dotenv` library.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Define environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
CONVERSATION_DB_PATH = os.getenv("CONVERSATION_DB_PATH", "interactions.sqlite3")
REPOSITORY_PATH = os.getenv("REPOSITORY_PATH", ".")
REPOSITORY_NAME = os.getenv("REPOSITORY_NAME", "maks-ivanov/automata")
TASK_DB_PATH = os.getenv("TASK_DB_PATH", "tasks.sqlite3")
TASKS_DIR_PATH = os.getenv("TASKS_DIR_PATH", "tasks")
