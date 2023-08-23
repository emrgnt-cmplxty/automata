from automata.eval import CodeWritingAction, OpenAIFunctionCallAction


# TODO - cleanup hacky use of `call-termination` throughout tests here.
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
                        "name": "call-termination",
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
                    "content": None,
                    "function_call": {
                        "name": "call-termination",  # TODO - Avoid having multiple call-terminations
                        "arguments": '{"result": "```python\nx = 1```"}',
                    },
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
                    "content": None,
                    "function_call": {
                        "name": "call-termination",  # TODO - Avoid having multiple call-terminations
                        "arguments": '{"result": "```python\nz = 3.14```"}',
                    },
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
                    "content": None,
                    "function_call": {
                        "name": "call-termination",  # TODO - Avoid having multiple call-terminations
                        "arguments": '{"result": "```python\nz = 3.1.4```"}',
                    },
                }
            }
        ]
    }


EXPECTED_FUNCTION_ACTIONS = [
    OpenAIFunctionCallAction(name="function1", arguments={"arg1": "value1"}),
    OpenAIFunctionCallAction(name="function2", arguments={"arg2": "value2"}),
]


EXPECTED_CODE_ACTIONS = [
    CodeWritingAction(py_object=1, error=None),
    CodeWritingAction(py_object="test", error=None),
]
COMPLICATED_ACTION = CodeWritingAction(
    py_object=CodeWritingAction(py_object="test2", error=None), error=None
)


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
        # mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_partial_match": [
        mock_openai_response_with_code_action_completion_message_x(),
        # mock_openai_response_with_function_completion_message_final(), --> final isn't necessary since code_action returns final action
    ],
    "test_generate_code_writing_eval_result_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_result_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        # mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_partial_match": [  # TODO - Implement this...
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_evaluation_harness_and_metrics": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        # mock_openai_response_with_function_completion_message_final(),
    ],
    "test_bad_code_action_completion": [
        mock_openai_response_with_bad_code_action_completion_message_z(),
    ],
}
