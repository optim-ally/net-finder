"""
Generic helper functions
"""

def get_total_faces(length, height, depth):
    """Calculate the surface area of a box with given dimensions"""
    return 2 * ((length * depth) + (length * height) + (depth * height))
