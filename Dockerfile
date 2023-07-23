# Use official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to the root of the project
WORKDIR /automata

# Copy the current directory contents (root of the project) into the container at /automata
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y gcc g++
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Install Node.js
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Instructions on how to run the Docker container
# These instructions will not be executed during the Docker build
# They are merely here for the user's convenience
# Run these commands in the terminal to build and run the Docker container:
# docker build -t automata .
# docker run -it --name test automata bash