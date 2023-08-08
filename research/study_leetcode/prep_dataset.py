"""Prepares the dataset for agent evaluation"""
# sourcery skip: avoid-global-variables
import os

import pandas as pd

from automata.core.utils import get_root_fpath
from automata.llm import OpenAIEmbeddingProvider

# Specify the path to your JSON file
FILE_NAME = "leetcode-solutions.json"
CHUNK_SIZE = 512

# Load the JSON file into a pandas DataFrame
df = pd.read_json(
    os.path.join(get_root_fpath(), "research", "study_leetcode", FILE_NAME)
)

# Extract cleaned explanations by splitting at "```"
cleaned_explanations = [
    ele.split("```")[0] for ele in df["code_with_problem"].values
]

# Initialize the embedding provider
embedding_provider = OpenAIEmbeddingProvider()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


all_embeddings = []
# Loop through the cleaned_explanations in chunks of CHUNK_SIZE
for chunk in chunks(cleaned_explanations, CHUNK_SIZE):
    # Build embedding vectors for each chunk
    chunk_embeddings = embedding_provider.batch_build_embedding_vector(chunk)
    all_embeddings.extend(chunk_embeddings)

# Add the embeddings to the DataFrame as a new column
df["embedding"] = all_embeddings

file_path = "leetcode-solutions-embedded.json"

# # Save the modified DataFrame back to the original JSON file
df.to_json(file_path)
