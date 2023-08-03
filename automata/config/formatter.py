from typing import TYPE_CHECKING, Dict

from automata.config.config_base import AgentConfig, AgentConfigName

if TYPE_CHECKING:
    from automata.experimental.search import SymbolRank


class TemplateFormatter:
    @staticmethod
    def create_default_formatter(
        config: AgentConfig,
        symbol_rank: "SymbolRank",
        max_default_overview_symbols: int = 10,
    ) -> Dict[str, str]:
        formatter: Dict[str, str] = {}
        if config.config_name == AgentConfigName.AUTOMATA_MAIN:
            top_symbols = symbol_rank.get_top_symbols(
                max_default_overview_symbols
            )
            formatter["symbol_rank_overview"] = "\n".join(
                f"{symbol}"
                for symbol, _ in sorted(
                    top_symbols, key=lambda x: x[1], reverse=True
                )
            )
            # TODO - Why are we duplicating max_tokens calculation?
            # This should be cleaned up.
            formatter["max_iterations"] = str(config.max_iterations)
            formatter["max_tokens"] = str(
                int(config.abs_max_tokens * config.max_token_percentage)
            )

        return formatter
