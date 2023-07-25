# import pytest

# from automata.llm.eval.code_writing import CodeWritingAction, CodeWritingEval
# from automata.core.run_handlers import run_agent_and_get_eval


# @pytest.mark.evaluation
# @pytest.mark.parametrize(
#     "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
#     [
#         # A simple instruction set with expected actions
#         (
#             "Return a valid executable code snippet in markdown, which when extracted and executed will set the variable `x` to the integer 10",
#             "automata-main",
#             [],
#             "gpt-3.5-turbo",
#             5,
#             [CodeWritingAction(object_types="int", object_value_repr="10")],
#         ),
#     ],
# )
# def test_eval_writing(
#     instructions,
#     agent_config_name,
#     toolkit_list,
#     model,
#     max_iterations,
#     expected_actions,
# ):
#     eval_result = run_agent_and_get_eval(
#         instructions,
#         agent_config_name,
#         toolkit_list,
#         model,
#         max_iterations,
#         expected_actions,
#         [CodeWritingEval()],
#     )
#     # check if all expected actions were performed
#     assert (
#         eval_result.full_match
#     ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"
