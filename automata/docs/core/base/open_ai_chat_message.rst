OpenAIChatMessage
=================

``OpenAIChatMessage`` is a simple data structure used to represent chat
messages in the context of OpenAI’s Chat API. It contains two
attributes: ``role`` and ``content``. The ``role`` attribute represents
the role of the message sender, which can be “system”, “user”, or
“assistant”. The ``content`` attribute holds the text of the chat
message.

Methods
-------

-  ``to_dict``: Convert the OpenAIChatMessage instance to a dictionary
   with “role” and “content” as keys.

Example
-------

.. code:: python

   from automata.core.base.openai import OpenAIChatMessage
   msg = OpenAIChatMessage(role="user", content="Hello, world!")
   msg_dict = msg.to_dict()

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Limitations
-----------

``OpenAIChatMessage`` is a basic data structure and is not responsible
for handling the communication with the Chat API directly. It is
designed to be used in conjunction with other classes to structure and
format messages to interact with the API. Consequently, it does not
provide any functionality beyond representing and converting messages to
dictionaries.

Follow-up Questions:
--------------------

-  How are the ``OpenAIChatMessage`` instances being utilized when
   interacting with the Chat API?
