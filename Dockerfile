# Use official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to the root of the project
WORKDIR /automata

# Copy the current directory contents (root of the project) into the container at /automata
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y gcc g++ curl
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Install dependencies and run indexing on the local codebase
RUN automata install-indexing

# Refresh the code embeddings (after making local changes)
RUN poetry run automata run-code-embedding

# Refresh the documentation + embeddings
RUN poetry run automata run-doc-embedding --embedding-level=2

# Instructions on how to run the Docker container
# These instructions will not be executed during the Docker build
# They are merely here for the user's convenience
# Run these commands in the terminal to build and run the Docker container:
# docker run --name automata_container -it --rm -e OPENAI_API_KEY=<your_openai_key> -e GITHUB_API_KEY=<your_github_key> ghcr.io/emrgnt-cmplxty/automata:latest
# docker stop automata_container
# docker rm automata_container (in case you run it with other run command that does not include --rm)
