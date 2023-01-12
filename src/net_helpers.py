import copy

from src.matrix_helpers import mirror, remove_zero_rows_columns, rotate_90


# Directions:
#     0
#     ^
#     |
# 3 <-+-> 1
#     |
#     v
#     2
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def create_net(tree, faces) -> tuple[tuple[int]]:
    """
    Build a net from a spanning tree of a box.

    :param list((int, int)) tree: Edges of a spanning tree (index into `faces`)
    :param list(Face) faces: The adjacent faces of the box with orientations
    :return: 2-dimensional tuple, bitmap of net
    :rtype: tuple(tuple(int))
    """
    total_faces = len(tree)
    edges = set(tree)

    net = [
        [0] * 2 * total_faces
        for _ in range(2 * total_faces)
    ]
    visited = set()

    def grow_net(face_index, i, j):
        net[i][j] += 1
        visited.add(face_index)

        for direction, adjacent_face in enumerate(faces[face_index].adjacents):
            if (
                adjacent_face not in visited and
                tuple(sorted((face_index, adjacent_face))) in edges
            ):
                face = faces[adjacent_face]
                x_change, y_change = directions[direction]

                opposite_direction = (direction + 2) % 4
                face.orient(face_index, opposite_direction)

                grow_net(adjacent_face, i + x_change, j + y_change)

    grow_net(0, total_faces, total_faces)

    trimmed = remove_zero_rows_columns(net)
    mirrored = mirror(trimmed)
    best = min(trimmed, mirrored)

    for matrix in (trimmed, mirrored):
        for _ in range(3):
            rotated = rotate_90(matrix)

            if rotated < best:
                best = rotated

            matrix = rotated

    return tuple(tuple(row) for row in best)


def check_net(net, faces) -> bool:
    """
    Decide whether a net is a net of a box.

    :param tuple(tuple(int)) net: Bitmap of the net
    :param list(Face) faces: The adjacent faces of the box with orientations
    :return: Whether or not the net is a net of the box
    :rtype: bool
    """
    if len(net) == 0:
        return len(faces == 0)

    faces = copy.deepcopy(faces)
    
    H = len(net)
    W = len(net[0])

    total_faces = sum(sum(row) for row in net)

    def is_in_net(i, j):
        return i >= 0 and j >= 0 and i < H and j < W and net[i][j] > 0

    def check_net_at_position(start_i, start_j):
        if not is_in_net(start_i, start_j):
            return False

        visited = set()

        def follow_net(face_index, i, j):
            if face_index in visited:
                return False

            visited.add(face_index)

            for direction, adjacent in enumerate(faces[face_index].adjacents):
                x_change, y_change = directions[direction]
                new_i = i + x_change
                new_j = j + y_change

                if is_in_net(new_i, new_j) and adjacent not in visited:
                    face = faces[adjacent]

                    opposite_direction = (direction + 2) % 4
                    face.orient(face_index, opposite_direction)

                    if not follow_net(adjacent, new_i, new_j):
                        return False

            return True

        return follow_net(0, start_i, start_j) and len(visited) == total_faces

    # Try placing the first face of the the box at each position in the net
    # in all 4 orientations then recursively trying to reach all other faces
    # via adjacent net squares.
    for direction in range(4):
        # Twist the net 90 degrees for each new direction.
        if direction != 0:
            net = rotate_90(net)
            H, W = W, H

        for i in range(len(net)):
            for j in range(len(net[0])):
                if check_net_at_position(i, j):
                    return True

    return False
