``AgentConfig`` Class
=====================

The ``AgentConfig`` class is a base abstraction for creating specific
configurations to be used by agent instances. It includes necessary
parameters such as instructions to be executed by the agent, a list of
tools used, a model name, and various boolean flags for stream and
verbose logging status.

In addition, it holds the max iterations and temperature settings for
the agent’s operation. It also has an optional session id attribute.

This class is an abstract base class (ABC), and it includes abstract
methods, requiring subclasses to provide concrete implementations of
these methods.

Attributes
----------

-  ``config_name``: Defines the name of the configuration.
-  ``tools``: Sets a list of Tools to be used by the agent.
-  ``instructions``: A string set by the user to handle instructions for
   the agent.
-  ``description``: A string to hold any necessary description.
-  ``model``: Defines the model to be used by the agent.
-  ``stream``: Boolean variable to define whether to use stream
   functionality.
-  ``verbose``: Boolean variable to define whether verbose logging
   should be used.
-  ``max_iterations``: Sets the maximum iterations count for the agent
   operations.
-  ``temperature``: Sets the temperature scalar for the agent
   operations.
-  ``session_id``: (Optional) Defines the session id for the agent.

Methods
-------

setup
~~~~~

A method that subclasses must implement. Its purpose is to be defined by
the subclasses.

load
~~~~

A method that subclasses must implement. It should load the agent
configuration based on the provided name.

get_llm_provider
~~~~~~~~~~~~~~~~

A static method that subclasses must implement. The method should return
the provider for the agent.

\_load_automata_yaml_config
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is responsible for loading YAML configuration for the agent.
It opens a YAML file, processes its content, and loads them into an
agent configuration instance. If ``config_name`` appears in the loaded
YAML, it raises an Exception. Once the loading completes, it adds
``config_name`` to the loaded YAML and returns it.

Inherited Classes
-----------------

The ``OpenAIAutomataAgentConfig`` is a concrete class that inherits from
``AgentConfig``. This class specifies ``OPENAI`` as the ``LLMProvider``
and allows the use of different models. It further enriches the
configuration by defining the system template, system template
variables, system template formatter, instruction version, and system
instruction.

Example
-------

Creating a derived class ``OpenAIAutomataAgentConfig`` and using the
``load`` method:

.. code:: python

       from automata.config.openai_agent import OpenAIAutomataAgentConfig
       from automata.config.base import AgentConfigName
       
       config = OpenAIAutomataAgentConfig.load(AgentConfigName.DEFAULT)
       assert isinstance(config, OpenAIAutomataAgentConfig)

Limitations
-----------

The class ``AgentConfig`` is an abstract base class and cannot be
directly used to create an object. It must be subclassed, and each
subclass must provide implementations for the abstract methods.

A derived class can load YAML configurations from a specific file
location, and this could raise file operation related exceptions. For
instance, if the configuration file is not found or if the YAML file is
not in the correct format, corresponding exceptions will be raised.

When a ``config_name`` is found in the loaded_yaml, the
``_load_automata_yaml_config`` method throws an error stating:
“config_name already specified in YAML. Please remove this from the YAML
file.” This could be a limitation when the user does not have much
control over the yaml content or if the yaml modification would conflict
with other requirements.

Follow-up Questions:
--------------------

-  How to manage the file operation exceptions when loading yaml
   configuration?
-  Can we modify ``_load_automata_yaml_config`` to allow ``config_name``
   in yaml or provide a mechanism to overwrite it?
-  What to do when we need to set up an ``AgentConfig`` with varying
   attributes not defined in existing classes?
