"""
Module defining a parser for command-line arguments
"""
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--box', action='append', nargs=3)


def parse_box_dimensions():
    """Convert command-line arguments to tuples of box dimensions"""
    boxes = parser.parse_args().box

    return tuple(
        tuple(int(x) for x in box)
        for box in boxes
    )
