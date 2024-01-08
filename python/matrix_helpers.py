def remove_zero_rows_columns(matrix):
    height = len(matrix)
    width = len(matrix[0]) if height else 0

    if height == 0 or width == 0:
        return matrix

    min_x = height - 1
    max_x = 0
    min_y = width - 1
    max_y = 0

    for i in range(height):
        for j in range(width):
            if matrix[i][j]:
                if i < min_x:
                    min_x = i
                if i > max_x:
                    max_x = i
                if j < min_y:
                    min_y = j
                if j > max_y:
                    max_y = j

    return [
        row[min_y : max_y + 1]
        for row in matrix[min_x : max_x + 1]
    ]


def mirror(matrix):
    if len(matrix) == 0:
        return matrix

    return [
        [matrix[i][j] for j in range(len(matrix[0]) - 1, -1, -1)]
        for i in range(len(matrix))
    ]


def rotate_90(matrix):
    if len(matrix) == 0:
        return matrix

    return [
        [matrix[i][j] for i in range(len(matrix))]
        for j in range(len(matrix[0]) - 1, -1, -1)
    ]
