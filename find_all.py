from time import time
from concurrent.futures import (
    ProcessPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED, Future
)

from setup import PROCESSES
from python.arg_parser import parse_box_dimensions
from python.box_graph_builder import build_box_graph
from python.get_all_trees import generate_all_trees
from python.net_helpers import create_net, is_net, stringify_net


def try_tree(tree, faces, target_boxes):
    net = create_net(tree, faces)

    if all(is_net(net, box) for box in target_boxes):
        # found one!
        return stringify_net(net)
    

def find_all_common_nets(dimensions):
    faces, adjacent_faces = build_box_graph(*dimensions[0])
    target_boxes = tuple(build_box_graph(*dims)[0] for dims in dimensions[1:])

    seen = set()

    def handle_results(completed: set[Future]):
        for task in completed:
            result = task.result()

            if result is not None and result not in seen:
                seen.add(result)
                print(f'\n{len(seen)}\n{result}')

                with open('results.txt', 'a') as f:
                    f.write(f'\n--------------------\n{len(seen)}\n{result}\n')

    with ProcessPoolExecutor(max_workers=PROCESSES) as executor:
        futures = set()

        for tree in generate_all_trees(list(range(len(faces))), adjacent_faces):
            if len(futures) >= 10000:
                # queue is getting too long, wait for tasks to complete
                completed, futures = wait(futures, return_when=FIRST_COMPLETED)
                handle_results(completed)

            futures.add(executor.submit(try_tree, tree, faces, target_boxes))

        completed, _ = wait(futures, return_when=ALL_COMPLETED)
        handle_results(completed)


if __name__ == '__main__':
    dimensions = parse_box_dimensions()

    start = time()
    find_all_common_nets(dimensions)
    end = time()

    print(f'\nFinished in {end - start}s')
