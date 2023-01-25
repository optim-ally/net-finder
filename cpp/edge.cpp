#include <utility>

#include "edge.h"

using namespace std;

Edge::Edge(pair<int, int> edge_label, int i, int j)
    : label(edge_label)
    , start(i)
    , end(j)
{};

bool Edge::operator==(const Edge &rhs) const
{
    return label == rhs.label;
};
