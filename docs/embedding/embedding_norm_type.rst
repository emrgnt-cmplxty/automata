As an AI model, I don’t have access to the real-time codebase or
updates. Based on general programming practice:

1. Expanding the ``EmbeddingNormType`` enumeration with more
   normalization options is generally possible. It would involve
   defining additional constants within the enumeration to represent the
   new normalization types. However, it also requires that the
   corresponding normalization algorithms are implemented in the
   embedding calculations where this enumeration is used.

2. In order to use a user-defined norm type in the embedding calculation
   process, the code must be modular enough to accept a custom function
   that performs the normalization. If the code is not currently
   designed in this way, it would need to be refactored to enable this
   functionality. This could involve changes to the
   ``EmbeddingSimilarityCalculator`` class and wherever the
   ``EmbeddingNormType`` enumeration is used in the calculation logic.
   Please check the documentation or contact a maintainer to understand
   the current possibilities.
