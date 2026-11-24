import numpy as np

import Ant
import Problem


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
        self.best_moveset = None
        self.best_cost = float("inf")

        self.pheromones = np.ones((self.problem.row, self.problem.column, 4), float)

        # ADDED: Store visualization history
        self.history = []

        for row in range(self.problem.row):

            for column in range(self.problem.column):

                if self.problem.grid[row][column] == 0:

                    for move in Problem.VALID_MOVES:

                        coordinate = (row + move[0], column + move[1])

                        if (
                            self.problem.is_inside(coordinate)
                            and self.problem.grid[coordinate[0]][coordinate[1]] == 1
                        ):

                            index = Problem.VALID_MOVES.index(move)

                            self.pheromones[row][column][index] = 0

    # ADDED: Save ant position and pheromone values
    def save_step(self, iteration, ant_number, ant, status):

        self.history.append(
            {
                "iteration": iteration + 1,
                "ant": ant_number + 1,
                "path": ant.visited.copy(),
                "position": ant.position,
                "best_path": (
                    self.best_path.copy() if self.best_path is not None else []
                ),
                "status": status,
                "pheromones": self.pheromones.copy(),
            }
        )

    def update_pheromone(
        self, paths: list[list[tuple]], moves: list[list[tuple]], distances: list[int]
    ):

        self.pheromones *= 1 - self.evaporation

        for path, move, distance in zip(paths, moves, distances):

            for i in range(len(path) - 1):

                m = move[i]

                index = Problem.VALID_MOVES.index(m)

                self.pheromones[path[i][0]][path[i][1]][index] += self.Q / distance

    def calculate_probability_numerator(
        self, ant: Ant.Ant, coordinate: tuple, move_index: int
    ) -> float:

        tau = (
            self.pheromones[ant.position[0]][ant.position[1]][move_index] ** self.alpha
        )

        eta = (1 / (self.problem.manhattan_distance(coordinate) + 1)) ** self.beta

        return tau * eta

    def run(self):

        if self.problem.start == self.problem.dest:
            return [self.problem.start], [], 0

        for iteration in range(self.iterations):

            print(f"Iteration {iteration}")

            all_paths = []
            all_moves = []
            all_distances = []

            for ant_number in range(self.ants):

                ant = Ant.Ant(self.problem)

                # ADDED: Save starting position
                self.save_step(iteration, ant_number, ant, "Started")

                while not ant.reached_dest():

                    valid_neighbors = self.problem.valid_neighbors(ant.position)

                    if len(valid_neighbors) == 0:

                        print(f"Ant {ant_number} not reached!")

                        # ADDED: Save dead end
                        self.save_step(iteration, ant_number, ant, "No valid moves")

                        break

                    probabilities = []

                    for coordinate in valid_neighbors:

                        if coordinate not in ant.visited:

                            move = (
                                coordinate[0] - ant.position[0],
                                coordinate[1] - ant.position[1],
                            )

                            index = Problem.VALID_MOVES.index(move)

                            probabilities.append(
                                self.calculate_probability_numerator(
                                    ant, coordinate, index
                                )
                            )

                        else:
                            probabilities.append(0)

                    probabilities = np.array(probabilities)

                    prob_sum = probabilities.sum()

                    if prob_sum == 0:

                        print(f"Ant {ant_number} looped!")

                        # ADDED: Save loop detection
                        self.save_step(iteration, ant_number, ant, "Loop detected")

                        break

                    probabilities /= prob_sum

                    next_position_index = np.random.choice(
                        len(valid_neighbors), p=probabilities
                    )

                    ant.move(
                        (
                            valid_neighbors[next_position_index][0] - ant.position[0],
                            valid_neighbors[next_position_index][1] - ant.position[1],
                        )
                    )

                    # ADDED: Save every movement
                    self.save_step(iteration, ant_number, ant, "Moving")

                if ant.reached_dest():

                    all_paths.append(ant.visited)
                    all_moves.append(ant.path)
                    all_distances.append(ant.move_cost)

                    if ant.move_cost < self.best_cost:

                        self.best_cost = ant.move_cost

                        self.best_path = ant.visited.copy()

                        self.best_moveset = ant.path.copy()

                        print("A better path founded!")

                    # ADDED: Save successful path
                    self.save_step(iteration, ant_number, ant, "Reached destination")

            # Update pheromones after all ants finish
            self.update_pheromone(all_paths, all_moves, all_distances)

            # ADDED: Save pheromones after each iteration
            self.history.append(
                {
                    "iteration": iteration + 1,
                    "ant": None,
                    "path": [],
                    "position": None,
                    "best_path": (
                        self.best_path.copy() if self.best_path is not None else []
                    ),
                    "status": "Pheromones updated",
                    "pheromones": self.pheromones.copy(),
                }
            )

        return (self.best_path, self.best_moveset, self.best_cost)
