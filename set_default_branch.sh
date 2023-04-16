#!/bin/sh
current_branch=$(git rev-parse --abbrev-ref HEAD)
sed -i '' "s/^DEFAULT_BRANCH_NAME=.*/DEFAULT_BRANCH_NAME=$current_branch/" .env
