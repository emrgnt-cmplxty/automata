"""Module containing functions to build SymbolDocEmbedding objects."""
from typing import List, Set

from automata.symbol import ISymbolProvider, Symbol


class SymbolProviderRegistry:
    """A class for registering and tracking `ISymbolProvider` instances."""

    _providers: Set[ISymbolProvider] = set([])
    sorted_supported_symbols: List[Symbol] = []

    @staticmethod
    def register_provider(provider: ISymbolProvider) -> None:
        """Registers a symbol provider."""

        provider.set_synchronized(False)
        SymbolProviderRegistry._providers.add(provider)

    @staticmethod
    def synchronize() -> None:
        """
        Synchronizes all symbol providers.
        As part of the synchronization process, each provider has
        their synchronized status set True and their supported symbols
        filtered to only include symbols that are supported by all providers.
        """

        all_symbols = [
            set(provider._get_sorted_supported_symbols())
            for provider in SymbolProviderRegistry._providers
        ]
        supported_symbols = set.intersection(*all_symbols)
        if not supported_symbols:
            raise RuntimeError(
                f"Symbol overlap across {SymbolProviderRegistry._providers} is empty."
            )

        sorted_supported_symbols = sorted(
            list(supported_symbols), key=lambda x: x.dotpath
        )

        for provider in SymbolProviderRegistry._providers:
            provider.filter_symbols(sorted_supported_symbols)
            provider.set_synchronized(True)

        SymbolProviderRegistry.sorted_supported_symbols = (
            sorted_supported_symbols
        )

    @staticmethod
    def get_sorted_supported_symbols() -> List[Symbol]:
        """Returns a list of all supported symbols."""

        if not SymbolProviderRegistry.sorted_supported_symbols:
            SymbolProviderRegistry.synchronize()

        return SymbolProviderRegistry.sorted_supported_symbols

    @staticmethod
    def reset() -> None:
        """Resets the registry."""

        SymbolProviderRegistry._providers = set([])
        SymbolProviderRegistry.sorted_supported_symbols = []


class SymbolProviderSynchronizationContext:
    """A context manager for synchronizing symbol providers."""

    def __init__(self):
        self._was_synchronized = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._was_synchronized:
            raise RuntimeError(
                "Must synchronize symbol providers in synchronization context"
            )

    def register_provider(self, provider: ISymbolProvider) -> None:
        """Registers a symbol provider."""

        SymbolProviderRegistry.register_provider(provider)
        self._was_synchronized = False

    def synchronize(self) -> None:
        """Synchronizes all symbol providers."""

        SymbolProviderRegistry.synchronize()
        self._was_synchronized = True
