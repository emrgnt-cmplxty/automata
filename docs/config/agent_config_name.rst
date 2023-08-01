-  To add new configuration files and ensure they can be loaded with
   ``AgentConfigName``, follow these steps:

   -  The new configuration file should be added to the
      ``automata/config/agent/`` directory.
   -  Update the ``AgentConfigName`` enumeration class with a new
      enumeration value that is the name of the new file (excluding the
      ``.yaml`` extension).
   -  In the ``AgentConfig`` class, update the ``load`` classmethod to
      properly load the new configuration file based on the given
      enumeration value.

-  Configurations are typically validated by using a validation schema
   or a set of rules defined in the code. An example can be checking for
   required fields, ensuring that values are within a certain range, or
   that they adhere to a specific format. If a configuration does not
   match these set rules, an error is thrown when attempting to load it.
   This process is not detailed for ``AgentConfigName`` specifically but
   generally happens in conjunction with the ``AgentConfig``
   implementation.
