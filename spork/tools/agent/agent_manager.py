import os
import textwrap
from typing import Sequence

from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseLanguageModel
from langchain.tools.base import BaseTool

from .prompt_configs.prompt_versions import PromptVersion


class AgentManager:
    def __init__(
        self,
        planning_tools: Sequence[BaseTool],
        planning_llm: BaseLanguageModel,
        exec_tools: Sequence[BaseTool],
        exec_llm: BaseLanguageModel,
        planning_agent: AgentType = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        execution_agent: AgentType = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        _planning_prompt_version: PromptVersion = PromptVersion.PLANNING_V1,
        _exec_prompt_version: PromptVersion = PromptVersion.EXECUTION_V1,
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

    def make_planning_task(self) -> str:
        """
        Generates a planning task for an agent.

        Args:
        - work_item (Union[Issue, PullRequest]): An object representing the work item to generate a planning task for.
        - exec_tools (List[BaseTool]): A list of tools that the execution agent has access to.
        - github_repo_name (str): The name of the GitHub repository the work item belongs to.

        Returns:
        - task_instructions (str): A string containing the instructions for the planning task.
        """
        file_tree_command = 'tree . -I "__pycache__*|*.pyc|__init__.py|local_env|*.egg-info"'
        file_tree = os.popen(file_tree_command)

        task = textwrap.dedent(
            """
        PROPOSE and IMPLEMENT a step-by-step solution to the following task: 

        Title: Optimize python_tools 

        Body: The PythonTool kit exposes 4 functions across two unique tool builders, the functions are

        - python-parser-get-raw-code
        - python-parser-get-pyobject-docstring
        - python-writer-modify-code-state
        - python-writer-write-to-disk

        These functions are to be used by an autonomous developer agent, and the tool is meant to be optimized for such a use case. 
        
        Your job is to inspect the code and come up with new essential functions for the agent, and to then implement them.
        """
        )
        return (
            f"You are a GPT-4, an autonomous python engineering system."
            f" You are given a task and your job is to plan and execute a solution to that task."
            f" You are working in {os.getcwd()} on the improved-spork repository."
            f" IMPORTANT - the output of tree . is shown:\n{file_tree.read()}\n"
            f" Your task is to PROPOSE and IMPLEMENT a step-by-step solution to the following task:\n"
            f"{task}"
            f" To accomplish your task you will need to make use of the following tools:\n"
            f" {[(tool.name, tool.description) for tool in self.exec_tools]}.\n"
            f" Begin by using the available tools to inspect the docstrings of"
            f" files you will need to modify to accomplish the task,"
            f" then, write a step-by-step plan for execution."
            f" Finally, execute your plan. REMEMBER, start by inspecting the docstrings and step-by-step reasoning."
            f" Begin the task: \n"
        )

        # def load_prompt_config(self) -> Dict:
        #     config_file = os.path.join("prompt_config", self.version.value)
        #     with open(config_path.get(), "r") as f:
        #         config: Config = jsoncomment.JsonComment().load(f)

        # def get_prompt_text(self, **kwargs) -> str:
        #     prompt_text = self.prompt_config["prompt_text"]
        #     # Inject the required local variables into the prompt text
        #     return prompt_text.format(**kwargs)
