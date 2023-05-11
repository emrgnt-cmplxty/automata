from typing import Dict, Optional

from automata.configs.automata_agent_configs import AutomataInstructionPayload
from automata.core.agent.automata_agent_enums import ActionIndicator, ResultField
from automata.tool_management.tool_management_utils import build_llm_toolkits


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


def create_builder_from_args(*args, **kwargs):
    from automata.core.agent.automata_agent_builder import AutomataAgentBuilder

    if "agent_config" not in kwargs:
        raise ValueError("agent_config must be provided")

    builder = AutomataAgentBuilder.from_config(kwargs["agent_config"]).with_eval_mode(
        kwargs.get("eval_mode", False)
    )

    if "instruction_payload" in kwargs and kwargs["instruction_payload"] != {}:
        builder = builder.with_instruction_payload(kwargs["instruction_payload"])

    if "instructions" in kwargs:
        builder = builder.with_instructions(kwargs["instructions"])

    if "model" in kwargs:
        builder = builder.with_model(kwargs["model"])

    if "session_id" in kwargs:
        builder = builder.with_session_id(kwargs["session_id"])

    if "stream" in kwargs:
        builder = builder.with_stream(kwargs["stream"])

    if "verbose" in kwargs:
        builder = builder.with_verbose(kwargs["verbose"])

    if "with_max_iters" in kwargs:
        builder = builder.with_max_iters(kwargs["with_max_iters"])

    if "llm_toolkits" in kwargs and kwargs["llm_toolkits"] != "":
        llm_toolkits = build_llm_toolkits(kwargs["llm_toolkits"].split(","))
        builder = builder.with_llm_toolkits(llm_toolkits)

    if "with_master" in kwargs:
        builder.with_master(kwargs["with_master"])

    return builder


def format_prompt(format_variables: AutomataInstructionPayload, input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables.__dict__.keys():
        if format_variables.__dict__[arg]:
            input_text = input_text.replace(f"{{{arg}}}", format_variables.__dict__[arg])
    return input_text
