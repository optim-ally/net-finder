#include "net_helpers.h"

using namespace std;

typedef unordered_set<pair<int, int>, pair_hash> PairSet;

Matrix create_net(vector<pair<int, int>> &tree, vector<Face> &faces)
{
    // Build a net from a spanning tree of a box.

    // tree: Edges of a spanning tree (index into `faces`)
    // faces: The adjacent faces of the box with orientations
    // returns a 2-dimensional vector representing a bitmap of the net
    const int total_faces = tree.size();

    PairSet edges(tree.begin(), tree.end());

    vector<vector<int>> net(2 * total_faces, vector<int>(2 * total_faces, 0));

    unordered_set<int> visited;

    function<bool (int)> is_visited = [&] (const int face_index)
    {
        return visited.find(face_index) != visited.end();
    };

    function<bool (int, int)> is_connected = [&] (const int i, const int j)
    {
        return (
            (edges.find(pair<int, int>(i, j)) != edges.end()) ||
            (edges.find(pair<int, int>(j, i)) != edges.end())
        );
    };

    function<void (int, int, int)> grow_net = [&] (
        const int face_index, const int i, const int j
    )
    {
        net[i][j] += 1;
        visited.insert(face_index);

        for (int dir = 0; dir < 4; ++dir)
        {
            const int adjacent = faces[face_index].adjacents[dir];

            if (!is_visited(adjacent) && is_connected(face_index, adjacent))
            {
                Face face = faces[adjacent];
                const int x_change = directions[dir].first;
                const int y_change = directions[dir].second;

                const int opposite_direction = (dir + 2) % 4;
                face.orient(face_index, opposite_direction);

                grow_net(adjacent, i + x_change, j + y_change);
            }
        }
    };

    grow_net(0, total_faces, total_faces);

    return remove_zero_rows_columns(net);
}

bool check_net(Matrix &net, vector<Face> &faces)
{
    // Decide whether a net is a net of a box.

    // net: Bitmap of the net
    // faces: The adjacent faces of the box with orientations
    // returns whether or not the net is a net of the box

    if (net.size() == 0)
    {
        return faces.size() == 0;
    }

    const int total_faces = faces.size();

    int net_size = 0;
    for (vector<int> &row : net)
    {
        for (int i : row)
        {
            net_size += i;
        }
    }

    if (net_size != total_faces)
    {
        return false;
    }

    const int H = net.size();
    const int W = net[0].size();

    function<bool (int, int)> is_in_net = [&] (const int i, const int j)
    {
        return i >= 0 && j >= 0 && i < H && j < W && net[i][j] > 0;
    };

    function<bool (int, int, int)> check_net_at_position = [&] (
        const int start_i, const int start_j, const int rotation
    )
    {
        if (!is_in_net(start_i, start_j))
        {
            return false;
        }

        unordered_set<int> visited = {};

        function<bool (int)> is_visited = [&] (const int face_index)
        {
            return visited.find(face_index) != visited.end();
        };

        function<bool (int, int, int)> follow_net = [&] (
            const int face_index, const int i, const int j
        )
        {
            if (is_visited(face_index))
            {
                return false;
            }

            visited.insert(face_index);

            for (int dir = 0; dir < 4; ++dir)
            {
                const int adjacent = faces[face_index].adjacents[dir];
                const int x_change = directions[dir].first;
                const int y_change = directions[dir].second;
                const int new_i = i + x_change;
                const int new_j = j + y_change;

                if (is_in_net(new_i, new_j) && !is_visited(adjacent))
                {
                    Face &face = faces[adjacent];

                    const int opposite_direction = (dir + 2) % 4;
                    face.orient(face_index, opposite_direction);

                    if (!follow_net(adjacent, new_i, new_j))
                    {
                        return false;
                    }
                }
            }

            return true;
        };

        faces[0].orient(faces[0].adjacents[0], rotation);

        return (
            follow_net(0, start_i, start_j) &&
            (visited.size() == total_faces)
        );
    };

    // Try placing the first face of the the box at each position in the net
    // in all 4 orientations then recursively trying to reach all other faces
    // via adjacent net squares.
    for (int direction = 0; direction < 4; ++direction)
    {
        for (int i = 0; i < net.size(); ++i)
        {
            for (int j = 0; j < net[0].size(); ++j)
            {
                if (check_net_at_position(i, j, direction))
                {
                    return true;
                }
            }
        }
    }

    return false;
}
