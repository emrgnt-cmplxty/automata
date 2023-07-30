import json
from typing import Any, Dict, List, Optional, Tuple, Union

from automata.eval.eval_base import (
    Action,
    Payload,
    parse_action_from_payload,
    register_action,
)

# Symbol Search Evaluation Result
from automata.eval.tool.tool_eval import ToolEval, ToolEvalResult
from automata.llm import FunctionCall

# TODO - Make this configurable somewhere upstream
TOP_K_MATCHES = 10


@register_action
class SymbolSearchAction(Action):
    """A concrete action representing a symbol search."""

    def __init__(self, query: str, search_results: Optional[List[str]] = None):
        self.query = query
        self.search_results = search_results or []

    def __eq__(self, other):
        if not isinstance(other, SymbolSearchAction):
            return False

        return (
            self.query == other.query
            and self.search_results == other.search_results
        )

    def __hash__(self):
        return hash((self.query, tuple(self.search_results)))

    def __repr__(self):
        return f"SymbolSearchAction(query={self.query}, search_results={self.search_results})"

    def to_payload(self) -> Payload:
        """Converts a SymbolSearchAction into a payload for storing."""

        return {
            "type": "SymbolSearchAction",
            "query": self.query,
            "search_results": ",".join(self.search_results),
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "SymbolSearchAction":
        """Converts a payload SymbolSearchAction into underlying payload."""

        query = payload["query"]
        if not isinstance(query, str):
            raise ValueError(
                f"Query of type={type(query)} received, instead of str."
            )

        search_results = payload["search_results"]
        if not isinstance(search_results, str):
            raise ValueError(
                f"Search results of type={type(search_results)} received, instead of str."
            )

        return cls(query=query, search_results=search_results.split(","))


class SymbolSearchEvalResult(ToolEvalResult):
    """A concrete class to represent the result of a symbol search eval."""

    def __init__(
        self,
        expected_action: SymbolSearchAction,
        observed_action: Optional[SymbolSearchAction],
        *args,
        **kwargs,
    ):
        super().__init__(expected_action, observed_action, *args, **kwargs)

        if not isinstance(expected_action, SymbolSearchAction):
            raise ValueError(
                "Expected action must be of type SymbolSearchAction."
            )
        if observed_action is not None and not isinstance(
            observed_action, SymbolSearchAction
        ):
            raise ValueError(
                f"Expected action must be of type SymbolSearchAction, not {type(observed_action)}"
            )

        self.top_match = (
            observed_action.search_results[0] if observed_action else "None"
        )
        if self.observed_action:
            self.top_k_matches = (
                observed_action.search_results[:TOP_K_MATCHES]
                if observed_action
                else []
            )
            if len(self.top_k_matches) < TOP_K_MATCHES:
                self.top_k_matches += ["None"] * (
                    TOP_K_MATCHES - len(self.top_k_matches)
                )
        else:
            self.top_k_matches = ["None"] * TOP_K_MATCHES

        self.expected_match = (
            expected_action.search_results[0]
            if expected_action.search_results
            else "None"
        )

    def __repr__(self):
        return f"SymbolSearchEvalResult(observed_action={self.observed_action}, expected_action={self.expected_action})"

    @property
    def is_full_match(self) -> bool:
        """Checks if the result is a full match (Exact Match at 0th entry)."""
        return self.expected_match == self.top_match

    @property
    def is_partial_match(self) -> bool:
        """Checks if the result is a partial match (Exact Match within top K entries)."""
        return (
            self.expected_match in self.top_k_matches
            if self.observed_action
            else False
        )

    def get_details(self) -> Dict[str, Union[Optional[Action], str]]:
        """Gets the details of the result."""
        return {
            "expected_match": self.expected_match or "None",
            "observed_action": self.observed_action,
        }

    def get_extra_info(self) -> Dict[str, Any]:
        """Gets the extra info of the result."""
        return {}

    def to_payload(self) -> Payload:
        """Converts the evaluation result to a dictionary (or other serializable format)."""
        return {
            "expected_action": json.dumps(self.expected_action.to_payload()),
            "observed_action": json.dumps(self.observed_action.to_payload())
            if self.observed_action
            else "None",
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "SymbolSearchEvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""

        expected_action = payload["expected_action"]
        if not isinstance(expected_action, str):
            raise ValueError("Expected action must be a string.")

        parsed_expected_action = parse_action_from_payload(
            json.loads(expected_action)
        )

        if not isinstance(parsed_expected_action, SymbolSearchAction):
            raise ValueError("Expected action must be a SymbolSearchAction.")

        observed_action = payload["observed_action"]
        parsed_observed_action = None
        if observed_action:
            if not isinstance(observed_action, str):
                raise ValueError("Observed action must be a string or None.")

            parsed_observed_action = parse_action_from_payload(
                json.loads(observed_action)
            )

        if parsed_observed_action is not None and not isinstance(
            parsed_observed_action, SymbolSearchAction
        ):
            raise ValueError(
                "Expected action must be a SymbolSearchAction or None."
            )

        return cls(
            expected_action=parsed_expected_action,
            observed_action=parsed_observed_action,
        )


class SymbolSearchEval(ToolEval):
    """A class for evaluating an LLM's symbol searching ability."""

    def __init__(self):
        pass

    def extract_action(
        self, input_action_tuple: Tuple[FunctionCall, str]
    ) -> Action:
        """Extracts the search action implicitly"""

        function_call, result = input_action_tuple
        split_results: List[str] = []

        if function_call.name == "symbol-rank-search":
            split_results = result.split("\n")
        else:
            raise ValueError("Only symbol-search is supported for now.")

        query = function_call.arguments["query"]
        return SymbolSearchAction(query=query, search_results=split_results)

    def to_tool_result(
        self, expected_action: Action, observed_action: Optional[Action]
    ) -> ToolEvalResult:
        if not isinstance(expected_action, SymbolSearchAction):
            raise ValueError("Expected action must be a SymbolSearchAction.")
        if observed_action is not None and not isinstance(
            observed_action, SymbolSearchAction
        ):
            raise ValueError(
                "Observed action must be a SymbolSearchAction or None."
            )

        return SymbolSearchEvalResult(
            expected_action,
            observed_action,
        )
