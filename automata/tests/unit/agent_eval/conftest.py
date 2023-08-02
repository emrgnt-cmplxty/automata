from automata.eval import CodeWritingAction, OpenAIFunctionCallAction


def mock_openai_response_with_function_completion_message_1():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function1",
                        "arguments": '{"arg1": "value1"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_2():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function2",
                        "arguments": '{"arg2": "value2"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_final():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "call_termination",
                        "arguments": '{"result": "Success"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_3():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function3",
                        "arguments": '{"arg3": "value3"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_x():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nx = 1```",
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_y():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\ny = 'test'```",
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_z():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nz = 3.14```",
                }
            }
        ]
    }


def mock_openai_response_with_bad_code_action_completion_message_z():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nz = 3.1.4```",
                }
            }
        ]
    }


EXPECTED_FUNCTION_ACTIONS = [
    OpenAIFunctionCallAction(name="function1", arguments={"arg1": "value1"}),
    OpenAIFunctionCallAction(name="function2", arguments={"arg2": "value2"}),
]


EXPECTED_CODE_ACTIONS = [
    CodeWritingAction(object_type="int", object_value_repr="1", error=None),
    CodeWritingAction(object_type="str", object_value_repr="test"),
]


params = {
    "test_generate_function_eval_result_match_responses": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_2(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_eval_result_no_match_responses": [
        mock_openai_response_with_function_completion_message_3(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_eval_result_partial_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_match": [
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_code_action_completion_message_y(),
        mock_openai_response_with_code_action_completion_message_z(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_partial_match": [
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_result_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_code_action_completion_message_z(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_partial_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_evaluation_harness_and_metrics": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_bad_code_action_completion": [
        mock_openai_response_with_bad_code_action_completion_message_z(),
    ],
}
