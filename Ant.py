import Problem


class Ant:
    def __init__(self, problem: Problem.Problem):
        self.problem = problem
        self.pose = self.problem.start
        self.visited = [self.problem.start]

    def move(self, move: tuple) -> None:
        if move in self.problem.valid_neighbors(self.pose):
            self.pose = (self.pose[0] + move[0], self.pose[1] + move[1])
