from geralt.path_finding import a_star
import random
import math

def optimal_path(start, end, objectives, maze):
    # traveling_path = [start]
    # for o in objectives:
    #     traveling_path.append(o)
    # traveling_path.append(end) 

    # The nearest neighbor method
    optimal_path = []
    optimal_path.append(start)

    remaining_objectives =  objectives.copy()

    for i in objectives:
        current_position = optimal_path[-1]
        nearest_objective = min(remaining_objectives, key=lambda x: len(a_star(current_position, x , maze)))
        optimal_path.append(nearest_objective)
        remaining_objectives.remove(nearest_objective)

    optimal_path.append(end)

    total_distance = 0
    for i in range(len(optimal_path) - 1):
        total_distance += len(a_star(optimal_path[i], optimal_path[i + 1], maze))

    print(f"Optimal order to visit objectives: {optimal_path}")
    print(f"Total distance: {total_distance}")

    return optimal_path


def closest_objective(player_position, objectives, maze):
    closest = None
    for i in objectives:
        nearest_objective = min(objectives, key=lambda x: len(a_star(player_position, x , maze)))

    return closest