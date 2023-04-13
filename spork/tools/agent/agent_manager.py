import os
from typing import Sequence

from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import load_prompt
from langchain.schema import BaseLanguageModel
from langchain.tools.base import BaseTool

from ..utils import home_path, load_yaml
from .agent_configs.agent_version import AgentVersion
from .task_configs.task import Task


class AgentManager:
    def __init__(
        self,
        planning_tools: Sequence[BaseTool],
        planning_llm: BaseLanguageModel,
        exec_tools: Sequence[BaseTool],
        exec_llm: BaseLanguageModel,
        planning_agent: AgentType = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        execution_agent: AgentType = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        planning_prompt_version: AgentVersion = AgentVersion.PLANNING_V1,
        exec_prompt_version: AgentVersion = AgentVersion.EXECUTION_V1,
    ):
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.plan_agent = initialize_agent(
            planning_tools,
            planning_llm,
            agent=planning_agent,
            verbose=True,
            memory=memory,
        )

        self.exec_tools = exec_tools
        self.exec_agent = initialize_agent(
            exec_tools, exec_llm, agent=execution_agent, verbose=True
        )
        self.planning_prompt_version = planning_prompt_version
        self.exec_prompt_version = exec_prompt_version

    def make_planning_task(self, task=Task.BASIC_PROGRAMMING_V0) -> str:
        """
        Generates a planning task for an agent.

        Args:
        - work_item (Union[Issue, PullRequest]): An object representing the work item to generate a planning task for.
        - exec_tools (List[BaseTool]): A list of tools that the execution agent has access to.
        - github_repo_name (str): The name of the GitHub repository the work item belongs to.

        Returns:
        - task_instructions (str): A string containing the instructions for the planning task.
        """
        if self.planning_prompt_version == AgentVersion.PLANNING_V1:
            file_tree_exec = os.popen(
                'tree . -I "__pycache__*|*.pyc|__init__.py|local_env|*.egg-info"'
            )
            file_tree = file_tree_exec.read()
            path = os.getcwd()
            tools = f" {[(tool.name, tool.description) for tool in self.exec_tools]}.\n"
            task_yaml = load_yaml(self.format_config_path("task_configs", f"{task.value}.yaml"))[
                "task"
            ]
            payload = {
                "file_tree": file_tree,
                "path": path,
                "tools": tools,
                "task": f"Title:{task_yaml['title']}\nBody:{task_yaml['body']}\n",
            }

        prompt = load_prompt(
            self.format_config_path("agent_configs", f"{self.planning_prompt_version.value}.yaml")
        )
        # Replace newline characters with actual newlines
        formatted_prompt = prompt.format(**payload).replace("\\n", "\n")

        print("Returning agent prompt = %s" % (formatted_prompt))
        return formatted_prompt

    @staticmethod
    def format_config_path(config_dir: str, config_path: str) -> str:
        """
        Returns the path to a config file.

        Args:
        - config_dir (str): The name of the directory the config file is in.
        - config_path (str): The name of the config file.

        Returns:
        - The path to the config file.
        """
        return os.path.join(
            home_path(),
            "spork",
            "tools",
            "agent",
            config_dir,
            config_path,
        )

        # def load_prompt_config(self) -> Dict:
        #     config_file = os.path.join("prompt_config", self.version.value)
        #     with open(config_path.get(), "r") as f:
        #         config: Config = jsoncomment.JsonComment().load(f)

        # def get_prompt_text(self, **kwargs) -> str:
        #     prompt_text = self.prompt_config["prompt_text"]
        #     # Inject the required local variables into the prompt text
        #     return prompt_text.format(**kwargs)
