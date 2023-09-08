from enum import IntEnum
import math
import numpy as np
from pygame import Rect

from Games2D import App


class MazeItem(IntEnum):
    Path = 0
    Wall = 1
    Obstacle = 2
    Coin = 3
    Treasure = 4
    Monster = 5
    Door = 6
    Exit = 7


class Input:
    def __init__(self, game_app: App) -> None:
        self._game_app = game_app

    def player_position(self):
        x, y = self._game_app.player.get_position()
        return self._tile_from_px(x, y)

    def maze_info(self):
        start = self._tile_from_px(*self._game_app.maze.start)
        start = (math.floor(start[0]), math.floor(start[1]))

        exit = self._tile_from_px(*Input._position_from_rect(self._game_app.maze.exit))
        exit = (math.floor(exit[0]), math.floor(exit[1]))

        walls = self._floor_positions_from_rects(self._game_app.maze.wallList)
        walls.remove(start)
        walls.remove(exit)

        coins = self._floor_positions_from_rects(self._game_app.maze.coinList)
        obstacles = self._floor_positions_from_rects(self._game_app.maze.obstacleList)
        treasures = self._floor_positions_from_rects(self._game_app.maze.treasureList)

        maze = np.full(
            shape=(self._game_app.maze.M, self._game_app.maze.N),
            fill_value=MazeItem.Path,
        )
        maze[exit] = MazeItem.Exit
        for i, j in walls:
            maze[i][j] = MazeItem.Wall
        for i, j in coins:
            maze[i][j] = MazeItem.Coin 
        for i, j in obstacles:
            maze[i][j] = MazeItem.Obstacle
        for i, j in treasures:
            maze[i][j] = MazeItem.Treasure

        return {"start": start, "exit": exit, "walls": walls, "coins": coins, "obstacles": obstacles, "treasures": treasures, "maze": maze}

    def _floor_positions_from_rects(self, rects):
        return list(map(lambda p: (round(p[0]), round(p[1])), map(lambda p: self._tile_from_px(*p), map(Input._position_from_rect, rects))))

    def _tile_from_px(self, x, y):
        return x / self._game_app.maze.tile_size_x, y / self._game_app.maze.tile_size_y

    def _rect_tile_from_rect_px(self, rect: Rect):
        return Rect(
            round(rect.left / self._game_app.maze.tile_size_x),
            round(rect.top / self._game_app.maze.tile_size_y),
            round(rect.width / self._game_app.maze.tile_size_x),
            round(rect.height / self._game_app.maze.tile_size_y),
        )

    def _position_from_rect(rect: Rect):
        return (rect.left, rect.top)
    
    def print_maze(self):
        maze = self.maze_info()["maze"]
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
                x, y = self.player_position()
                x = math.floor(x) 
                y = math.floor(y) 
                if i == x and j == y:
                    c = "🧝"
                s += c
            s += "\n"
        print(s)
