EvalResult
==========

``EvalResult`` is an abstract class that represents the result of an
evaluation. This class gets an unique random string as ‘run_id’ on
instantiation and has abstract properties like ``is_full_match`` and
``is_partial_match``. It also contains two abstract methods -
``to_payload`` and ``from_payload`` for serialization and
deserialization of evaluation results.

Overview
--------

``EvalResult`` serves as a base for creation of specific evaluation
result objects in Automata platform. All evaluation result classes
should inherit from ``EvalResult`` and implement its properties and
methods. The primary purpose of the ``EvalResult`` class is to provide a
unified interface for dealing with evaluation results. The ``run_id``
attribute uniquely identifies each run of evaluation.

Related Symbols
---------------

-  ``automata.llm.llm_base.LLMCompletionResult.get_content``
-  ``automata.agent.openai_agent.OpenAIAutomataAgent.get_result``
-  ``automata.llm.llm_base.LLMCompletionResult.get_role``
-  ``automata.experimental.tools.builders.agentified_search_builder.AgentifiedSearchToolkitBuilder._get_formatted_search_results``
-  ``automata.experimental.search.symbol_search.SymbolSearch.symbol_references``
-  ``automata.experimental.search.symbol_search.SymbolSearch.process_query``

Example
-------

Since ``EvalResult`` is an abstract base class, you would not typically
instantiate it directly. Instead, you would create a new class that
inherits from ``EvalResult`` and implements its abstract methods and
properties.

Here is an example of how you might define such a class:

.. code:: python

   from automata.eval.eval_base import EvalResult
   from typing import Any

   class CustomEvalResult(EvalResult):

       # Implement the abstract properties
       @property
       def is_full_match(self) -> bool:
           # Implement the logic here
           pass

       @property
       def is_partial_match(self) -> bool:
           # Implement the logic here
           pass
       
       # Implement the abstract methods
       def to_payload(self) -> dict:
           # Convert the object into a dict or other serializable format
           pass

       @classmethod
       def from_payload(cls, payload: dict) -> 'CustomEvalResult':
           # Create a new object from a dict or other serialized format
           pass

Limitations
-----------

Being an abstract base class, ``EvalResult`` is not meant to be used
directly. The main limitation is that it defines a common interface but
does not provide an implementation. The actual functionality must be
provided by subclasses, meaning errors can occur if subclasses do not
properly implement all required methods and properties.

Follow-up Questions:
--------------------

-  How are ``run_ids`` used in the larger context of the Automata
   application?
-  What are the typical return types and key-value pairs expected in the
   ``to_payload`` and ``from_payload`` methods?
