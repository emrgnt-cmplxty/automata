

The improved-spork project is an AI software engineering assistant that helps developers contribute clean, high-quality code to GitHub repositories. It provides the following functionality:

- Automatically log into GitHub using an API key
- List repositories and issues
- Utilize an AI agent along with various tools (Python REPL, Terminal, and others) to close issues while adhering to the user's instructions
# Getting Started

To run the code, follow these steps:

1. Clone the repository on your local machine.
2. Navigate to the project directory.
3. Create and activate a virtual environment by running `python3 -m venv local_env && source local_env/bin/activate`
4. Upgrade to the latest pip by running `python3 -m pip install --upgrade pip`
5. Install the project in editable mode by running `pip3 install -e .`
6. Install pre-commit hooks by running `pre-commit install`
7. Execute the main script by running `python -m spork.main`
