#ifndef EDGE_H
#define EDGE_H

#include <unordered_set>
#include <utility>

using namespace std;

class Edge {
  public:
    pair<int, int> label;
    int start;
    int end;

    Edge(pair<int, int>, int, int);

    bool operator==(const Edge&) const;
};

struct edge_hash {
    size_t operator () (const Edge &edge) const {
        return edge.start * 100 + edge.end;  
    }
};

typedef unordered_set<Edge, edge_hash> EdgeSet;

#endif
