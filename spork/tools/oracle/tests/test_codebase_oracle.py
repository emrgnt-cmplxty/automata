import os
import tempfile

import git
import pytest
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory

from spork.tools.oracle.codebase_oracle import CodebaseOracle


# Mock LLM and ReadOnlySharedMemory for testing purposes
class MockLLM(BaseLLM):
    def __call__(self, *args, **kwargs):
        pass

    def _generate(self, *args, **kwargs):
        pass

    def _llm_type(self, *args, **kwargs):
        pass

    def _agenerate(self, *args, **kwargs):
        pass


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

mock_memory = ReadOnlySharedMemory(memory=memory)


# Fixture for creating a temporary git repository
@pytest.fixture
def temp_git_repo():
    with tempfile.TemporaryDirectory() as tempdir:
        repo = git.Repo.init(tempdir)
        with open(os.path.join(tempdir, "test_file.txt"), "w") as f:
            f.write("This is a test file.")
        repo.index.add(["test_file.txt"])
        repo.index.commit("Initial commit")
        yield tempdir


def test_codebase_oracle_initialization(temp_git_repo):
    codebase_oracle = CodebaseOracle(temp_git_repo, MockLLM(), mock_memory)
    assert codebase_oracle is not None


def test_codebase_oracle_is_git_repo(temp_git_repo):
    with pytest.raises(AssertionError):
        CodebaseOracle("not_a_git_repo", MockLLM(), mock_memory)


def test_codebase_oracle_chain_building(temp_git_repo):
    codebase_oracle = CodebaseOracle(temp_git_repo, MockLLM(), mock_memory)
    codebase_oracle._build_chain()
    assert codebase_oracle._chain is not None


# Add more test functions to test other aspects of the CodebaseOracle class
