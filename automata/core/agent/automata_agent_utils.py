import logging
from typing import Dict, Optional

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.core.agent.automata_agent_enums import ActionIndicator, ResultField

logger = logging.getLogger(__name__)


class AutomataAgentFactory:
    @staticmethod
    def create_agent(instructions: str, config: Optional[AutomataAgentConfig]):
        from automata.core.agent.automata_agent import AutomataAgent

        agent = AutomataAgent(instructions=instructions, config=config)
        agent.setup()
        return agent


def generate_user_observation_message(observations: Dict[str, str], include_prefix=True) -> str:
    """
    Create a formatted message for the user based on the provided observations.

    Args:
        observations (Dict[str, str]): A dictionary containing observation names and values.
        include_prefix (bool, optional): Whether to include the action indicator prefix. Defaults to True.

    Returns:
        str: A formatted message containing the observations.
    """
    message = ""
    if include_prefix:
        message += f"{ActionIndicator.ACTION.value} observations\n"
    for observation_name in observations.keys():
        message = append_observation_message(observation_name, observations, message)
    return message


def append_observation_message(observation_name: str, observations: Dict[str, str], message: str):
    """
    Append an observation message to an existing message.

    Args:
        observation_name (str): The name of the observation to append.
        observations (Dict[str, str]): A dictionary containing observation names and values.
        message (str): The existing message to append the observation to.

    Returns:
        str: The updated message with the observation appended.
    """
    new_message = ""
    new_message += f"    {ActionIndicator.ACTION.value}{observation_name}" + "\n"
    new_message += f"      {ActionIndicator.ACTION.value}{observations[observation_name]}" + "\n"
    return message + new_message


def retrieve_completion_message(processed_inputs: Dict[str, str]) -> Optional[str]:
    """
    Retrieve a completion message from the processed inputs, if it exists.

    Args:
        processed_inputs (Dict[str, str]): A dictionary containing processed input names and values.

    Returns:
        Optional[str]: The completion message if found, otherwise None.
    """
    for processed_input in processed_inputs.keys():
        if ResultField.INDICATOR.value in processed_input:
            return processed_inputs[processed_input]
    return None
