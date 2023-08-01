-  Guidelines for ``generate_eval_result`` and ``process_result``
   implementations would typically be related to the specific needs of
   the project or organization. However, it is important to ensure that
   the method implementations are performant, and return results in a
   consistent, easily understood format. Precise documentation is
   crucial to ensure consistency and clarity for any developers
   implementing these methods.
-  Specific criteria or metrics to be evaluated by subclasses of
   ``AgentEval`` will be dependent on the objectives of the project.
   However, it can be enforced by defining abstract methods in the
   ``AgentEval`` base class that each subclass must implement. Strict
   interface definitions will force subclasses to implement certain
   methods, ensuring they evaluate the required metrics.
-  ``AgentEval`` can handle cases where the expected actions do not
   fully map to the LLM’s capabilities by returning an exception or
   error condition in the output of the evaluation. This can help in
   identifying the deficit areas of the LLM, letting developers take
   steps to improve or expand on those areas. Alternatively, the
   evaluation could include a measure of how many or what percentage of
   expected actions the LLM was able to perform.
