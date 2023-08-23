import ast
import json
import logging
import os
import textwrap
from typing import Dict, List, Optional, Set, Tuple

from automata.core.utils import get_root_py_fpath
from automata.llm import OpenAIChatCompletionProvider, OpenAIConversation
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.symbol_utils import get_rankable_symbols

logger = logging.getLogger(__name__)
PAYLOADS = ["single_target_search_payload"]
RAW_PROMPT_TEXT = textwrap.dedent(
    '''
                           
You are Automata, a system designed by OpenAI to code at the highest level. Your primary purpose is to carry out user provided tasks.

Your first task in this session is to convert provided source code into a payload of queries and results. The queries should describe the relevant classes, methods, and standalone files in side of the provided module. The final return result should be formatted into a json payload. Please us the two following examples to further familiarize yourself with the task at hand:

Example 1
----------

## Source Code 

```python

# automata.eval.eval_base

class EvalResult(ABC):
    """An abstract class to represent the result of an evaluation."""

    def __init__(self, *args, **kwargs):
        # TODO - Add tests for run_id
        self.run_id = kwargs.get("run_id") or str(uuid.uuid4())
        if not isinstance(self.run_id, str):
            raise ValueError("run_id must be a string.")

    @property
    @abstractmethod
    def is_full_match(self) -> bool:
        """Indicates whether the evaluation was a full match."""

    @property
    @abstractmethod
    def is_partial_match(self) -> bool:
        """Indicates whether the evaluation was a partial match."""

    @abstractmethod
    def to_payload(self) -> Payload:
        """Converts the evaluation result to a dictionary (or other serializable format)."""

    @classmethod
    @abstractmethod
    def from_payload(cls, payload: Payload) -> "EvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""


```

## Parsed Results

```json
[
    {
        "query": "What abstract base class represents the result of an evaluation?",
        "result": "automata.eval.eval_base.EvalResult"
    },
    {
        "query": "How is the EvalResult object constructed?",
        "result": "automata.eval.eval_base.EvalResult.__init__"
    },
    {
        "query": "What abstract method is used to determine if an evaluation was a full match?",
        "result": "automata.eval.eval_base.EvalResult.is_full_match"
    },
    {
        "query": "What abstract property is used to determine if an evaluation was a partial match?",
        "result": "automata.eval.eval_base.EvalResult.is_partial_match"
    },
    {
        "query": "What abstract method is used to convert an evaluation into a `Payload`?",
        "result": "automata.eval.eval_base.EvalResult.to_payload"
    },
    {
        "query": "How can an EvalResult instance be created from a `Payload`?",
        "result": "automata.eval.eval_base.EvalResult.from_payload"
    }
]
```



Example 2
----------

## Source Code

```python

# automata.eval.agent.agent_eval

class AgentEvalResult(EvalResult):
    """A concrete class to represent the result of an agent eval."""

    def __init__(
        self,
        match_results: Dict[Action, bool],
        extra_actions: List[Action],
        session_id: Optional[str],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.match_results = match_results
        self.extra_actions = extra_actions
        self.session_id = session_id

    def __repr__(self) -> str:
        return f"AgentEvalResult(match_results={self.match_results}, extra_actions={self.extra_actions}, session_id={self.session_id}, run_id={self.run_id})"

    @property
    def is_full_match(self) -> bool:
        """Checks if the result is a full match."""
        return all(self.match_results.values())

    @property
    def is_partial_match(self) -> bool:
        """Checks if the result is a partial match."""
        return any(self.match_results.values())

    def to_payload(self) -> Payload:
        """Converts the result to a dictionary."""

        match_results = {
            json.dumps(action.to_payload()): str(result)
            for action, result in self.match_results.items()
        }
        extra_actions = [
            json.dumps(action.to_payload()) for action in self.extra_actions
        ]

        return {
            "match_results": match_results,
            "extra_actions": extra_actions,
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "AgentEvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""

        matches = payload["match_results"]
        if not isinstance(matches, dict) or not all(
            isinstance(item, str) for item in matches.keys()
        ):
            raise ValueError(
                f"An invalid match result was encountered in {matches}"
            )

        match_results = {
            parse_action_from_payload(json.loads(action)): result == "True"
            for action, result in matches.items()
        }

        extra_actions = [
            parse_action_from_payload(json.loads(action))
            for action in payload["extra_actions"]
        ]

        session_id = payload.get("session_id")
        if session_id is not None and not isinstance(session_id, str):
            raise ValueError(
                f"Invalid session_id ({session_id}) was observed."
            )
        run_id = payload.get("run_id")

        return cls(
            match_results=match_results,
            extra_actions=extra_actions,
            session_id=session_id,
            run_id=run_id,
        )

```json
[
    {
        "query": "What concrete class represents the result of an agent evaluation?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult"
    },
    {
        "query": "What method is used to construct the AgentEvalResult?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.__init__"
    },
    {
        "query": "How is the AgentEvalResult represented as a string for debugging?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.__repr__"
    },
    {
        "query": "What property is used to determine if an agent evaluation was a full match?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.is_full_match"
    },
    {
        "query": "What property is used to determine if an agent evaluation was a partial match?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.is_partial_match"
    },
    {
        "query": "What method is used to convert an agent evaluation into a `Payload`?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.to_payload"
    },
    {
        "query": "How can an AgentEvalResult instance be created from a `Payload`?",
        "result": "automata.eval.agent.agent_eval.AgentEvalResult.from_payload"
    }
]
```

Example 3
---------

## Source Code Omitted

```json
[
    {
        "query": "Which class is an abstract base class for creating agents?",
        "result": "automata.agent.agent.Agent"
    },
    {
        "query": "Which class is an abstract base class for building agent tools?",
        "result": "automata.agent.agent.AgentToolkitBuilder"
    },
    {
        "query": "Which class enumerates the available agent tools?",
        "result": "automata.agent.agent.AgentToolkitNames"
    },
    {
        "query": "Which class represents a general agent error?",
        "result": "automata.agent.error.AgentGeneralError"
    },
    {
        "query": "Which class is a concrete class for building OpenAI agent tools?",
        "result": "automata.agent.openai_agent.OpenAIAgentToolkitBuilder"
    },
    {
        "query": "Which class is a concrete class for building OpenAI agents?",
        "result": "automata.agent.openai_agent.OpenAIAutomataAgent"
    },
    {
        "query": "Which method of an OpenAI agent is responsible for running the agent?",
        "result": "automata.agent.openai_agent.OpenAIAutomataAgent.run"
    },
    {
        "query": "Which private method does the OpenAI agent call to perform setup?",
        "result": "automata.agent.openai_agent.OpenAIAutomataAgent._setup"
    },
]


Below is the source code for which your task is to extract a similar JSON payload. Reminder, for this task each query should correspond to a specific class, method, or standalone function in the defined module. Lastly, the result should be a single line item. Begin - 

```python
{SOURCE_CODE}
```
'''
)
MODEL = "gpt-4"
TEMPERATURE = 0.7
STREAM = True
EVAL_ROOT_PATH = os.path.join(get_root_py_fpath(), "config", "eval")


