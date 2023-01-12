import random

from src.face import Face
from src.get_all_trees import Edge


def build_box_graph(L, H, D, randomise=False):
    # Handle surfaces in this orientation
    #                  L
    #             o---------o
    #             |         |
    #           D |   TOP   | D
    #        D    |         |    D
    #   o---------o---------o---------o
    #   |         |         |         |
    # H |  LEFT   |  FRONT  |  RIGHT  | H
    #   |         |         |         |
    #   o---------o---------o---------o
    #        D    |         |    D
    #           D |  BOTTOM | D
    #             |         |
    #             o---------o
    #             |         |
    #           H |   BACK  | H
    #             |         |
    #             o---------o
    #                  L

    up_map = {}
    right_map = {}
    down_map = {}
    left_map = {}

    faces = []
    edges = set()
    
    def _add(index, a, b, c, d):
        faces.append(Face((a, b, c, d)))

        for other in (a, b, c, d):
            if index < other: 
                edges.add(Edge((index, other), index, other))

    ## Top surface (L x D)
    #     0      1       2   ... L-1
    #     L      L+1     L+2 ... 2L-1
    #     ...
    #     (D-1)L (D-1)L+1    ... DL-1
    for i in range(L):
        for j in range(D):
            index = j * L + i

            if j > 0:
                up_map[index] = index - L
            if i < L - 1:
                right_map[index] = index + 1
            # down wraps onto front surface
            down_map[index] = index + L
            if i > 0:
                left_map[index] = index - 1

    starting_index = L * D

    ## Front surface (L x H)
    #     DL       DL+1       ... (D+1)L-1
    #     (D+1)L   (D+1)L+1   ... (D+2)L-1
    #     ...
    #     (D+H-1)L (D+H-1)L+1 ... (D+H)L-1
    for i in range(L):
        for j in range(H):
            index = starting_index + j * L + i

            # up wraps onto top surface
            up_map[index] = index - L
            if i < L - 1:
                right_map[index] = index + 1
            # down wraps onto bottom surface
            down_map[index] = index + L
            if i > 0:
                left_map[index] = index - 1

    starting_index += L * H

    ## Bottom surface (L x D)
    #     (D+H)L    (D+H)L+1    ... (D+H+1)L-1
    #     (D+H+1)L  (D+H+1)L+1  ... (D+H+2)L-1
    #     ...
    #     (2D+H-1)L (2D+H-1)L+1 ... (2D+H)L-1
    for i in range(L):
        for j in range(D):
            index = starting_index + j * L + i

            # up wraps onto front surface
            up_map[index] = index - L
            if i < L - 1:
                right_map[index] = index + 1
            # down wraps onto back surface
            down_map[index] = index + L
            if i > 0:
                left_map[index] = index - 1

    starting_index += L * D

    ## Back surface (L x H)
    #     (2D+H)L    (2D+H)L+1    ... (2D+H+1)L-1
    #     (2D+H+1)L  (2D+H+1)L+1  ... (2D+H+2)L-1
    #     ...
    #     (2D+2H-1)L (2D+2H-1)L+1 ... (2D+2H)L-1
    for i in range(L):
        for j in range(H):
            index = starting_index + j * L + i

            # up wraps onto bottom surface
            up_map[index] = index - L
            if i < L - 1:
                right_map[index] = index + 1
            if j < H - 1:
                down_map[index] = index + L
            if i > 0:
                left_map[index] = index - 1

    starting_index += L * H

    ## Left surface (D x H)
    #     (2D+2H)L        (2D+2H)L+1        ... (2D+2H)L+D-1
    #     (2D+2H)L+D      (2D+2H)L+D+1      ... (2D+2H)L+2D-1
    #     ...
    #     (2D+2H)L+(H-1)D (2D+2H)L+(H-1)D+1 ... (2D+2H)L+HD-1
    for i in range(D):
        for j in range(H):
            index = starting_index + j * D + i

            if j > 0:
                up_map[index] = index - D
            if i < D - 1:
                right_map[index] = index + 1
            if j < H - 1:
                down_map[index] = index + D
            if i > 0:
                left_map[index] = index - 1

    starting_index += D * H

    ## Right surface (D x H)
    #     (2D+2H)L+HD      (2D+2H)L+HD+1      ... (2D+2H)L+(H+1)D-1
    #     (2D+2H)L+(H+1)D  (2D+2H)L+(H+1)D+1  ... (2D+2H)L+(H+2)D-1
    #     ...
    #     (2D+2H)L+(2H-1)D (2D+2H)L+(2H-1)D+1 ... (2D+2H)L+2HD-1
    for i in range(D):
        for j in range(H):
            index = starting_index + j * D + i

            if j > 0:
                up_map[index] = index - D
            if i < D - 1:
                right_map[index] = index + 1
            if j < H - 1:
                down_map[index] = index + D
            if i > 0:
                left_map[index] = index - 1

    ## Link front and left surfaces
    #          left     H  front
    #     (2D+2H)L+D-1  | DL
    #     (2D+2H)L+2D-1 | (D+1)L
    #     ...           | ...
    #     (2D+2H)L+HD-1 | (D+H-1)L
    left_starting_index = (2 * (D + H) * L) + D - 1
    for i in range(H):
        right_map[left_starting_index + (i * D)] = (D + i) * L
        left_map[(D + i) * L] = left_starting_index + (i * D)

    ## Link front and right surfaces
    #       front  H      right
    #     (D+1)L-1 | (2D+2H)L+HD
    #     (D+2)L-1 | (2D+2H)L+(H+1)D
    #     ...      | ...
    #     (D+H)L-1 | (2D+2H)L+(2H-1)D
    right_starting_index = (2 * (D + H) * L) + (H * D)
    for i in range(H):
        right_map[((D + i + 1) * L) - 1] = right_starting_index + (i * D)
        left_map[right_starting_index + (i * D)] = ((D + i + 1) * L) - 1

    ## Zip top and back surfaces
    #     back  (2D+2H-1)L (2D+2H-1)L+1 ... (2D+2H)L-1
    #         L --------------------------------------
    #      top  0          1            ... L-1
    back_starting_index = ((2 * (D + H)) - 1) * L
    for i in range(L):
        up_map[i] = back_starting_index + i
        down_map[back_starting_index + i] = i

    ## Zip top and left surfaces
    #                                                top
    #                                            | 0
    #                           D ------------>  | L
    #                           |                | ...
    #                           v                | (D-1)L
    #     ---------------------------------------
    #     (2D+2H)L  (2D+2H)L+1  ...  (2D+2H)L+D-1
    #                        left
    left_starting_index = 2 * (D + H) * L
    for i in range(D):
        up_map[left_starting_index + i] = i * L
        left_map[i * L] = left_starting_index + i

    ## Zip top and right surfaces
    #       top                       
    #     L-1  |                
    #     2L-1 |  <-------------------- D              
    #     ...  |                        |
    #     DL-1 |                        v
    #           ------------------------------------------------
    #           (2D+2H)L+HD  (2D+2H)L+HD+1 ... (2D+2H)L+(H+1)D-1
    #                        right
    right_starting_index = (2 * (D + H) * L) + (H * D)
    for i in range(D):
        top_index = ((D - i) * L) - 1
        up_map[right_starting_index + i] = top_index
        right_map[top_index] = right_starting_index + i

    ## Zip bottom and left surfaces
    #                        left
    #     (2D+2H)L+(H-1)D (2D+2H)L+(H-1)D+1 ... (2D+2H)L+HD-1
    #     ---------------------------------------------------
    #                                ^                       | (D+H)L
    #                                |                       | (D+H+1)L
    #                                D ------------------->  | ...
    #                                                        | (2D+H-1)L
    #                                                          bottom
    left_starting_index = (2 * (D + H) * L) + ((H - 1) * D)
    for i in range(D):
        bottom_index = ((2 * D) + H - 1 - i) * L
        down_map[left_starting_index + i] = bottom_index
        left_map[bottom_index] = left_starting_index + i

    ## Zip bottom and right surfaces
    #                                        right
    #                 (2D+2H)L+(2H-1)D (2D+2H)L+(2H-1)D+1 ... (2D+2H)L+2HD-1
    #                 ------------------------------------------------------
    #     (D+H+1)L-1 |                          ^                     
    #     (D+H+2)L-1 |                          |                     
    #     ...        |  <---------------------- D
    #     (2D+H)L-1  |                                                 
    #      bottom
    right_starting_index = (2 * (D + H) * L) + (((2 * H) - 1) * D)
    for i in range(D):
        bottom_index = ((D + H + 1 + i) * L) - 1
        down_map[right_starting_index + i] = bottom_index
        right_map[bottom_index] = right_starting_index + i

    ## Zip back and left surfaces
    #            | (2D+2H)L
    #         -> | (2D+2H)L+D   left
    #       /    | ...
    #      /     | (2D+2H)L+(H-1)D
    #     H    * * *
    #      \     | (2D+H)L
    #       \    | (2D+H+1)L
    #         -> | ...          back
    #            | (2D+2H-1)L
    left_starting_index = 2 * (D + H) * L
    back_starting_index = (2 * (D + H) * L) - L
    for i in range(H):
        left_index = left_starting_index + (i * D)
        back_index = back_starting_index - (i * L)
        left_map[left_index] = back_index
        left_map[back_index] = left_index

    ## Zip back and right surfaces
    #           (2D+2H)L+(H+1)D-1 |
    #     right (2D+2H)L+(H+2)D-1 | <-
    #           ...               |    \
    #           (2D+2H)L+2HD-1    |     \
    #                           * * *    H
    #           (2D+H+1)L-1       |     /
    #           (2D+H+2)L-1       |    /
    #     back  ...               | <-
    #           (2D+2H)L-1        |
    right_starting_index = (2 * (D + H) * L) + ((H + 1) * D) - 1
    back_starting_index = (2 * (D + H) * L) - 1
    for i in range(H):
        right_index = right_starting_index + (i * D)
        back_index = back_starting_index - (i * L)
        right_map[right_index] = back_index
        right_map[back_index] = right_index

    # should now have complete directional maps
    # can build 'Face' instances with all their connections
    total_faces = (2 * L * D) + (2 * L * H) + (2 * D * H)

    order = list(range(total_faces))

    if randomise:
        random.shuffle(order)

    args = {
        new_label: (
            new_label,
            order[up_map[i]],
            order[right_map[i]],
            order[down_map[i]],
            order[left_map[i]]
        )
        for i, new_label in enumerate(order)
    }

    for i in range(total_faces):
        _add(*args[i])

    return faces, edges
