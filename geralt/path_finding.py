import math
import numpy as np

from geralt.input import MazeItem


class Node:
    def __init__(self, maze_idx, goal, parent=None):
        self.parent = parent
        self.position = maze_idx
        self.g = 0 if parent is None else parent.g + 1  # movement cost
        self.h = self.heuristic(goal)  # estimated cost

    def __eq__(self, other):
        return (
            self.position[0] == other.position[0]
            and self.position[1] == other.position[1]
        )

    def f(self):
        return self.g + self.h

    def heuristic(self, goal):
        return math.sqrt(
            (self.position[0] - goal[0]) ** 2 + (self.position[1] - goal[1]) ** 2
        )


def a_star(start, end, maze):
    open_list = [Node(start, end)]
    closed_list = []

    end_node = None

    while len(open_list) > 0 and end_node is None:
        # Find the node with the least f on the open list
        q = None
        min_f = float("inf")
        for n in open_list:
            if n.f() < min_f:
                min_f = n.f()
                q = n

        # Pop q of the open list
        open_list.remove(q)

        # Generate q's successors and set their parents to q
        successors = []
        for x, y in [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            # (1, -1),
            # (1, 1),
            # (-1, -1),
            # (1, -1),
        ]:
            position = (q.position[0] + x, q.position[1] + y)
            if (position[0] < 0 or position[0] >= maze.shape[0]) or (position[1] < 0 or position[1] >= maze.shape[1]):
                continue
            if maze[position[0]][position[1]] != MazeItem.Wall:
                successors.append(position)

        for x, y in successors:
            node = Node((x, y), end, parent=q)
            if x == end[0] and y == end[1]:
                # If successor is the goal, stop the search
                end_node = node
            else:
                # Add node with to open list if f is smaller
                prev_f = None
                prev_i = None
                for i, n in enumerate(open_list):
                    if n == node:
                        prev_f = n.f()
                        prev_i = i

                # If a node with the same position as successor is in the CLOSED list
                # which has a lower f than successor, skip this successor
                skip = False
                for n in closed_list:
                    if n == node and n.f() < node.f():
                        skip = True

                # Add node to open list
                if not skip:
                    if prev_i is None:
                        open_list.append(node)
                    if prev_f is not None and prev_f > node.f():
                        open_list[prev_i] = node

                closed_list.append(q)

    path = []
    n = end_node
    while n is not None:
        path.insert(0, n.position)
        n = n.parent
    return path
