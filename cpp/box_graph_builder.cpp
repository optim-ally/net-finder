#include "box_graph_builder.h"
#include "edge.h"
#include "face.h"

using namespace std;

auto rng = default_random_engine {};

pair<vector<Face>, EdgeSet> build_box_graph(
    const int L, const int H, const int D, bool randomise
)
{
    // Handle surfaces in this orientation
    //                  L
    //             o---------o
    //             |         |
    //           D |   TOP   | D
    //        D    |         |    D
    //   o---------o---------o---------o
    //   |         |         |         |
    // H |  LEFT   |  FRONT  |  RIGHT  | H
    //   |         |         |         |
    //   o---------o---------o---------o
    //        D    |         |    D
    //           D |  BOTTOM | D
    //             |         |
    //             o---------o
    //             |         |
    //           H |   BACK  | H
    //             |         |
    //             o---------o
    //                  L

    unordered_map<int, int> up_map = {};
    unordered_map<int, int> right_map = {};
    unordered_map<int, int> down_map = {};
    unordered_map<int, int> left_map = {};

    vector<Face> faces = {};
    EdgeSet edges = {};
    
    function<void (int, int, int, int, int)> add = [&] (
        const int index,
        const int a, const int b, const int c, const int d
    )
    {
        int adjacents[4] = {a, b, c, d};

        faces.push_back(Face(adjacents));

        for (int other : adjacents)
        {
            if (index < other)
            {
                const pair<int, int> label = pair<int, int>(index, other);
                edges.insert(Edge(label, index, other));
            }
        }
    };

    // Top surface (L x D)
    //     0      1       2   ... L-1
    //     L      L+1     L+2 ... 2L-1
    //     ...
    //     (D-1)L (D-1)L+1    ... DL-1
    for (int i = 0; i < L; ++i)
    {
        for (int j = 0; j < D; ++j)
        {
            const int index = j * L + i;

            if (j > 0)
            {
                up_map[index] = index - L;
            }
            if (i < L - 1)
            {
                right_map[index] = index + 1;
            }
            // down wraps onto front surface
            down_map[index] = index + L;
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    int starting_index = L * D;

    // Front surface (L x H)
    //     DL       DL+1       ... (D+1)L-1
    //     (D+1)L   (D+1)L+1   ... (D+2)L-1
    //     ...
    //     (D+H-1)L (D+H-1)L+1 ... (D+H)L-1
    for (int i = 0; i < L; ++i)
    {
        for (int j = 0; j < H; ++j)
        {
            const int index = starting_index + j * L + i;

            // up wraps onto top surface
            up_map[index] = index - L;
            if (i < L - 1)
            {
                right_map[index] = index + 1;
            }
            // down wraps onto bottom surface
            down_map[index] = index + L;
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    starting_index += L * H;

    // Bottom surface (L x D)
    //     (D+H)L    (D+H)L+1    ... (D+H+1)L-1
    //     (D+H+1)L  (D+H+1)L+1  ... (D+H+2)L-1
    //     ...
    //     (2D+H-1)L (2D+H-1)L+1 ... (2D+H)L-1
    for (int i = 0; i < L; ++i)
    {
        for (int j = 0; j < D; ++j)
        {
            const int index = starting_index + j * L + i;

            // up wraps onto front surface
            up_map[index] = index - L;
            if (i < L - 1)
            {
                right_map[index] = index + 1;
            }
            // down wraps onto back surface
            down_map[index] = index + L;
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    starting_index += L * D;

    // Back surface (L x H)
    //     (2D+H)L    (2D+H)L+1    ... (2D+H+1)L-1
    //     (2D+H+1)L  (2D+H+1)L+1  ... (2D+H+2)L-1
    //     ...
    //     (2D+2H-1)L (2D+2H-1)L+1 ... (2D+2H)L-1
    for (int i = 0; i < L; ++i)
    {
        for (int j = 0; j < H; ++j)
        {
            const int index = starting_index + j * L + i;

            // up wraps onto bottom surface
            up_map[index] = index - L;
            if (i < L - 1)
            {
                right_map[index] = index + 1;
            }
            if (j < H - 1)
            {
                down_map[index] = index + L;
            }
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    starting_index += L * H;

    // Left surface (D x H)
    //     (2D+2H)L        (2D+2H)L+1        ... (2D+2H)L+D-1
    //     (2D+2H)L+D      (2D+2H)L+D+1      ... (2D+2H)L+2D-1
    //     ...
    //     (2D+2H)L+(H-1)D (2D+2H)L+(H-1)D+1 ... (2D+2H)L+HD-1
    for (int i = 0; i < D; ++i)
    {
        for (int j = 0; j < H; ++j)
        {
            const int index = starting_index + j * D + i;

            if (j > 0)
            {
                up_map[index] = index - D;
            }
            if (i < D - 1)
            {
                right_map[index] = index + 1;
            }
            if (j < H - 1)
            {
                down_map[index] = index + D;
            }
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    starting_index += D * H;

    // Right surface (D x H)
    //     (2D+2H)L+HD      (2D+2H)L+HD+1      ... (2D+2H)L+(H+1)D-1
    //     (2D+2H)L+(H+1)D  (2D+2H)L+(H+1)D+1  ... (2D+2H)L+(H+2)D-1
    //     ...
    //     (2D+2H)L+(2H-1)D (2D+2H)L+(2H-1)D+1 ... (2D+2H)L+2HD-1
    for (int i = 0; i < D; ++i)
    {
        for (int j = 0; j < H; ++j)
        {
            const int index = starting_index + j * D + i;

            if (j > 0)
            {
                up_map[index] = index - D;
            }
            if (i < D - 1)
            {
                right_map[index] = index + 1;
            }
            if (j < H - 1)
            {
                down_map[index] = index + D;
            }
            if (i > 0)
            {
                left_map[index] = index - 1;
            }
        }
    }

    // Link front and left surfaces
    //          left     H  front
    //     (2D+2H)L+D-1  | DL
    //     (2D+2H)L+2D-1 | (D+1)L
    //     ...           | ...
    //     (2D+2H)L+HD-1 | (D+H-1)L
    int left_starting_index = (2 * (D + H) * L) + D - 1;

    for (int i = 0; i < H; ++i)
    {
        right_map[left_starting_index + (i * D)] = (D + i) * L;
        left_map[(D + i) * L] = left_starting_index + (i * D);
    }

    // Link front and right surfaces
    //       front  H      right
    //     (D+1)L-1 | (2D+2H)L+HD
    //     (D+2)L-1 | (2D+2H)L+(H+1)D
    //     ...      | ...
    //     (D+H)L-1 | (2D+2H)L+(2H-1)D
    int right_starting_index = (2 * (D + H) * L) + (H * D);

    for (int i = 0; i < H; ++i)
    {
        right_map[((D + i + 1) * L) - 1] = right_starting_index + (i * D);
        left_map[right_starting_index + (i * D)] = ((D + i + 1) * L) - 1;
    }

    // Zip top and back surfaces
    //     back  (2D+2H-1)L (2D+2H-1)L+1 ... (2D+2H)L-1
    //         L --------------------------------------
    //      top  0          1            ... L-1
    int back_starting_index = ((2 * (D + H)) - 1) * L;

    for (int i = 0; i < L; ++i)
    {
        up_map[i] = back_starting_index + i;
        down_map[back_starting_index + i] = i;
    }

    // Zip top and left surfaces
    //                                                top
    //                                            | 0
    //                           D ------------>  | L
    //                           |                | ...
    //                           v                | (D-1)L
    //     ---------------------------------------
    //     (2D+2H)L  (2D+2H)L+1  ...  (2D+2H)L+D-1
    //                        left
    left_starting_index = 2 * (D + H) * L;

    for (int i = 0; i < D; ++i)
    {
        up_map[left_starting_index + i] = i * L;
        left_map[i * L] = left_starting_index + i;
    }

    // Zip top and right surfaces
    //       top                       
    //     L-1  |                
    //     2L-1 |  <-------------------- D              
    //     ...  |                        |
    //     DL-1 |                        v
    //           ------------------------------------------------
    //           (2D+2H)L+HD  (2D+2H)L+HD+1 ... (2D+2H)L+(H+1)D-1
    //                        right
    right_starting_index = (2 * (D + H) * L) + (H * D);

    for (int i = 0; i < D; ++i)
    {
        const int top_index = ((D - i) * L) - 1;

        up_map[right_starting_index + i] = top_index;
        right_map[top_index] = right_starting_index + i;
    }

    // Zip bottom and left surfaces
    //                        left
    //     (2D+2H)L+(H-1)D (2D+2H)L+(H-1)D+1 ... (2D+2H)L+HD-1
    //     ---------------------------------------------------
    //                                ^                       | (D+H)L
    //                                |                       | (D+H+1)L
    //                                D ------------------->  | ...
    //                                                        | (2D+H-1)L
    //                                                          bottom
    left_starting_index = (2 * (D + H) * L) + ((H - 1) * D);

    for (int i = 0; i < D; ++i)
    {
        const int bottom_index = ((2 * D) + H - 1 - i) * L;

        down_map[left_starting_index + i] = bottom_index;
        left_map[bottom_index] = left_starting_index + i;
    }

    // Zip bottom and right surfaces
    //                                        right
    //                 (2D+2H)L+(2H-1)D (2D+2H)L+(2H-1)D+1 ... (2D+2H)L+2HD-1
    //                 ------------------------------------------------------
    //     (D+H+1)L-1 |                          ^                     
    //     (D+H+2)L-1 |                          |                     
    //     ...        |  <---------------------- D
    //     (2D+H)L-1  |                                                 
    //      bottom
    right_starting_index = (2 * (D + H) * L) + (((2 * H) - 1) * D);
    for (int i = 0; i < D; ++i)
    {
        const int bottom_index = ((D + H + 1 + i) * L) - 1;

        down_map[right_starting_index + i] = bottom_index;
        right_map[bottom_index] = right_starting_index + i;
    }

    // Zip back and left surfaces
    //            | (2D+2H)L
    //         -> | (2D+2H)L+D   left
    //       /    | ...
    //      /     | (2D+2H)L+(H-1)D
    //     H    * * *
    //      \     | (2D+H)L
    //       \    | (2D+H+1)L
    //         -> | ...          back
    //            | (2D+2H-1)L
    left_starting_index = 2 * (D + H) * L;
    back_starting_index = (2 * (D + H) * L) - L;

    for (int i = 0; i < H; ++i)
    {
        const int left_index = left_starting_index + (i * D);
        const int back_index = back_starting_index - (i * L);
        left_map[left_index] = back_index;
        left_map[back_index] = left_index;
    }

    // Zip back and right surfaces
    //           (2D+2H)L+(H+1)D-1 |
    //     right (2D+2H)L+(H+2)D-1 | <-
    //           ...               |    \
    //           (2D+2H)L+2HD-1    |     \
    //                           * * *    H
    //           (2D+H+1)L-1       |     /
    //           (2D+H+2)L-1       |    /
    //     back  ...               | <-
    //           (2D+2H)L-1        |
    right_starting_index = (2 * (D + H) * L) + ((H + 1) * D) - 1;
    back_starting_index = (2 * (D + H) * L) - 1;

    for (int i = 0; i < H; ++i)
    {
        const int right_index = right_starting_index + (i * D);
        const int back_index = back_starting_index - (i * L);
        right_map[right_index] = back_index;
        right_map[back_index] = right_index;
    }

    // should now have complete directional maps
    // can build 'Face' instances with all their connections
    const int total_faces = (2 * L * D) + (2 * L * H) + (2 * D * H);

    vector<int> order(total_faces);
    iota(order.begin(), order.end(), 0);

    // if (randomise)
    // {
    //     shuffle(order.begin(), order.end(), rng);
    // }

    unordered_map<int, int[4]> args;

    for (int i = 0; i < total_faces; ++i)
    {
        int new_label = order[i];

        args[new_label][0] = order[up_map[i]];
        args[new_label][1] = order[right_map[i]];
        args[new_label][2] = order[down_map[i]];
        args[new_label][3] = order[left_map[i]];
    }

    for (int i = 0; i < total_faces; ++i)
    {
        add(i, args[i][0], args[i][1], args[i][2], args[i][3]);
    }

    return pair<vector<Face>, EdgeSet>(faces, edges);
}
