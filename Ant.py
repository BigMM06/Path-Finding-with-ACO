import Problem


class Ant:
    def __init__(self, problem: Problem.Problem):
        self.problem = problem
        self.position = self.problem.start
        self.move_cost = 0
        self.visited = [self.problem.start]
        self.path = []

    def move(self, move: tuple) -> bool:
        coordinate = (self.position[0] + move[0], self.position[1] + move[1])
        if coordinate in self.problem.valid_neighbors(self.position):
            self.position = coordinate
            self.path.append(move)
            self.move_cost += 1
            self.visited.append(self.position)
            return True
        else:
            return False

    def get_current_position(self) -> tuple:
        return self.position

    def reached_dest(self) -> bool:
        return self.position == self.problem.dest
