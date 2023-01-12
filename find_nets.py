from dimensions import LENGTH, DEPTH, HEIGHT, target_boxes
from src.box_graph_builder import build_box_graph
from src.get_all_trees import generate_all_trees
from src.matrix_helpers import remove_zero_rows_columns
from src.net_helpers import create_net, check_net


total_faces = 2 * ((LENGTH * DEPTH) + (LENGTH * HEIGHT) + (DEPTH * HEIGHT))

faces, adjacent_faces = build_box_graph(LENGTH, HEIGHT, DEPTH, True)
target_boxes_faces = {
    dimensions: build_box_graph(*dimensions)[0] for dimensions in target_boxes
}


def try_net(net):
    matches = [
        dimensions
        for dimensions, faces in target_boxes_faces.items()
        if check_net(net, faces)
    ]

    if len(matches) > 0:
        f = open("results.txt", "a")
        f.write("\n--------------------\n")

        for row in net:
            f.write(
                "".join(
                    "[]" if el == 1 else (f"[{str(el)}" if el else "  ")
                    for el in row
                ) + "\n"
            )

        for match in matches:
            f.write(f"\nCommon development with {match}\n")

        f.close()

        if len(matches) == len(target_boxes):
            print("\nDone!")
            return True


is_done = False

# start at (-3, -2, 1, x, x, ...)
for off_1 in range(-3, 4):
    for off_2 in range(-3, 4):
        for off_3 in range(-3, 4):
            # ignore offsets already checked
            if (
                (off_1 == -3) and
                ((off_2 == -3) or ((off_2 == -2) and (off_3 < 1)))
            ):
                continue
            for off_4 in range(-3, 4):
                for off_5 in range(-3, 4):
                    print(
                        ".".join(str(offset) for offset in [
                            off_1, off_2, off_3, off_4,
                            off_5, "x", "x", "x", "x", "x"
                        ])
                    )

                    for off_6 in range(-3, 4):
                        for off_7 in range(-3, 4):
                            for off_8 in range(-3, 4):
                                for off_9 in range(-3, 4):
                                    for off_10 in range(-3, 4):
                                        net = [
                                            [0] * 70 for _ in range(13)
                                        ]
                                        offsets = [
                                            0, off_1, off_2, off_3, off_4,
                                            off_5, off_6, off_7, off_8, off_9,
                                            off_10
                                        ]

                                        start = 30
                                        cumulative_offset = start

                                        net[0][start] = 1

                                        for row, offset in enumerate(offsets):
                                            cumulative_offset += offset

                                            for j in range(4):
                                                index = j + cumulative_offset
                                                net[row + 1][index] = 1

                                        net[12][cumulative_offset] = 1

                                        net = remove_zero_rows_columns(net)

                                        if try_net(net):
                                            is_done = True
                                            break

                                    if is_done:
                                        break

                                if is_done:
                                    break

                            if is_done:
                                break

                        if is_done:
                            break

                    if is_done:
                        break

                if is_done:
                    break

            if is_done:
                break

        if is_done:
            break

    if is_done:
        break


# already_seen = set()
# count = 0

# for tree in generate_all_trees(list(range(total_faces)), adjacent_faces):
#     net = create_net(tree, faces)

#     count += 1
#     if net not in already_seen:
#         print(f"\n{len(already_seen) + 1}  ({count}).")

#         already_seen.add(net)

#         for row in net:
#             print(
#                 "".join(
#                     "[]" if el == 1 else (f"[{str(el)}" if el else "  ")
#                     for el in row
#                 )
#             )

#         try_net(net)
