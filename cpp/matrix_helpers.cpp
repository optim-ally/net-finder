#include "matrix_helpers.h"

using namespace std;

Matrix remove_zero_rows_columns(const Matrix &matrix)
{
    const int height = matrix.size();
    const int width = (height > 0) ? matrix[0].size() : 0;

    if (height == 0 || width == 0)
    {
        return matrix;
    }

    int min_x = height - 1;
    int max_x = 0;
    int min_y = width - 1;
    int max_y = 0;

    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            if (matrix[i][j])
            {
                if (i < min_x)
                {
                    min_x = i;
                }
                if (i > max_x)
                {
                    max_x = i;
                }
                if (j < min_y)
                {
                    min_y = j;
                }
                if (j > max_y)
                {
                    max_y = j;
                }
            }
        }
    }

    Matrix result;

    for (int i = min_x; i <= max_x; ++i)
    {
        vector<int> row;

        for (int j = min_y; j <= max_y; ++j)
        {
            row.push_back(matrix[i][j]);
        }

        result.push_back(row);
    }

    return result;
}

Matrix mirror(Matrix &matrix)
{
    const int height = matrix.size();
    const int width = (height > 0) ? matrix[0].size() : 0;

    if (height == 0 || width == 0)
    {
        return matrix;
    }

    Matrix result;

    for (int i = 0; i < height; ++i)
    {
        vector<int> row;

        for (int j = width - 1; j >= 0; --j)
        {
            row.push_back(matrix[i][j]);
        }

        result.push_back(row);
    }
}

Matrix rotate_90(Matrix &matrix)
{
    const int height = matrix.size();
    const int width = (height > 0) ? matrix[0].size() : 0;

    if (height == 0 || width == 0)
    {
        return matrix;
    }

    Matrix result;

    for (int j = width - 1; j >= 0; --j)
    {
        vector<int> row;

        for (int i = 0; i < height; ++i)
        {
            row.push_back(matrix[i][j]);
        }

        result.push_back(row);
    }

    return result;
}
