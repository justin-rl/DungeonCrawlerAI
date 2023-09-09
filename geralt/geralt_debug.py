import math
from geralt.input import MazeItem


def print_maze(maze, player_position = None, path = None):
        s = ""
        n, m = maze.shape
        for j in range(0, m):
            sa = ""
            sb = ""
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
                ca = c
                cb = c
                if path: 
                    for p in path:
                        if i == p[0] and j == p[1] and e != MazeItem.Wall:
                            cb = "🟩"
                            break

                sa += ca
                sb += cb 
            s += sa 
            if path: 
                s += " │ " + sb
            s += "\n"
        print(s)