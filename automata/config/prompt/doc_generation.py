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


readme = "{{readme}}"
TREE_STRUCTURE = textwrap.dedent(
    """
    .
    ├── __init__.py
    ├── cli
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── commands.py
    │   ├── options.py
    │   └── scripts
    │       ├── __init__.py
    │       ├── run_code_embedding.py
    │       ├── run_doc_embedding_l2.py
    │       ├── run_doc_embedding_l3.py
    │       └── run_doc_post_process.py
    └── core
        ├── __init__.py
        ├── coding
        │   ├── directory.py
        │   └── py_coding
        │       ├── module_tree.py
        │       ├── navigation.py
        │       ├── py_utils.py
        │       ├── retriever.py
        │       └── writer.py
        ├── context
        │   └── py_context
        │       └── retriever.py
        ├── database
        │   ├── __init__.py
        │   ├── provider.py
        │   └── vector.py
        ├── embedding
        │   ├── __init__.py
        │   ├── symbol_code_embedding.py
        │   ├── symbol_doc_embedding.py
        │   ├── embedding_types.py
        │   └── symbol_similarity.py
        ├── symbol
        │   ├── graph.py
        │   ├── parser.py
        │   ├── scip_pb2.py
        │   ├── search
        │   │   ├── __init__.py
        │   │   ├── rank.py
        │   │   └── symbol_search.py
        │   ├── base.py
        │   └── symbol_utils.py
        └── utils.py

    """
)

path = "{{path}}"
overview = "{{overview}}"
DEFAULT_DOC_POST_PROCESS_PROMPT = textwrap.dedent(
    f'''
    You are an autonomous coding agent working inside of a repository with the following README.md -\n{readme}\n

    The directory structure of the repository is as follows -\n{TREE_STRUCTURE}\n


    Your task is to use the following context from documentation which corresponds to the {path} directory to write an overview of the directory and its contents.

    ---BEGIN AGGREGATE DOCS---
    {overview}
    ---END AGGREGATE DOCS---


    NOTE: PLEASE DO NOT MIRROR THE STRUCTURE OF THE ORIGINAL DOCUMENTATION VERBATIM.

    Your goal in writing the documentation is to critically examine the provided context, pinpointing and selecting the most crucial information. The output should be rich in detail, explanatory, and indicative of your own understanding synthesized from the context.
    
    You should take inspiration from successful major projects, such as the Stripe developer documentation. 
    
    For instance, here is a snippet from the Stripe quickstart guide - 
    """
    
    Custom payment flow
    View the text-based guide


    Prebuilt checkout page

    Custom payment flow
    Learn how to embed a custom Stripe payment form in your website or application. The client- and server-side code builds a checkout form with Elements to complete a payment using various payment methods.
    If you’re looking for the individual Card Element integration builder, you can find it here. Before following that guide, you might want to learn more about when to use the Payment Element and the Card Element.

    Download full app
    Don't code? Use Stripe’s no-code options or get help from our partners.
    1
    Set up the server
    Install the Stripe Ruby library
    Install the Stripe ruby gem and require it in your code. Alternatively, if you’re starting from scratch and need a Gemfile, download the project files using the link in the code editor.

    Terminal

    Bundler

    GitHub
    Install the gem:
    gem install stripe

    Server
    Create a PaymentIntent
    Add an endpoint on your server that creates a PaymentIntent. A PaymentIntent tracks the customer’s payment lifecycle, keeping track of any failed payment attempts and ensuring the customer is only charged once. Return the PaymentIntent’s client secret in the response to finish the payment on the client.
    Server
    Configure payment methods
    With automatic_payment_methods enabled, we enable cards and other common payment methods for you by default, and you can enable or disable payment methods directly in the Stripe Dashboard. Before displaying the payment form, Stripe evaluates the currency, payment method restrictions, and other parameters to determine the list of supported payment methods. We prioritize payment methods that help increase conversion and are most relevant to the currency and the customer’s location.
    Server
    2
    Build a checkout page on the client
    Load Stripe.js
    Use Stripe.js to remain PCI compliant by ensuring that payment details are sent directly to Stripe without hitting your server. Always load Stripe.js from js.stripe.com to remain compliant. Don’t include the script in a bundle or host it yourself.

    """
    The final document should comprise of several pages of content and encompass the following sections: Introduction, Getting Started, Examples, Guidelines, and Limitations.

    1. **Introduction**: This section should give an overall context about the topic, hinting at its significance, use cases, and general functionality. 

    2. **Getting Started**: Here, provide a step-by-step guide for beginners. This should include setting up necessary prerequisites, installation (if applicable), and initial setup.

    3. **Examples**: This section should include functional examples from the original documentation. Preserve the logical consistency of the examples while ensuring they are easy to understand. Also, provide enough context so each example makes sense to the reader.

    4. **Guidelines**: Discuss best practices, effective strategies, and general recommendations for the optimal use of the subject at hand.

    5. **Limitations**: Highlight any potential limitations, risks, or drawbacks. This part should assist readers in understanding the possible challenges they might face and how to navigate them.

    Each section needs to be furnished with ample descriptive text. Keep the language clear, concise, and user-friendly. You should aim to provide substantial value to the reader in understanding the subject thoroughly.

    '''
)
