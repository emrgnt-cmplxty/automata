-  New versions can be added to the ``InstructionConfigVersion`` enum by
   adding a new enum member in the definition of
   ``InstructionConfigVersion``. This will correspond to a filename in
   ``automata/configs/instruction_configs/``.
-  Changes in instruction versions potentially can have effects on the
   Automated Agent’s performance. If the instructions in a new version
   differ significantly from the old version, the agent might behave
   differently. Hence, whenever a new version is incorporated, a
   thorough testing and tuning of the agent might be necessary.
-  If an instruction version does not have a corresponding YAML
   configuration file, an error will likely be raised when the agent
   tries to use that instruction set. The application won’t be able to
   locate the file and will fail to start properly. Thus, it’s crucial
   to ensure that the necessary files exist when creating new versions.
