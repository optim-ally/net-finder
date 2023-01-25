#include "helpers.h"
#include <iostream>

using namespace std;
 
void rotate_array(int arr[], const int shift, const int size)
{
    vector<int> temp;

    for (int i = shift; i < size; ++i)
    {
        temp.push_back(arr[i]);
    }

    for (int i = 0; i < shift; ++i)
    {
        temp.push_back(arr[i]);
    }

    // copy temp back into `arr'
    for (int i = 0; i < size; ++i)
    {
        arr[i] = temp[i];
    }
}
