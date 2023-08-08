TemplateFormatter
=================

``TemplateFormatter`` is a utility class that helps in formatting agent
configurations in a dictionary format which enhances code readability
and maintainability. It supports operations for creating a default
formatter given a configuration, symbol ranking and maximum default
overview symbols.

Overview
--------

``TemplateFormatter`` is used for the preparation of formatted
configurations that are used by the system. This class offers a
``create_default_formatter`` static method which takes an
``AgentConfig``, a ``SymbolRank`` object, and an integer specifying the
maximum default overview symbols. This method builds a dictionary that
provides an overview of the top symbols in the system, as well as
important configuration settings including maximum iterations and
tokens.

The class is set up as a static utility, and all its methods are
available as static methods. This makes it an efficient tool to format
and present configurations and symbol rankings in a meaningful way which
is essential for debugging and system comprehension.

Related Symbols
---------------

-  ``config.automata_agent_config.AgentConfig``
-  ``experimental.search.symbol_rank.SymbolRank``
-  ``config.config_enums.AgentConfigName``

Example
-------

The following serves as an example for creating a dictionary for a
formatter with a default setup.

.. code:: python

   from automata.config.automata_agent_config import AgentConfig
   from automata.experimental.search.symbol_rank import SymbolRank
   from automata.config.formatter import TemplateFormatter
   from automata.config.config_enums import AgentConfigName

   #Initialize the AgentConfig
   agent_config = AgentConfig(AgentConfigName.AUTOMATA_MAIN)
   #Initialize SymbolRank object
   symbol_rank = SymbolRank()

   #Create a TemplateFormatter
   formatter = TemplateFormatter.create_default_formatter(agent_config, symbol_rank)

In the above example, the ``create_default_formatter`` method of
``TemplateFormatter`` is utilized to generate a format that presents key
configurations and symbol rankings in a readable manner.

Limitations
-----------

The TemplateFormatter assumes a specific configuration setup within the
system and has a rigidity in terms of input parameters. Also, the method
``create_default_formatter`` only works if the ``config_name`` of the
passed ``AgentConfig`` is ``AUTOMATA_MAIN``, otherwise it simply
generates an empty dictionary.

Follow-up Questions:
--------------------

-  How could additional class methods for alternate formatting styles be
   implemented?
-  How should the TemplateFormatter handle incorrect or unexpected input
   parameters for the ``create_default_formatter`` method? Should
   specific exceptions be defined?
-  What is the use case for ``create_default_formatter`` method when the
   ``AgentConfig``\ ’s ``config_name`` is not ``AUTOMATA_MAIN``?
