"""
Module defining the 'Edge' dataclass
"""
from collections import namedtuple


class Edge(namedtuple('Edge', ['label', 'vertices'])):

    """Edge class for storing graph data"""

    label: str
    vertices: tuple[int]

    __slots__ = ()

    def __new__(cls, label, i, j):
        return super(Edge, cls).__new__(cls, label, (i, j))
