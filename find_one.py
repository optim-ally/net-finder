"""
Program to search for a common net of a set of boxes
"""
from time import time
from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED

from setup import SCORE_THRESHOLD, PROCESSES
from python.arg_parser import parse_box_dimensions
from python.box_graph_builder import build_box_graph
from python.get_all_trees import generate_all_trees
from python.net_helpers import create_net, score_net, stringify_net


class ThresholdException(Exception):
    """Search has exceeded the maximum allowed distance from the goal"""


def try_net(net, dimensions, best_score):
    """
    Check wether a net is a net of all given boxes.

    :param tuple[tuple[int]] net: Bitmap of the net
    :param tuple[(int, int, int)] dimensions: Sizes of each 3D box to check
    :param Manager.Value<unsigned char> best_score: Lowest score found so far
    :returns: Whether or not the net matched all boxes
    :rtype: bool
    """
    scores = {
        dim: score_net(net, build_box_graph(*dim)[0])
        for dim in dimensions
    }
    total_score = sum(scores.values())

    if total_score <= best_score.value:
        net_string = stringify_net(net)
        indiv_scores = tuple(scores.values()) if len(scores) > 1 else ''
        result = f'\nBest score: {total_score} {indiv_scores}\n{net_string}'

        print(result)
        with open('results.txt', 'a', encoding="utf-8") as f:
            f.write(result)

        best_score.value = total_score

    elif total_score > SCORE_THRESHOLD:
        raise ThresholdException('Dead end')

    return total_score == 0


def search_for_nets(dimensions, best_score, is_done):
    """
    Systematically check possible common nets starting from a random point in
    the search space.

    :param tuple[(int, int, int)] dimensions: Sizes of each 3D box to check
    :param Manager.Value<unsigned char> best_score: Lowest score found so far
    :param Manager.Value<signed char> is_done

    Will throw a `ThresholdException` if it reaches a net that is deemed too
    far from the goal.
    """
    already_seen = set()

    # randomise the labels of the faces of the first box
    # this will randomise the trees output by `generate_all_trees` while
    # ensuring that the values of `adjacent_faces` are correct
    faces, adjacent_faces = build_box_graph(*dimensions[0], randomise=True)

    for tree in generate_all_trees(list(range(len(faces))), adjacent_faces):
        net = create_net(tree, faces)

        if net not in already_seen:
            already_seen.add(net)

            if try_net(net, dimensions[1:], best_score):
                # the net matches all boxes
                print('\nDone!')
                is_done.value = True

        if is_done.value:
            break


def start_searching(dimensions, best_score, is_done):
    """Continuously call the the search function until a common net is found"""
    while not is_done.value:
        try:
            search_for_nets(dimensions, best_score, is_done)
        except ThresholdException:
            # the last search area wasn't promising, try somewhere else
            continue


def find_one_common_net(dimensions):
    """Semi-randomly search for a single common net for the given boxes"""
    with (
        Manager() as manager,
        ProcessPoolExecutor(max_workers=PROCESSES) as executor
    ):
        is_done = manager.Value('b', 0)
        best_score = manager.Value('B', 256) # maximum size of signed char type
        futures = set()

        # start multiple simultaneous search threads
        for _ in range(PROCESSES):
            futures.add(
                executor.submit(
                    start_searching, dimensions, best_score, is_done
                )
            )

        _, futures = wait(futures, return_when=FIRST_COMPLETED)


if __name__ == '__main__':
    box_dimensions = parse_box_dimensions()

    start = time()
    find_one_common_net(box_dimensions)
    end = time()

    print(f'\nFinished in {end - start}s')
