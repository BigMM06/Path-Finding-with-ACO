import math

import numpy as np

import Ant
import Problem


# Q = Number of deposited pheromones
class ACO:
    def __init__(
        self,
        problem: Problem.Problem,
        iterations: int,
        ants: int,
        alpha: float,
        beta: float,
        evaporation_rate: float,
        Q: float,
    ):
        self.problem = problem
        self.iterations = iterations
        self.ants = ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation_rate
        self.Q = Q
        self.best_path = None
        self.best_cost = math.inf
        self.pheromones = np.ones((self.problem.row, self.problem.column), float)
        for row in range(self.problem.row):
            for column in range(self.problem.column):
                if self.problem.grid[row][column] == 1:
                    self.pheromones[row][column] = 0

    def update_phromone(self):
        pass

    def run(self):
        for iteration in range(self.iterations):
            all_paths = []
            all_distances = []
            for ant in range(self.ants):
                pass
