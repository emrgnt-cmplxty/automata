from typing import Optional, Tuple

import pytest

from automata.core.base.base_tool import BaseCallbackManager, BaseTool, SilentCallbackManager


class MockTool(BaseTool):
    def _run(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "MockTool response"

    async def _arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "MockTool async response"


@pytest.fixture
def mock_tool():
    return MockTool(name="MockTool", description="A mock tool for testing purposes")


def test_silent_callback_manager():
    manager = SilentCallbackManager()

    # Test that all methods return None when called
    assert manager.on_tool_start(None, None) is None
    assert manager.on_tool_error(None) is None
    assert manager.on_tool_end(None) is None

    assert manager.add_handler() is None
    assert manager.on_agent_action() is None
    assert manager.on_agent_finish() is None
    assert manager.on_chain_end() is None
    assert manager.on_chain_error() is None
    assert manager.on_chain_start() is None
    assert manager.on_llm_end() is None
    assert manager.on_llm_error() is None
    assert manager.on_llm_new_token() is None
    assert manager.on_llm_start() is None
    assert manager.on_text() is None
    assert manager.remove_handler() is None
    assert manager.set_handlers() is None


def test_base_tool_instantiation(mock_tool):
    assert mock_tool.name == "MockTool"
    assert mock_tool.description == "A mock tool for testing purposes"
    assert mock_tool.return_direct is False
    assert mock_tool.verbose is False
    assert isinstance(mock_tool.callback_manager, SilentCallbackManager)


def test_base_tool_run(mock_tool):
    tool_input = ("test",)
    response = mock_tool.run(tool_input)
    assert response == "MockTool response"


@pytest.mark.asyncio
async def test_base_tool_arun(mock_tool):
    tool_input = ("test",)
    response = await mock_tool.arun(tool_input)
    assert response == "MockTool async response"


def test_base_tool_set_callback_manager():
    tool = MockTool(
        name="MockTool", description="A mock tool for testing purposes", callback_manager=None
    )
    assert isinstance(tool.callback_manager, BaseCallbackManager)

    manager = SilentCallbackManager()
    tool = MockTool(
        name="MockTool", description="A mock tool for testing purposes", callback_manager=manager
    )
    assert tool.callback_manager is manager


def test_base_tool_call(mock_tool):
    tool_input = ("test",)
    response = mock_tool(tool_input)
    assert response == "MockTool response"
