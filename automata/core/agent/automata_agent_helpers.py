from typing import Dict, Optional

from .automata_agent_utils import ActionIndicator, ResultField


def generate_user_observation_message(observations: Dict[str, str], include_prefix=True) -> str:
    """Generate a message for the user based on the observations."""
    message = ""
    if include_prefix:
        message += f"{ActionIndicator.ACTION.value} observations\n"
    for observation_name in observations.keys():
        message = append_observation_message(observation_name, observations, message)
    return message


def append_observation_message(observation_name: str, observations: Dict[str, str], message: str):
    new_message = ""
    new_message += f"    {ActionIndicator.ACTION.value}{observation_name}" + "\n"
    new_message += f"      {ActionIndicator.ACTION.value}{observations[observation_name]}" + "\n"
    return message + new_message


def retrieve_completion_message(processed_inputs: Dict[str, str]) -> Optional[str]:
    """Check if the result is a return result indicator."""
    for processed_input in processed_inputs.keys():
        if ResultField.INDICATOR.value in processed_input:
            return processed_inputs[processed_input]
    return None


def create_instruction_payload(overview: str, agents_message: str) -> Dict[str, str]:
    """Create initial payload for the master agent."""
    instruction_payload: Dict[str, str] = {}

    if overview != "":
        instruction_payload["overview"] = overview

    if agents_message != "":
        instruction_payload["agents"] = agents_message

    return instruction_payload
