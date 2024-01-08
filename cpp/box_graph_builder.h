#ifndef BOX_GRAPH_BUILDER_H
#define BOX_GRAPH_BUILDER_H

#include <algorithm>
#include <numeric>
#include <random>
#include <unordered_map>

#include "net_helpers.h"
#include "box_graph_builder.h"

using namespace std;

pair<vector<Face>, EdgeSet> build_box_graph(
    const int, const int, const int, bool = false
);

#endif
