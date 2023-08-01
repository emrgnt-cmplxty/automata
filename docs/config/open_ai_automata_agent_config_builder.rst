Extending the builder to support custom agent configuration schemas:

The builder pattern by design is modular and extendable, thus custom
schemata or settings can be added in the following ways:

1. **Method Additions**: Add new methods to the
   ``OpenAIAutomataAgentConfigBuilder`` corresponding to new
   configuration settings. Each method should perform necessary
   validation and update the builder’s internal state.

2. **Subclassing**: If the customization involves significant changes in
   logic, one may consider creating a new builder class altogether,
   inheriting from ``OpenAIAutomataAgentConfigBuilder``.

Adding a more descriptive error when the model is not found:

This can be achieved by adding a method that checks if the model
(provided as argument) is found in the list of supported models before
setting the model. If the model is not found, a ``ValueError`` or a
custom error can be raised, indicating that the input model is not
supported. The error message can additionally provide a list of
supported models for user reference. To facilitate this:

1. A dedicated method can be added to check the model against the list
   of supported ones. This method should be invoked in the
   ``.with_model()`` method.

2. Enhance the ``.with_model()`` method itself to include the above
   check and raise an error in case of mismatch.
