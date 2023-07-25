# import random

# import pytest

# from automata.llm.eval.eval_providers import OpenAIFunctionCallAction
# from automata.core.run_handlers import run_agent_and_get_eval


# @pytest.mark.evaluation
# @pytest.mark.parametrize(
#     "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
#     [
#         (
#             "Fetch the source code for VectorDatabaseProvider.",
#             "automata-main",
#             ["py-reader"],
#             "gpt-4",
#             2,
#             [
#                 OpenAIFunctionCallAction(
#                     name="py-retriever-code",
#                     arguments={
#                         "module_path": "automata.core.base.database.vector",
#                         "node_path": "VectorDatabaseProvider",
#                     },
#                 )
#             ],
#         ),
#     ],
# )
# def test_eval_read(
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
#     )

#     assert (
#         eval_result.full_match
#     ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"


# random_suffix = random.randint(0, 1000000)


# @pytest.mark.evaluation
# @pytest.mark.parametrize(
#     "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
#     [
#         (
#             f"Create a new module with a hello world function at automata.test_module_{random_suffix}",
#             "automata-main",
#             ["py-writer"],
#             "gpt-4",
#             2,
#             [
#                 OpenAIFunctionCallAction(
#                     name="py-writer-create-new-module",
#                     arguments={
#                         "module_name": f"automata.test_module_{random_suffix}",
#                         "content": "def hello_world():\n    print('Hello, world!')",
#                     },
#                 )
#             ],
#         ),
#     ],
# )
# def test_eval_py_write(
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
#     )
#     # TODO - Add post test cleanup which deletes the test_module_{random_suffix} module
#     assert (
#         eval_result.full_match
#     ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"
