# Use official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to the root of the project
WORKDIR /automata

# Install dependencies
RUN apt-get update && apt-get install -y gcc g++ curl git && rm -rf /var/lib/apt/lists/*
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN pip install --no-cache-dir poetry

# Copy the current directory contents (root of the project) into the container at /automata
COPY . .

# Initialize and update submodules
RUN git submodule update --init --recursive

RUN poetry config virtualenvs.create false
RUN poetry install

# Create a script that will be run when the container is started
RUN echo "#!/bin/bash\n\
set -e\n\
poetry run automata configure --GITHUB_API_KEY=\$GITHUB_API_KEY --OPENAI_API_KEY=\$OPENAI_API_KEY\n\
poetry run automata install-indexing --from-docker=TRUE\n\
poetry run automata run-code-embedding\n\
poetry run automata run-doc-embedding --embedding-level=2\n\
exec \"\$@\"" > entrypoint.sh
RUN chmod +x entrypoint.sh

# Set this script as the entrypoint for the Docker container
ENTRYPOINT ["./entrypoint.sh"]
