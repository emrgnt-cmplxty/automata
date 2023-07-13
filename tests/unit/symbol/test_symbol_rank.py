import random

import networkx as nx
import pytest
from networkx import DiGraph

from automata.experimental.search import SymbolRank, SymbolRankConfig


@pytest.fixture
def random_graph():
    nodes = 10
    edges = 20
    return generate_random_graph(nodes, edges)


@pytest.fixture
def symbol_rank(random_graph):
    config = SymbolRankConfig()
    return SymbolRank(random_graph, config)


def generate_random_graph(nodes, edges):
    """Generate a directed random graph with specified nodes and edges."""
    graph = nx.DiGraph()
    for i in range(nodes):
        graph.add_node(i)
    for _ in range(edges):
        graph.add_edge(random.randint(0, nodes - 1), random.randint(0, nodes - 1))
    return graph


def test_generate_random_graph():
    nodes = 10
    edges = 20
    G = generate_random_graph(nodes, edges)

    assert G.number_of_nodes() == nodes
    assert G.number_of_edges() <= edges  # It can be less because of randomly identical edges


def test_pagerank_config_validation():
    with pytest.raises(ValueError):
        invalid_config_alpha = SymbolRankConfig(alpha=1.5, max_iterations=100, tolerance=1.0e-5)
        invalid_config_alpha.validate_config(invalid_config_alpha)
    with pytest.raises(ValueError):
        invalid_config_tolerance = SymbolRankConfig(
            alpha=0.5, max_iterations=100, tolerance=1.0e-3
        )
        invalid_config_tolerance.validate_config(invalid_config_tolerance)


def test_prepare_initial_ranks(random_graph, symbol_rank):
    initial_ranks = symbol_rank._prepare_initial_ranks(random_graph, None)
    assert len(initial_ranks) == random_graph.number_of_nodes()
    assert sum(initial_ranks.values()) == pytest.approx(1.0)



def test_get_ranks(random_graph, symbol_rank):
    ranks = symbol_rank.get_ranks()
    assert len(ranks) == random_graph.number_of_nodes()
    assert sum(ele[1] for ele in ranks) == pytest.approx(1.0)


def test_get_ranks_small_graph():
    G = DiGraph()
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    config = SymbolRankConfig()
    pagerank = SymbolRank(G, config)

    ranks = pagerank.get_ordered_ranks()
    assert len(ranks) == 3
    assert sum(ele[1] for ele in ranks) == pytest.approx(1.0)
