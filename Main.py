import numpy as np


class environment:

    def __init__(self, h_counts: int, v_counts: int):
        self.h_counts = h_counts
        self.v_counts = v_counts
        self.grid = np.zeros((v_counts, h_counts), int)

    def printEnv(self):
        print(self.grid)

    def setBlocks(self, blocksList):
        for coordinats in blocksList:
            self.grid[coordinats[0]][coordinats[1]] = 1
