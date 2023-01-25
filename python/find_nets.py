from dimensions import LENGTH, DEPTH, HEIGHT, target_boxes
from src.box_graph_builder import build_box_graph
from src.get_all_trees import generate_all_trees
from src.matrix_helpers import remove_zero_rows_columns
from src.net_helpers import create_net, check_net


# Specify whether you want all common nets or just one.
find_all = False

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
        with open("results.txt", "a") as f:
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

            if len(matches) == len(target_boxes):
                print("\nDone!")
                return True


already_seen = set()
count = 0

for tree in generate_all_trees(list(range(total_faces)), adjacent_faces):
    net = create_net(tree, faces)

    count += 1
    if net not in already_seen:
        print(f"\n{len(already_seen) + 1}  ({count} with duplicates).")

        already_seen.add(net)

        for row in net:
            print(
                "".join(
                    "[]" if el == 1 else (f"[{str(el)}" if el else "  ")
                    for el in row
                )
            )

        if try_net(net) and not find_all:
            break
