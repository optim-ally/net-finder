"""
Module defining the 'Face' dataclass
"""
from dataclasses import dataclass


@dataclass
class Face():

    """Face class for storing nodes of net graphs"""

    def __init__(self, adjacents_clockwise):
        self.adjacents = adjacents_clockwise

    def orient(self, adjacent_face, direction):
        """
        Rotate `adjacents` to match a given orientation of the face.

        :param Face adjacent_face: One of the adjacent faces
        :param int direction: New direction of that face relative to this one

        This is used to sychronise the orientation of a face with others around
        it. A net in tree format has no inherent orientation, but it may be
        given several orientations while checking it against different boxes.
        """
        if adjacent_face in self.adjacents:
            face_index = self.adjacents.index(adjacent_face)
            desired_index = direction

            shift = (face_index - desired_index + 4) % 4

            self.adjacents = self.adjacents[shift:] + self.adjacents[:shift]
        else:
            print("Failed to orient: adjacent face not recognised")
