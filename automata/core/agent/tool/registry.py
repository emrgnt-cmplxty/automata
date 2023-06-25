# agent_tool_manager_registry.py
class AgentToolManagerRegistry:
    ALL_MANAGERS = []

    @staticmethod
    def register_tool_manager(cls):
        AgentToolManagerRegistry.ALL_MANAGERS.append(cls)
        return cls
