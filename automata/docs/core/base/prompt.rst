Prompt
======

``Prompt`` is an abstract base class that encapsulates everything
required to present the ``raw_prompt`` in different formats, such as a
normal unadorned format vs. a chat format. This class can be subclassed
to create concrete implementations for specific prompt types.

Overview
--------

``Prompt`` provides an abstract method ``to_formatted_prompt`` that is
responsible for providing the actual data to be passed as the ``prompt``
field to the model. Subclasses of ``Prompt`` should implement this
method to handle different prompt formats. The ``Prompt`` class is used
throughout the Automata framework on various occasions, such as creating
response suggestions or interacting with an API.

Related Symbols
---------------

-  ``automata.core.base.openai.CompletionPrompt``
-  ``automata.core.base.openai.text_prompt_to_chat_prompt``
-  ``automata.core.base.openai.is_chat_prompt``
-  ``automata.core.base.openai.CompletionPrompt.to_formatted_prompt``

Example
-------

The following example demonstrates how to create a custom class that
implements the ``Prompt`` interface. In this example, we create a
``CustomPrompt`` class that formats the raw prompt as an instruction.

.. code:: python

   from automata.core.base.openai import Prompt

   class CustomPrompt(Prompt):
       def __init__(self, raw_prompt: str):
           super().__init__(raw_prompt)

       def to_formatted_prompt(self) -> str:
           return f"Instruction: {self.raw_prompt}"

   raw_prompt = "Find the sum of 3 and 5"
   prompt = CustomPrompt(raw_prompt)
   formatted_prompt = prompt.to_formatted_prompt()
   print(formatted_prompt)  # Output: "Instruction: Find the sum of 3 and 5"

Limitations
-----------

As an abstract base class, ``Prompt`` has no direct limitations.
However, the design of the class assumes that the prompt format can be
determined using a single method (``to_formatted_prompt``). There might
be cases where multiple methods or additional information are required
for prompt formatting, in which case the class design should be
extended.

Follow-up Questions:
--------------------

-  Are there any specific considerations for prompt formatting that
   should be addressed by subclasses implementing the ``Prompt``
   interface?
