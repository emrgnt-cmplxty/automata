from typing import List, NamedTuple, cast

from automata.core.agent.automata_actions import Action, AgentAction, ResultAction, ToolAction


class EvalResult(NamedTuple):
    """
    A class to represent the result of an eval.
    """

    token_match: bool
    full_match: bool


class EvalAction:
    """
    A class to represent an action in an eval.
    """

    def __init__(self, action: Action, tokens: List[str] = []):
        """
        Args:
            action: The action that was executed.
            result: The result of executing the action.
        """
        self.action = action
        self.tokens = tokens

    def token_match(self, action_str: str) -> bool:
        """
        Performs a relative comparison between two actions
        """
        for token in self.tokens:
            if token not in action_str:
                return False
        return True

    def full_match(self, extracted_action: Action, expected_action: Action) -> bool:
        """
        Performs an exact comparison between two actions
        """
        return extracted_action == expected_action


# def full_match(extracted_action, expected_action):
#     return extracted_action == expected_action


def calc_eval_result(
    extracted_actions: List[Action], expected_actions: List[EvalAction]
) -> EvalResult:
    all_token_matches = True
    all_full_matches = True

    for extracted_action in extracted_actions:
        has_token_match = False
        has_full_match = False

        for expected_eval_action in expected_actions:
            expected_action = expected_eval_action.action

            # Check if actions are of the same type
            if type(extracted_action) == type(expected_action):
                if isinstance(extracted_action, ToolAction):
                    # extracted_action = cast(ToolAction, extracted_action)
                    expected_action = cast(ToolAction, expected_action)
                    # Compare tool_name and tool_query
                    if (
                        extracted_action.tool_name == expected_action.tool_name
                        and extracted_action.tool_query == expected_action.tool_query
                    ):
                        has_token_match = expected_eval_action.token_match(
                            "\n".join(extracted_action.tool_args)
                        )
                        has_full_match = expected_eval_action.full_match(
                            extracted_action, expected_action
                        )
                        if has_token_match:
                            break

                elif isinstance(extracted_action, AgentAction):
                    # Compare agent_version and agent_query
                    expected_action = cast(AgentAction, expected_action)
                    if (
                        extracted_action.agent_version == expected_action.agent_version
                        and extracted_action.agent_query == expected_action.agent_query
                    ):
                        has_token_match = expected_eval_action.token_match(
                            extracted_action.agent_query
                        )
                        has_full_match = expected_eval_action.full_match(
                            extracted_action, expected_action
                        )
                        if has_token_match:
                            break

                elif isinstance(extracted_action, ResultAction):
                    # Compare result_name
                    expected_action = cast(ResultAction, expected_action)
                    if extracted_action.result_name == expected_action.result_name:
                        has_token_match = expected_eval_action.token_match(
                            "\n".join(extracted_action.result_outputs)
                        )
                        has_full_match = expected_eval_action.full_match(
                            extracted_action, expected_action
                        )
                        if has_token_match:
                            break

        if not has_token_match:
            all_token_matches = False

        if not has_full_match:
            all_full_matches = False

    return EvalResult(token_match=all_token_matches, full_match=all_full_matches)
