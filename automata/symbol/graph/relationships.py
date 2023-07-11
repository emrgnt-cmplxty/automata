import logging
from typing import Any

import networkx as nx
from google.protobuf.json_format import MessageToDict  # type: ignore

from automata.symbol.graph.base import GraphProcessor
from automata.symbol.parser import parse_symbol

logger = logging.getLogger(__name__)


class RelationshipProcessor(GraphProcessor):
    """Adds edges to the `MultiDiGraph` for relationships between `Symbol` nodes."""

    def __init__(self, graph: nx.MultiDiGraph, symbol_information: Any) -> None:
        self._graph = graph
        self.symbol_information = symbol_information

    def process(self) -> None:
        """
        Adds edges in the local `MultiDiGraph` for relationships between `Symbol` nodes.
        Two `Symbols` are related if they share an inheritance relationship.
        See below for example - the `Dog` class inherits from the `Animal` class,
        so the `Dog` class is related to the `Animal` class.
        When resolving "Find references", this field documents what other symbols
        should be included together with this symbol. For example, consider the
        following TypeScript code that defines two symbols `Animal#sound()` and
        `Dog#sound()`:
        ```ts
        interface Animal {
                  ^^^^^^ definition Animal#
          sound(): string
          ^^^^^ definition Animal#sound()
        }
        class Dog implements Animal {
              ^^^ definition Dog#, relationships = [{symbol: "Animal#", is_implementation: true}]
          public sound(): string { return "woof" }
                 ^^^^^ definition Dog#sound(), references_symbols = Animal#sound(), relationships = [{symbol: "Animal#sound()", is_implementation:true, is_reference: true}]
        }
        const animal: Animal = new Dog()
                      ^^^^^^ reference Animal#
        console.log(animal.sound())
                           ^^^^^ reference Animal#sound()
        ```
        Doing "Find references" on the symbol `Animal#sound()` should return
        references to the `Dog#sound()` method as well. Vice-versa, doing "Find
        references" on the `Dog#sound()` method should include references to the
        `Animal#sound()` method as well.
        """
        for relationship in self.symbol_information.relationships:
            relationship_labels = MessageToDict(relationship)
            relationship_labels.pop("symbol")
            related_symbol = parse_symbol(relationship.symbol)
            self._graph.add_edge(
                self.symbol_information.symbol,
                related_symbol,
                label="relationship",
                **relationship_labels,
            )
