import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--box', action='append', nargs=3)


def parse_box_dimensions():
    boxes = parser.parse_args().box

    return tuple(
        tuple(int(x) for x in box)
        for box in boxes
    )
