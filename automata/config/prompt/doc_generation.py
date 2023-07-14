import textwrap

DOC_EXAMPLE_0 = textwrap.dedent(
    '''
    ...
    ## Usage Example

    ```python
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    import torch

    src_text = [
        """ PG&E .... """
    ]

    model_name = "google/pegasus-xsum"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    batch = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(device)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    assert (
        tgt_text[0]
        == "California's..."
    )
    '''
)

DOC_EXAMPLE_1 = textwrap.dedent(
    """
    # AutomataAgentConfig

    `AutomataAgentConfig` is a configuration class that helps configure, setup, and interact with an `AutomataAgent`. It contains various attributes such as `config_name`, `instruction_payload`, `tool_builders`, and others to provide the necessary setup and settings to be used by the agent.

    ## Overview

    `AutomataAgentConfig` provides a way to load the agent configurations specified by the `AgentConfigName`. The configuration options can be set during the instantiation of the class or can be loaded using the `load` classmethod. It provides utility methods to load and setup agent configurations while also validating the provided settings. The class offers a convenient way to create an agent with custom configurations and includes closely related symbols like `AgentConfigName`.

    ## Related Symbols

    - `config.config_enums.AgentConfigName`
    - `automata.agent.agent.AutomataAgent`
    - `config.automata_agent_config_utils.AutomataAgentConfigBuilder`
    - `automata.coordinator.automata_instance.AutomataInstance`

    ## Example

    The following is an example demonstrating how to create an instance of `AutomataAgentConfig` using a predefined configuration name.

    ```python
    from config.automata_agent_config import AutomataAgentConfig
    from config.config_enums import AgentConfigName

    config_name = AgentConfigName.AUTOMATA_MAIN
    config = AutomataAgentConfig.load(config_name)
    ```

    ## Limitations

    The primary limitation of `AutomataAgentConfig` is that it relies on the predefined configuration files based on `AgentConfigName`. It can only load configurations from those files and cannot load custom configuration files. In addition, it assumes a specific directory structure for the configuration files.

    ## Follow-up Questions:

    - How can we include custom configuration files for loading into the `AutomataAgentConfig` class?
    
    """
)

symbol_dotpath = "{{symbol_dotpath}}"
symbol_context = "{{symbol_context}}"
DEFAULT_DOC_GENERATION_PROMPT = textwrap.dedent(
    f"""
    Generate the documentation for {symbol_dotpath} using the context shown below -\n{symbol_context}\n
    The output documentation should include an overview section, related symbols, examples, and discussion around limitations.
    Examples should be comprehensive and readily executable (e.g. correct imports and values).
    If there are references to 'Mock' objects in test files from your context, do your best to replace these with the actual underlying object.
    If that is not possible, note this in a footnote. Mock objects are used in testing to simplify working with complex objects.
    For reference, write in the style of in the original Python Library documentation -\n{DOC_EXAMPLE_0}\n
    For further reference, see the local documentation here -\n{DOC_EXAMPLE_1}\n
    Some information is just included for contextual reference, and this may be omitted from the output documentation.
    Start the documentation with a header that includes only the class name.
    Lastly, if some points are unclear, note these in a footnote that begins with ## Follow-up Questions:
    """
)
