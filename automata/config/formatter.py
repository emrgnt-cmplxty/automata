from typing import TYPE_CHECKING, Dict

from automata.config.base import AgentConfig, AgentConfigName

if TYPE_CHECKING:
    from automata.experimental.search import SymbolRank


class TemplateFormatter:
    @staticmethod
    def create_default_formatter(
        config: AgentConfig,
        symbol_rank: "SymbolRank",
        max_default_overview_symbols: int = 100,
    ) -> Dict[str, str]:
        """
        TODO:
            - Re-implement this method after the new instruction configs are finalized.
        """
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
            formatter["max_iterations"] = str(config.max_iterations)
        elif config.config_name != AgentConfigName.TEST:
            raise NotImplementedError(
                "Automata does not have a default template formatter."
            )

        return formatter
