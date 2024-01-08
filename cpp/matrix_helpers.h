#ifndef MATRIX_HELPERS_H
#define MATRIX_HELPERS_H

#include <vector>

using namespace std;

typedef vector<vector<int>> Matrix;

Matrix remove_zero_rows_columns(const Matrix&);

Matrix mirror(Matrix&);

Matrix rotate_90(Matrix&);

#endif
