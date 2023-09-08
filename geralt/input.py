from enum import IntEnum
import math
import numpy as np
from pygame import Rect

from Games2D import App


class MazeItem(IntEnum):
    Path = 0
    Wall = 1
    Obstacle = 2
    Token = 3
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

    def maze_walls(self):
        walls = list(
            map(
                lambda p: (round(p[0]), round(p[1])),
                map(
                    lambda p: self._tile_from_px(*p),
                    map(
                        Input._position_from_rect,
                        self._game_app.maze.wallList,
                    ),
                ),
            )
        )
        start = self._tile_from_px(*self._game_app.maze.start)
        start = (math.floor(start[0]), math.floor(start[1]))
        walls.remove(start)
        return np.array(walls)

    def maze_exit(self):
        exit = self._tile_from_px(*Input._position_from_rect(self._game_app.maze.exit))
        return (math.floor(exit[0]), math.floor(exit[1]))

    def generate_maze_matrix(self):
        maze = np.full(shape=(self._game_app.maze.M, self._game_app.maze.N), fill_value=MazeItem.Path) 
        return maze

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
