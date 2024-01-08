#include "get_all_trees.h"

bool is_bridge(const int i, const int j, EdgeSet &edges)
{
    unordered_map<int, vector<int>> adjacents;

    for (const Edge &edge : edges)
    {
        const int x = edge.start;
        const int y = edge.end;

        adjacents[x].push_back(y);
        adjacents[y].push_back(x);
    }

    unordered_set<int> visited;

    function<bool (int)> is_visited = [&] (const int face_index)
    {
        return visited.find(face_index) != visited.end();
    };

    function<bool (int)> search = [&] (const int x)
    {
        if (x == j)
        {
            return true;
        }

        visited.insert(x);

        for (int y : adjacents[x])
        {
            if ((x != i) && (y != j) && !is_visited(y) && search(y))
            {
                return true;
            }
        }

        return false;
    };

    return !search(i);
}

tuple<vector<int>, EdgeSet, vector<pair<int, int>>> do_contraction(
    const int i, const int j, vector<int> &vertices, EdgeSet &edges
)
{
    // Assuming i < j. Vertex i and the edges that join it to j are deleted
    // and all edges connected to i are connected to j.
    vector<int> new_vertices;

    for (int v : vertices)
    {
        if (v != i)
        {
            new_vertices.push_back(v);
        }
    }

    EdgeSet new_edges;
    vector<pair<int, int>> contracted_edges;

    for (const Edge &edge : edges)
    {
        if (edge.start == i && edge.end == j)
        {
            contracted_edges.push_back(edge.label);
        }
        else if (edge.start == i)
        {
            Edge new_edge = Edge(
                edge.label, min(j, edge.end), max(j, edge.end)
            );
            new_edges.insert(new_edge);
        }
        else
        {
            new_edges.insert(edge);
        }
    }

    return tuple<vector<int>, EdgeSet, vector<pair<int, int>>>
    (
        new_vertices, new_edges, contracted_edges
    );
}

EdgeSet do_deletion(const int i, const int j, EdgeSet &edges)
{
    // Assuming i < j. All edges that join vertices i and j are deleted.
    EdgeSet new_edges;

    for (const Edge &edge : edges)
    {
        if ((edge.start != i) || (edge.end != j))
        {
            new_edges.insert(edge);
        }
    }

    return new_edges;
}

void generate_all_trees(
    vector<int> &starting_vertices,
    EdgeSet &starting_edges,
    function<bool (vector<pair<int, int>>&)> callback
)
{
    // Uses Winter's algorithm

    // Starting with the input graph, recursively try contracting and deleting-
    // then-contracting.
    function<bool (
        vector<int>&, EdgeSet&, vector<vector<pair<int, int>>>&
    )> recurse = [&](
        vector<int> &vertices,
        EdgeSet &edges,
        vector<vector<pair<int, int>>> &contractions
    )
    {
        // The contraction happens at each node until the graph is reduced to a
        // single vertex.
        if (vertices.size() == 1)
        {
            // The contracted edges are stored in sequences, which correspond
            // to the paths between the root node and the leaves of the created
            // binary tree.

            // From these sequences we may retrieve the possible spanning trees
            // of G.
            // TODO : need to apply callback on each product el of contractions
            // return callback(contractions);
        }

        // Vertex i is the first labeled vertex. Vertex j is the first labeled
        // vertex adjacent to vertex i.
        const int i = vertices[0];
        int j = INT_MAX;

        for (const Edge &edge : edges)
        {
            if (edge.start == i)
            {
                j = min(j, edge.end);
            }
        }

        vector<int> v;
        EdgeSet e;
        vector<pair<int, int>> contraction;
        
        tie(v, e, contraction) = do_contraction(i, j, vertices, edges);

        vector<vector<pair<int, int>>> new_contractions(contractions);
        new_contractions.push_back(contraction);
        
        if (recurse(v, e, new_contractions))
        {
            return true;
        }

        // The elimination of edges that connect vertices i and j happens only
        // if it does not disconnect the graph.
        if (!is_bridge(i, j, edges))
        {
            EdgeSet new_edges = do_deletion(i, j, edges);

            if (recurse(vertices, new_edges, contractions))
            {
                return true;
            }
        }
    };

    vector<vector<pair<int, int>>> starting_contractions;

    recurse(starting_vertices, starting_edges, starting_contractions);
}
