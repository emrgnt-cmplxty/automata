from typing import Dict, Optional

from automata.configs.automata_agent_configs import AutomataInstructionPayload

from .automata_agent_enums import ActionIndicator, ResultField


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


def create_instruction_payload(overview: str, agents_message: str) -> AutomataInstructionPayload:
    """
    Create an initial payload for the MasterAutomataAgent based on the provided overview and agents_message.

    Args:
        overview (str): The overview text for the instruction payload.
        agents_message (str): The agents' message for the instruction payload.

    Returns:
        Dict[str, str]: A dictionary containing the created instruction payload.
    """
    instruction_payload = AutomataInstructionPayload()

    if overview != "":
        instruction_payload.overview = overview

    if agents_message != "":
        instruction_payload.agents = agents_message

    return instruction_payload


def format_prompt(format_variables: AutomataInstructionPayload, input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables.__dict__.keys():
        input_text = input_text.replace(f"{{{arg}}}", format_variables.__dict__[arg])
    return input_text