def load_json_data(filepath: str) -> List[Dict[str, List[Dict[str, str]]]]:
    """Loads the JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def save_json_data(
    filepath: str, data: List[Dict[str, List[Dict[str, str]]]]
) -> None:
    """Saves the JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def get_processed_paths(
    data: List[Dict[str, List[Dict[str, str]]]]
) -> Set[str]:
    """Gets the observed paths from the JSON data."""
    processed_paths = set([])
    for item in data:
        for entry in item["entries"]:
            logger.info(f"Loading Entry {entry}")
            if not isinstance(entry["result"], str):
                continue
            processed_paths.add(entry["result"])
    return processed_paths


def filter_entries(
    data: List[Dict[str, List[Dict[str, str]]]],
    expected_symbol_dotpaths: Set[str],
) -> List[Dict[str, List[Dict[str, str]]]]:
    """Filters the entries in the JSON data."""
    for item in data:
        item["entries"] = [
            entry
            for entry in item["entries"]
            if isinstance(entry["result"], str)
            if entry["result"] in expected_symbol_dotpaths
        ]
    return data


def get_missing_symbols(
    processed_paths: Set[str], expected_symbol_dotpaths: Set[str]
) -> Set[str]:
    """Returns a list of the missing symbols."""
    return {
        symbol
        for symbol in expected_symbol_dotpaths
        if symbol not in processed_paths
    }


def get_extra_symbols(
    processed_paths: Set[str], expected_symbol_dotpaths: Set[str]
) -> Set[str]:
    """Returns a list of the extra symbols."""
    return {
        symbol
        for symbol in processed_paths
        if symbol not in expected_symbol_dotpaths
    }


def call_completion_provider(
    module_dot_fpath: str, module: ast.Module
) -> List[Dict[str, str]]:
    """Build a completion provider and call it."""
    conversation = OpenAIConversation()
    completion_provider = OpenAIChatCompletionProvider(
        model=MODEL,
        temperature=TEMPERATURE,
        stream=STREAM,
        conversation=conversation,
        functions=[],
    )

    # Call a one-time completion with the provided context
    result = completion_provider.standalone_call(
        RAW_PROMPT_TEXT.replace(
            "{SOURCE_CODE}",
            f"# {module_dot_fpath}\n{ast.unparse(module)}",
        )
    )

    # Process the output
    cleaned_result = (
        result.split("```json")[1].split("```")[0].strip()
        if "```json" in result
        else result
    )
    return json.loads(cleaned_result)


