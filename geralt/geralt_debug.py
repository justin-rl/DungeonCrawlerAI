import math
from geralt.input import MazeItem


def print_maze(maze, player_position = None):
        s = ""
        n, m = maze.shape
        for j in range(0, m):
            for i in range(0, n):
                e = maze[i][j]
                c = e
                if e == MazeItem.Path:
                    c = "⬜"
                elif e == MazeItem.Wall:
                    c = "🧱"
                elif e == MazeItem.Exit:
                    c = "🏁"
                elif e == MazeItem.Door:
                    c = "🚪"
                elif e == MazeItem.Obstacle:
                    c = "🌵"
                elif e == MazeItem.Monster:
                    c = "🧌"
                elif e == MazeItem.Coin:
                    c = "🪙 "
                elif e == MazeItem.Treasure:
                    c = "💰"
                if player_position:
                    x = math.floor(player_position[0]) 
                    y = math.floor(player_position[1]) 
                    if i == x and j == y:
                        c = "🧝"
                s += c
            s += "\n"
        print(s)