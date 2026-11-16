import matplotlib.pyplot as plt

import ACO
import Problem

row = int(input("Enter row count: "))
column = int(input("Enter column count: "))
start = tuple(int(x) for x in input("Enter start coordination: ").split())
dest = tuple(int(x) for x in input("Enter destination coordination: ").split())
problem = Problem.Problem(row, column, start, dest)
blocks_count = int(input("How many blocks you want to create? "))
blocks_list = []
for block in range(blocks_count):
    blocks_list.append(
        tuple(int(x) for x in input(f"Enter block {block} coordination: ").split())
    )
problem.set_blocks(blocks_list)
algorithm = ACO.ACO(
    problem, 50, 10, 1, 2, 0.5, 100
)  # HyperParameters should change according to the problem

best_path, best_moveset, best_cost = algorithm.run()

if best_path == None:
    print("No path found!")
else:
    print("Best path:", best_path)
    print("Best moves:", best_moveset)
    print("Best cost:", best_cost)
