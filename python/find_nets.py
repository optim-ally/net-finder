from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor

from dimensions import LENGTH, DEPTH, HEIGHT, target_boxes
from src.box_graph_builder import build_box_graph
from src.get_all_trees import generate_all_trees
from src.matrix_helpers import remove_zero_rows_columns
from src.net_helpers import create_net, check_net


PROCESSES = 8
SCORE_THRESHOLD = 5

# Specify whether you want all common nets or just one.
find_all = False

total_faces = 2 * ((LENGTH * DEPTH) + (LENGTH * HEIGHT) + (DEPTH * HEIGHT))

target_boxes_faces = {
    dimensions: build_box_graph(*dimensions)[0] for dimensions in target_boxes
}


class ThresholdException(Exception):
    pass


def try_net(net, best_score):
    scores = {
        dimensions: check_net(net, faces)
        for dimensions, faces in target_boxes_faces.items()
    }
    total_score = sum(scores.values())
    matches = [
        dimensions
        for dimensions, score in scores.items()
        if score == 0
    ]

    if total_score > SCORE_THRESHOLD:
        raise ThresholdException("Dead end")

    if total_score <= best_score.value:
        indiv_scores = tuple(scores.values())
        print(
            f"\nBest score: {total_score} {indiv_scores}\n" +
            "\n".join(
                "".join(
                    "[]" if el == 1 else (f"[{str(el)}" if el else "  ")
                    for el in row
                )
                for row in net
            )
        )
        best_score.value = total_score

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

            for dimensions in target_boxes:
                score = scores[dimensions]

                if score == 0:
                    f.write(f"\nCommon development with {dimensions}\n")
                else:
                    f.write(f"\n{score} away from {dimensions}\n")

            if len(matches) == len(target_boxes):
                print("\nDone!")
                return True


def find_nets(faces, adjacent_faces, best_score, is_done):
    already_seen = set()
    count = 0

    for tree in generate_all_trees(list(range(total_faces)), adjacent_faces):
        net = create_net(tree, faces)

        count += 1
        if net not in already_seen:
            already_seen.add(net)

            if try_net(net, best_score) and not find_all:
                print(
                    f"\nFound after {count} nets checked\n\n" +
                    "\n".join(
                        "".join(
                            "[]" if el == 1 else (f"[{str(el)}" if el else "  ")
                            for el in row
                        )
                        for row in net
                    )
                )
                is_done.value = True

        if is_done.value:
            break


def search_for_nets(best_score, is_done):
    while not is_done.value:
        try:
            faces, adjacent_faces = build_box_graph(LENGTH, HEIGHT, DEPTH, True)

            find_nets(faces, adjacent_faces, best_score, is_done)
        except ThresholdException as e:
            continue


if __name__ == "__main__":
    with Manager() as manager:
        is_done = manager.Value("b", 0)
        best_score = manager.Value("i", 30)

        with ProcessPoolExecutor() as executor:
            for _ in range(PROCESSES):
                executor.submit(search_for_nets, best_score, is_done)

        print("\nProcesses completed")
