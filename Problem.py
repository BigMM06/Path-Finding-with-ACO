import numpy as np

VALID_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Problem:

    def __init__(self, column: int, row: int, start: tuple, dest: tuple):
        self.row = row
        self.column = column
        self.grid = np.zeros((row, column), int)
        self.start = start
        self.dest = dest

    def print_env(self):
        print(self.grid)

    def is_inside(self, pose: tuple) -> bool:
        r, c = pose
        return 0 <= r < self.row and 0 <= c < self.column

    def set_blocks(self, blocks_list):
        for coordinates in blocks_list:
            if (
                self.is_inside(coordinates)
                and coordinates != self.start
                and coordinates != self.dest
            ):
                self.grid[coordinates[0]][coordinates[1]] = 1

    def valid_neighbors(self, pose: tuple) -> list:
        neighborsList = []
        if not self.is_inside(pose):
            return neighborsList

        for move in VALID_MOVES:
            coordinate = (pose[0] + move[0], pose[1] + move[1])
            if (
                self.is_inside(coordinate)
                and self.grid[coordinate[0]][coordinate[1]] == 0
            ):
                neighborsList.append(coordinate)
        return neighborsList

    def manhattan_distance(self, coordinate: tuple) -> int:
        return abs(self.dest[0] - coordinate[0]) + abs(self.dest[1] - coordinate[1])
