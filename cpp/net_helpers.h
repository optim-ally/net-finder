#ifndef NET_HELPERS_H
#define NET_HELPERS_H

#include <functional>
#include <numeric>
#include <unordered_set>

#include "edge.h"
#include "face.h"
#include "helpers.h"
#include "matrix_helpers.h"

using namespace std;

// Directions:
//     0
//     ^
//     |
// 3 <-+-> 1
//     |
//     v
//     2
const pair<int, int> directions[4] = {
    {-1, 0}, {0, 1}, {1, 0}, {0, -1}
};

Matrix create_net(vector<pair<int, int>> &tree, vector<Face> &faces);

bool check_net(Matrix &net, vector<Face> &faces);

#endif
