"""
Functions to generate spanning trees of a given graph
"""

import itertools
from collections import defaultdict

from .edge import Edge


def is_bridge(i, j, edges):
    """
    Determine whether removing the edge (i, j) would disconnect the graph.

    :param int i
    :param int j
    :param list[Edge] edges: All edges of the graph
    :rtype: bool

    e.g.

    a-b-c-d
    |/
    e

    The edges (b, c) and (c, d) are bridges, since removing either of them
    would split the graph into two separate pieces.

    The edge (a, b) is not a bridge: the graph would still be connected without
    it.
    """
    adjacents = defaultdict(list)

    for edge in edges:
        x, y = edge.vertices
        adjacents[x].append(y)
        adjacents[y].append(x)

    visited = set()

    def _search(x):
        if x == j:
            return True

        visited.add(x)

        for y in adjacents[x]:
            if (x, y) != (i, j) and y not in visited and _search(y):
                return True

        return False

    return not _search(i)


def do_contraction(i, j, vertices, edges):
    """
    Contract vertices i and j: part of Winter's algorithm.

    :param int i
    :param int j: j > i
    :param list[int] vertices: All vertices of the graph
    :param list[Edge] edges: All edges of the graph
    :returns: All graph vertices and edges after the contraction, plus all
    edges that were contracted identified by their original vertex pairs.
    :rtype: (list[int], list[Edge], list[(int, int)])

    Vertex i and the edges that join it to j are deleted and all other edges
    connected to i are connected to j.
    """
    new_vertices = [v for v in vertices if v != i]

    new_edges = []
    contracted_edges = []
    for edge in edges:
        if edge.vertices[0] == i and edge.vertices[1] == j:
            contracted_edges.append(edge.label)
        elif edge.vertices[0] == i:
            new_edge = Edge(edge.label, *sorted((j, edge.vertices[1])))
            new_edges.append(new_edge)
        else:
            new_edges.append(edge)

    return new_vertices, new_edges, contracted_edges


def do_deletion(i, j, edges):
    """
    Delete all edges between i and j: part of Winter's algorithm.

    :param int i
    :param int j: j > i
    :param list[Edge] edges: All edges of the graph

    All edges that join vertices i and j are deleted.
    """
    new_edges = [e for e in edges if e.vertices != (i, j)]

    return new_edges


def generate_all_trees(starting_vertices, starting_edges):
    """
    Recursively generate all spanning trees of a given graph using Winter's
    algorithm (see https://doi.org/10.1007/BF01939361).

    :param list[int] starting_vertices: Labels that wil be used in the output
    :param list[Edge] starting_edges: All edges of the graph
    :returns: Trees in the form of lists of connected vertex pairs
    :rtype: Generator[list[(int, int)]]

    All edges that join vertices i and j are deleted.
    """

    # Starting with the input graph, recursively try contracting and deleting-
    # then-contracting.
    def _recurse(vertices, edges, contractions=None):
        if contractions is None:
            contractions = []

        # The contraction happens at each node until the graph is reduced to a
        # single vertex.
        if len(vertices) == 1:
            yield contractions
            return

        # Vertex i is the first labeled vertex. Vertex j is the first labeled
        # vertex adjacent to vertex i.
        i = vertices[0]
        j = min(e.vertices[1] for e in edges if e.vertices[0] == i)

        v, e, contraction = do_contraction(i, j, vertices, edges)
        yield from _recurse(v, e, contractions + [contraction])

        # The elimination of edges that connect vertices i and j happens only
        # if it does not disconnect the graph.
        if not is_bridge(i, j, edges):
            e = do_deletion(i, j, edges)
            yield from _recurse(vertices, e, contractions)

    # The contracted edges are stored in sequences, which correspond to the
    # paths between the root node and the leaves of the created binary tree.
    contraction_sequences = _recurse(starting_vertices, starting_edges)

    # From these sequences we may retrieve the possible spanning trees of G.
    for contracted_edges in contraction_sequences:
        yield from itertools.product(*contracted_edges)
