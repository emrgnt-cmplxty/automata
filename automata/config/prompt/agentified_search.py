"""Defines the agentified search prompt template."""
import textwrap

AGENTIFIED_SEARCH_TEMPLATE = textwrap.dedent(
    """
                               
                               Here are a few examples of matchign a search query to a best match


Example 1
----------

Search Query: What method is used in SymbolEmbeddingHandler to get the sorted supported symbols?

- Observed Results - 

Top 10 Search Results: ['automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler._get_sorted_supported_symbols', 'automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler', 'automata.symbol.graph.symbol_graph.SymbolGraph._get_sorted_supported_symbols', 'automata.symbol.symbol_base.ISymbolProvider._get_sorted_supported_symbols', 'automata.symbol.symbol_base.ISymbolProvider.get_sorted_supported_symbols', 'automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler.get_all_ordered_embeddings', 'automata.context_providers.symbol_synchronization_context.SymbolProviderRegistry.get_sorted_supported_symbols', 'automata.symbol.graph.symbol_navigator.SymbolGraphNavigator.get_sorted_supported_symbols', 'automata.symbol.symbol_base.ISymbolProvider', 'automata.memory_store.symbol_doc_embedding_handler.SymbolDocEmbeddingHandler']


Best Match: automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler._get_sorted_supported_symbols



Example 2
----------

Search Query: Which method generates a tool evaluation result?

- Observed Results - 
o
Top 10 Search Results: ['automata.eval.tool.tool_eval.ToolEval', 'automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics', 'automata.eval.tool.tool_eval.ToolEvalResult', 'automata.eval.tool.tool_eval_harness.ToolEvaluationHarness', 'automata.eval.tool.tool_eval_harness.ToolEvaluationHarness.__init__', 'automata.cli.commands.run_tool_eval', 'automata.eval.tool.tool_eval.ToolEval.generate_eval_result', 'automata.eval.tool.search_eval.SymbolSearchEval', 'automata.experimental.tools.builders.advanced_context_oracle_builder.AdvancedContextOracleToolkitBuilder.build', 'automata.eval.tool.tool_eval_harness.ToolEvaluationHarness.evaluate']

Best Match: automata.eval.tool.tool_eval.ToolEval.generate_eval_result


Example 3
----------


Search Query: What property is used to retrieve the total number of partial matches?

- Observed Results - 

Top 10 Search Results: ['automata.eval.agent.agent_eval_metrics.AgentEvaluationMetrics.total_partial_matches', 'automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.total_partial_matches', 'automata.eval.agent.agent_eval_metrics.AgentEvaluationMetrics.total_full_matches', 'automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.total_full_matches', 'automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.partial_match_rate', 'automata.eval.agent.agent_eval_metrics.AgentEvaluationMetrics.partial_match_rate', 'automata.eval.agent.agent_eval.AgentEvalResult.is_partial_match', 'automata.eval.eval_base.EvalResult.is_partial_match', 'automata.eval.tool.search_eval.SymbolSearchEvalResult.is_partial_match', 'automata.eval.agent.agent_eval_metrics.AgentEvaluationMetrics.total_actions']


Best Match: automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.total_partial_matches



Repeat for the following question -

Search Query: {QUERY}

- Observed Results - 

Top 10 Search Results: {SEARCH_RESULTS}

Best Match:"""
)
