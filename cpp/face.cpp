#include <algorithm>
#include <iostream>
#include <iterator>

#include "face.h"
#include "helpers.h"

using namespace std;

Face::Face(int adjacents_clockwise[4])
{
    for (int i = 0; i < 4; ++i)
    {
        adjacents[i] = adjacents_clockwise[i];
    }
}

void Face::orient(const int adjacent_face, const int direction)
{
    int* index = find(begin(adjacents), end(adjacents), adjacent_face);

    if (index != end(adjacents))
    {
        const int actual_index = distance(adjacents, index);
        const int desired_index = direction;
        const int shift = (actual_index - desired_index + 4) % 4;

        rotate_array(adjacents, shift, 4);
    }
    else
    {
        cout << "Failed to orient: adjacent face not recognised";
    }
};

ostream& operator<<(ostream& s, const Face& face)
{
    for (int adjacent : face.adjacents)
    {
        s << adjacent << " ";
    }

    return s;
}
