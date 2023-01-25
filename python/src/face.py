class Face():
    def __init__(self, adjacents_clockwise):
        self.adjacents = adjacents_clockwise

    def orient(self, adjacent_face, direction):
        if adjacent_face in self.adjacents:
            face_index = self.adjacents.index(adjacent_face)
            desired_index = direction

            shift = (face_index - desired_index + 4) % 4

            self.adjacents = self.adjacents[shift:] + self.adjacents[:shift]
        else:
            print("Failed to orient: adjacent face not recognised")
