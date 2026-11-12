import numpy as np


class problem:

    def __init__(self, column: int, row: int, start: tuple, dest: tuple):
        self.column = column
        self.row = row
        self.grid = np.zeros((row, column), int)
        self.start = start
        self.dest = dest

    def printEnv(self):
        print(self.grid)

    def setBlocks(self, blocksList):
        for coordinats in blocksList:
            if coordinats != self.start and coordinats != self.dest:
                self.grid[coordinats[0]][coordinats[1]] = 1
