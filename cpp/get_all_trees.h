#ifndef GET_ALL_TREES_H
#define GET_ALL_TREES_H

#include <algorithm>
#include <functional>
#include <limits.h>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "edge.h"

bool is_bridge(const int, const int, EdgeSet&);

tuple<vector<int>, EdgeSet, vector<pair<int, int>>> do_contraction(
    const int, const int, vector<int>&, EdgeSet&
);

EdgeSet do_deletion(const int, const int, EdgeSet&);

void generate_all_trees(
    vector<int>&, EdgeSet&, function<bool (vector<pair<int, int>>&)>
);

#endif
