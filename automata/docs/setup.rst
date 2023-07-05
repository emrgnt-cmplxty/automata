Setup
=====

To set up the project, follow the instructions detailed below:

Create Local Environment
------------------------

Create a Python virtual environment and activate it:

.. code-block:: bash

   python3 -m venv local_env
   source local_env/bin/activate

Install the Project
-------------------

Install the project in editable mode:

.. code-block:: bash

   pip3 install -e .

Setup Pre-commit Hooks
----------------------

.. code-block:: bash

   pre-commit install

Configure Environment Variables
-------------------------------

Copy the `.env.example` file to a `.env` file:

.. code-block:: bash

   cp .env.example .env

The `.env` file contains several environment variables which need to be set:

.. code-block:: bash

   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_API_KEY=your_github_api_key
   CONVERSATION_DB_PATH="$PWD/conversation_db.sqlite3"
   TASK_DB_PATH="$PWD/task_db.sqlite3"
   TASKS_OUTPUT_PATH="$PWD/tasks"
   REPOSITORY_NAME="emrgnt-cmplxty/Automata"
   MAX_WORKERS=8

Replace the placeholders with your own values. The `OPENAI_API_KEY` and `GITHUB_API_KEY` should be your personal API keys for OpenAI and GitHub respectively.

Detect Operating System
----------------------

.. code-block:: bash

   if [[ "$OSTYPE" == "darwin"* ]]; then
       # Mac OSX
       # Replace placeholders in .env with actual values using `sed`
   else
       # Linux and others
       # Replace placeholders in .env with actual values using `sed`
   fi

Fetch Submodules
----------------

.. code-block:: bash

   git submodule update --init --recursive

Install and Initialize Git LFS
------------------------------

You must install `git-lfs` if you have not done so already:

For Ubuntu, run the following:

.. code-block:: bash

   sudo apt-get install git-lfs

For Mac, run the following:

.. code-block:: bash

   brew install git-lfs

Then, initialize by running the following:

.. code-block:: bash

   git lfs install
   git lfs pull
