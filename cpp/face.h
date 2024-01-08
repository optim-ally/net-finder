#ifndef FACE_H
#define FACE_H

#include <iostream>

using namespace std;

class Face {
  public:
    int adjacents[4];

    Face(int[4]);

    void orient(int, int);
};

ostream& operator<<(ostream&, const Face&);

#endif
