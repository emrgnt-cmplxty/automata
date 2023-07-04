from automata.core.symbol.base import Symbol, ISymbolProvider
from typing import List, Type, Set


class SymbolProviderRegistry:
    _providers: Set[ISymbolProvider] = set([])
    supported_symbols: List[Symbol] = []

    @staticmethod
    def register_provider(provider: ISymbolProvider):
        provider.set_synchronized(False)
        SymbolProviderRegistry._providers.add(provider)
        return provider

    @staticmethod
    def synchronize():
        all_symbols = [
            set(provider._get_all_supported_symbols())
            for provider in SymbolProviderRegistry._providers
        ]
        supported_symbols = set.intersection(*all_symbols)
        for provider in SymbolProviderRegistry._providers:
            provider.filter_symbols(supported_symbols)
            provider.set_synchronized(True)

        SymbolProviderRegistry.supported_symbols = list(supported_symbols)

        if not SymbolProviderRegistry.supported_symbols:
            raise RuntimeError("No symbols are supported by any symbol provider")

    @staticmethod
    def get_all_supported_symbols():
        if not SymbolProviderRegistry.supported_symbols:
            SymbolProviderRegistry.synchronize()
        return SymbolProviderRegistry.supported_symbols


class SymbolProviderSynchronizationContext:
    def __init__(self):
        self._was_synchronized = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._was_synchronized:
            raise RuntimeError("Must synchronize symbol providers in synchronization context")

    def register_provider(self, provider: ISymbolProvider):
        SymbolProviderRegistry.register_provider(provider)
        self._was_synchronized = False

    def synchronize(self):
        SymbolProviderRegistry.synchronize()
        self._was_synchronized = True
