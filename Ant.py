import Problem


class Ant:
    def __init__(self, problem: Problem.Problem):
        self.problem = problem
        self.pose = self.problem.start
        self.moveCost = 0
        self.visited = [self.problem.start]
        self.path = []

    def move(self, move: tuple) -> None:
        if move in self.problem.valid_neighbors(self.pose):
            self.pose = (self.pose[0] + move[0], self.pose[1] + move[1])
            self.path.append(move)
            self.moveCost += 1
            self.visited.append(self.pose)
        else:
            print("Not valid move")

    def current_pose(self) -> tuple:
        return self.pose

    def is_reach_food(self) -> bool:
        return self.pose == self.problem.dest
