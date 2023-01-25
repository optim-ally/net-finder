#ifndef HELPERS_H
#define HELPERS_H

#include <utility>
#include <vector>

using namespace std;

struct pair_hash {
    size_t operator () (const pair<int, int> &p) const {
        return p.first * 31 + p.second;  
    }
};

void rotate_array(int[], const int, const int);

#endif
