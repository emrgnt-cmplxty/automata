#!/bin/bash


# Build and embed the L2 docs
poetry run automata run-doc-embedding --embedding-level=2

# Build and embed the L3 docs
# NOTE - This is an experimental feature.
# poetry run automata run-doc-embedding  --embedding-level=3 