def process_missing_symbols(
    data_path: str,
    module_dot_fpath: str,
    module: ast.Module,
    missing_symbols_dotpaths: Set[str],
    filtered_data: List[Dict[str, List[Dict[str, str]]]],
) -> None:
    """Process missing symbols."""
    is_missing_entry = False
    for symbol in missing_symbols_dotpaths:
        if module_dot_fpath in symbol:
            if not is_missing_entry:
                logger.info(f"Processing module {module_dot_fpath}")
                logger.info("  Listing missing symbols:")
                is_missing_entry = True
            logger.info(f"    {symbol}")
    if is_missing_entry:
        try:
            processed_payload = call_completion_provider(
                module_dot_fpath, module
            )
            filtered_data[0]["entries"].extend(processed_payload)

            # Save the JSON data just in case of crash
            # because completion operations are expensive
            save_json_data(data_path, filtered_data)
            logger.info(
                f'There are now {len(filtered_data[0]["entries"])} entries in the dataset.'
            )
        except Exception as e:
            logger.error(f"Error parsing result {e}")


def filter_and_log_symbols(
    data: List[Dict[str, List[Dict[str, str]]]],
    expected_symbol_dotpaths: Set[str],
    processed_paths: Set[str],
) -> Tuple[List[Dict[str, List[Dict[str, str]]]], Set[str]]:
    """Filters and logs the symbols"""
    filtered_data = filter_entries(data, expected_symbol_dotpaths)
    extra_symbol_dotpaths = get_extra_symbols(
        processed_paths, expected_symbol_dotpaths
    )
    missing_symbols_dotpaths = get_missing_symbols(
        processed_paths, expected_symbol_dotpaths
    )

    missing_symbols_dotpaths = {
        ele for ele in missing_symbols_dotpaths if "test" not in ele
    }

    logger.warning(
        f"We found {len(extra_symbol_dotpaths)} extra symbols = {extra_symbol_dotpaths}"
    )
    logger.warning(
        f"We found {len(missing_symbols_dotpaths)} missing symbols = {missing_symbols_dotpaths}"
    )
    return filtered_data, missing_symbols_dotpaths


def load_and_process_data(
    data_path: str,
) -> Tuple[List[Dict[str, List[Dict[str, str]]]], Set[str]]:
    """Loads the input data and processes the paths"""
    data = load_json_data(data_path)
    processed_paths = get_processed_paths(data)
    return data, processed_paths


def process_symbol_graph() -> Set[str]:
    """Processes the symbol graph to fetch the local rankable symbols"""
    symbol_graph = dependency_factory.get("symbol_graph")
    symbol_graph._initialized = True  # mock initialization
    return {
        symbol.dotpath
        for symbol in get_rankable_symbols(
            symbol_graph.get_sorted_supported_symbols()
        )
    }


def process_modules(
    data_path: str,
    filtered_data: List[Dict[str, List[Dict[str, str]]]],
    missing_symbols_dotpaths: Set[str],
) -> None:
    """Process the modules in the local path"""
    for module_path, module in py_module_loader.items():
        logger.info(f"Examining module at {module_path}")
        if "__init__" in module_path:
            continue
        if not module:
            continue
        process_missing_symbols(
            data_path,
            module_path,
            module,
            missing_symbols_dotpaths,
            filtered_data,
        )


def process_payload(payload: str, eval_rootpath: str) -> None:
    """Process a single payload."""
    logger.info(f"Processing payload = {payload}")

    data_path = os.path.join(eval_rootpath, f"{payload}.json")
    data, processed_paths = load_and_process_data(data_path)

    expected_symbol_dotpaths = process_symbol_graph()

    (
        filtered_data,
        missing_symbols_dotpaths,
    ) = filter_and_log_symbols(data, expected_symbol_dotpaths, processed_paths)

    process_modules(data_path, filtered_data, missing_symbols_dotpaths)

    save_json_data(data_path, filtered_data)

    logger.warning(f"Finished processing {payload}.")


def main(eval_rootpath: str, payloads: Optional[List[str]] = None) -> None:
    if not payloads:
        payloads = PAYLOADS
    """Run the main event loop for updating tool evaluations"""
    logger.info("Initialized, now running over payloads")
    py_module_loader.initialize()

    for payload in payloads:
        process_payload(payload, eval_rootpath)
    return


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    logger.info("Running tool eval")

    # Load the target evals
    main(EVAL_ROOT_PATH)
