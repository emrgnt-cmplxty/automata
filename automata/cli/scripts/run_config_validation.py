import glob
import logging
import logging.config
import os

import yaml
from jsonschema import ValidationError, validate

from automata.configs.config_enums import ConfigCategory
from automata.core.agent.automata_action_extractor import AutomataActionExtractor
from automata.core.utils import get_logging_config, root_py_path

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

# Define the JSON schema for your YAML configuration files
yaml_schema = {
    "type": "object",
    "properties": {
        "instruction_input_variables": {"type": "array", "items": {"type": "string"}},
        "system_instruction_template": {"type": "string"},
        "template_format": {"type": "string"},
        "description": {"type": "string"},
        "number_of_expected_actions": {"type": "integer"},
    },
    "required": [
        "instruction_input_variables",
        "system_instruction_template",
        "template_format",
        "description",
        "number_of_expected_actions",
    ],
}


# Validation test function
def test_yaml_validation(file_path):
    with open(file_path, "r") as file:
        yaml_data = yaml.safe_load(file)

    try:
        validate(instance=yaml_data, schema=yaml_schema)
        logger.debug(f"Validation test for {file_path} passed.")
    except ValidationError as e:
        raise ValidationError(f"Validation test for {file_path} failed: {e}")


# Compatibility test function
def test_yaml_compatibility(file_path):
    with open(file_path, "r") as file:
        yaml_data = yaml.safe_load(file)

    # Add compatibility test cases based on your specific requirements
    compatibility_tests = [
        {
            "test_name": "Check for required keys",
            "condition": all(
                key in yaml_data
                for key in [
                    "instruction_input_variables",
                    "system_instruction_template",
                    "template_format",
                    "description",
                    "number_of_expected_actions",
                ]
            ),
        },
    ]
    for test in compatibility_tests:
        if not test["condition"]:
            raise ValidationError(
                f"Compatibility test '{test['test_name']}' for {file_path} failed."
            )
        else:
            logger.debug(f"Compatibility test '{test['test_name']}' for {file_path} passed.")


def test_action_extraction(file_path):
    with open(file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    actions = AutomataActionExtractor.extract_actions(yaml_data["system_instruction_template"])
    number_of_expected_actions = yaml_data["number_of_expected_actions"]
    if len(actions) != int(number_of_expected_actions):
        raise ValidationError(f"Action extraction test for {file_path} failed.")

    logger.debug(f"Action extraction test for {file_path} passed.")


if __name__ == "__main__":
    # Find all .yaml files in the specified directory
    yaml_files = glob.glob(
        os.path.join(root_py_path(), "configs", ConfigCategory.AGENT.value, "*.yaml")
    )

    # Run validation and compatibility tests on each YAML file
    for yaml_file in yaml_files:
        logger.debug(f"Processing yaml_file={yaml_file}")
        logger.debug(f"yaml_file={yaml_file}")
        test_yaml_validation(yaml_file)
        test_yaml_compatibility(yaml_file)
        test_action_extraction(yaml_file)
