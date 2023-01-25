#include <iostream>
#include <fstream>
#include <functional>
#include <thread>
#include <vector>

#include "box_graph_builder.h"
#include "get_all_trees.h"
#include "net_helpers.h"

using namespace std;

// Smallest possible 3 boxes with common development (area = 46):
// 1 x 1 x 11
// 1 x 2 x 7
// 1 x 3 x 5

int main()
{
    pair<vector<Face>, EdgeSet> box_graph_A = build_box_graph(1, 1, 11);
    pair<vector<Face>, EdgeSet> box_graph_B = build_box_graph(1, 2, 7);
    pair<vector<Face>, EdgeSet> box_graph_C = build_box_graph(1, 3, 5);

    function<bool (Matrix&)> try_net = [&] (Matrix &net)
    {
        const bool is_net_of_B = check_net(net, box_graph_B.first);
        const bool is_net_of_C = check_net(net, box_graph_C.first);

        if (is_net_of_B || is_net_of_C)
        {
            ofstream file;

            // open file in 'append' mode (creates if does not exist)
            file.open("results.txt", ios_base::app);
            file << "\n--------------------\n";

            for (vector<int> &row : net)
            {
                for (int i : row)
                {
                    file << (i ? "[]" : "  ");
                }
                file << "\n";
            }

            if (is_net_of_B)
            {
                file << "\nCommon development with (1, 2, 7)\n";
            }
            if (is_net_of_C)
            {
                file << "\nCommon development with (1, 3, 5)\n";
            }
        }

        return is_net_of_B && is_net_of_C;
    };

    function<bool (int[11], Matrix&)> try_offsets = [&] (
        const int offsets[11],
        Matrix &net
    )
    {
        // Matrix net(13, vector<int>(70));
        for (vector<int> &row : net)
        {
            fill(row.begin(), row.end(), 0);
        }

        const int start = 30;
        int cumulative_offset = start;

        net[0][start] = 1;

        for (int row = 0; row < 11; ++row)
        {
            const int offset = offsets[row];
            cumulative_offset += offset;

            for (int col = 0; col < 4; ++col)
            {
                const int index = col + cumulative_offset;
                net[row + 1][index] = 1;
            }
        }

        net[12][cumulative_offset] = 1;

        // check if net is valid
        return try_net(net);
    };

    bool is_done = false;

    function<void (int, int, int, int, int, int, int)> try_first_7_offsets = [&] (
        int off_1, int off_2, int off_3, int off_4, int off_5, int off_6, int off_7
    )
    {
        Matrix net(13, vector<int>(70));

        for (int off_8 = -3; off_8 < 4; ++off_8)
        {
            for (int off_9 = -3; off_9 < 4; ++off_9)
            {
                for (int off_10 = -3; off_10 < 4; ++off_10)
                {
                    int offsets[11]{
                        0, off_1, off_2, off_3, off_4, off_5,
                        off_6, off_7, off_8, off_9, off_10
                    };

                    if (try_offsets(offsets, net))
                    {
                        is_done = true;
                    }

                    if (is_done) break;
                }
                if (is_done) break;
            }
            if (is_done) break;
        }
    };

    for (int off_1 = -3; off_1 < 4; ++off_1)
    {
        for (int off_2 = -3; off_2 < 4; ++off_2)
        {
            for (int off_3 = -3; off_3 < 4; ++off_3)
            {
                ofstream file;
                file.open("results.txt", ios_base::app);
                file << off_1 << "." << off_2 << "." << off_3
                    << ".x.x.x.x.x.x.x.x\n";
                file.close();

                for (int off_4 = -3; off_4 < 4; ++off_4)
                {
                    for (int off_5 = -3; off_5 < 4; ++off_5)
                    {
                        cout << off_1 << "." << off_2 << "." << off_3 << "."
                            << off_4 << "." << off_5 << ".x.x.x.x.x\n";

                        vector<std::thread> threads;

                        for (int off_6 = -3; off_6 < 4; ++off_6)
                        {
                            for (int off_7 = -3; off_7 < 4; ++off_7)
                            {
                                threads.push_back(
                                    thread(
                                        try_first_7_offsets,
                                        off_1, off_2, off_3, off_4,
                                        off_5, off_6, off_7
                                    )
                                );

                                if (is_done) break;
                            }
                            if (is_done) break;
                        }

                        for (thread &th : threads)
                        {
                            th.join();
                        }

                        if (is_done) break;
                    }
                    if (is_done) break;
                }
                if (is_done) break;
            }
            if (is_done) break;
        }
        if (is_done) break;
    }
    
    return 0;
}