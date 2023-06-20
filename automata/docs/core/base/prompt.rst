automata.core.base.openai.Prompt
================================

``Prompt`` is an abstract base class that encapsulates everything
required to present the ``raw_prompt`` in different formats, such as a
normal unadorned format versus a chat format. It contains one abstract
method, ``to_formatted_prompt``, which must be implemented by any
subclass.

Methods
-------

to_formatted_prompt()
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   @abstractmethod
   def to_formatted_prompt(self):
       """
       Return the actual data to be passed as the `prompt` field to your model.
       See the above types to see what each API call is able to handle.
       """
       pass

This abstract method must be implemented by any subclass of ``Prompt``.
It should return the actual data to be passed as the ``prompt`` field to
the language model.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.base.tool.Tool``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Limitations
-----------

``Prompt`` is an abstract base class, which means it cannot be directly
instantiated. You’ll need to subclass it and implement the
``to_formatted_prompt()`` method to create a custom prompt class.

Follow-up Questions:
--------------------

-  In what scenarios would it be necessary to create a custom prompt
   subclass?
-  Are there any specific examples of ``Prompt`` subclasses in use in
   the codebase or existing applications?
