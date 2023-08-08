AgentEvalResult
===============

``AgentEvalResult`` is a Python class serving as a designated container
for storing the outcome from an evaluation of an agent. It’s a concrete
class that inherits from the ``EvalResult``, and is designed
specifically to accommodate results following agent evaluations.
Fundamentally, it holds the match results, extra actions taken by the
agent, and the associated session ID.

Overview
--------

The ``AgentEvalResult`` takes a dictionary of match results, a list of
extra actions, and an optional session id in its constructor. The match
results represent outcomes of each action taken by the agent as either
True or False (True being a successful match and False being a missed
match), while the extra actions contain any additional actions performed
by the agent that were not specified in the original instruction. The
session id is a unique identifier for the agent’s session.

The class also provides properties ``is_full_match`` and
``is_partial_match``, which are utilities to quickly determine if the
result is a full or partial match. A full match is when the agent
performs all of the expected actions according to the given instruction,
and a partial match is at least one of the expected actions was
performed.

The class provides methods to create a ``payload``, i.e., a dictionary
of the result, and to create an ``AgentEvalResult`` from a payload,
enabling serialization and deserialization of the objects.

Related Symbols
---------------

-  ``agent.agent_eval.AgentEvalResult.__repr__``: Represents the class
   object as a string.
-  ``eval_base.Action.to_payload``: Converts the Action to a dictionary.
-  ``eval_base.parse_action_from_payload``: Parses out the corresponding
   action from a raw dictionary.
-  ``eval.agent.agent_eval.AgentEvalResult.is_full_match``: Checks if
   the result is a full match.
-  ``eval.agent.agent_eval.AgentEvalResult.is_partial_match``: Checks if
   the result is a partial match.
-  ``eval.agent.agent_eval.AgentEvalResult.from_payload``: Creates an
   evaluation result from a dictionary (or other serialized format).
-  ``eval.eval_base.EvalResult.__init__``: Initializes the EvalResult
   class.

Usage Example
-------------

.. code:: python

   from automata.eval.agent.agent_eval import AgentEvalResult
   from automata.eval.eval_base import Action

   # Define action and match results
   actions = [{"type":"read","payload":{"text":"Read the document."},"time_to_live":5}]
   match_results = {Action.from_payload(action): True for action in actions}
   extra_actions = []

   # Define the agent evaluation result
   session_id = "123456"
   agent_result = AgentEvalResult(match_results, extra_actions, session_id)

   # Use the agent evaluation result
   is_full_match = agent_result.is_full_match

In this example, we first create a dictionary of match results with one
action “Read” which has successfully matched (True). We also specify no
extra actions (``extra_actions = []``). We then initialize an
``AgentEvalResult`` instance with the match results, empty
``extra_actions``, and a ``session_id``. ``is_full_match`` is a boolean
value indicating whether all actions were successfully matched.

Limitations
-----------

One of the limitations of the ``AgentEvalResult`` is that it assumes the
results to be in the form of a dictionary where actions are keys and the
match results are values (boolean). As such, if match results come in a
different format, conversion to the expected format is necessary before
initializing ``AgentEvalResult``.

Furthermore, the class is tightly coupled with the ``Action`` class, as
it expects actions to be instances of the ``Action`` class or its
subclass, which may limit the flexibility of using this class with
different action representations.

In the ``from_payload`` method, it raises a ``ValueError`` when the
payload contains invalid match results or session_id. This means
``AgentEvalResult`` assumes certain data hygiene of the inputs which
needs to be ensured by the calling class/function.

Follow-up Questions:
--------------------

-  How does the ``is_full_match`` property handle invalid or incomplete
   match results?
-  How are ``extra_actions`` utilized in the agent’s operations, and how
   does including them in AgentEvalResult aid in result analysis?
-  Could the handling of invalid match results or session IDs within
   ``from_payload`` method be better managed?
