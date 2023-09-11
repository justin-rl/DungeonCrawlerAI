from enum import IntEnum
import math
import numpy as np
from pygame import Rect
from Constants import PLAYER_SIZE

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
        x, y = self._tile_from_px(x, y)
        x += PLAYER_SIZE / 2
        y += PLAYER_SIZE / 2
        return x, y
    
    def player_perspective(self):
        _walls, obstacles, items, _monsters, _doors = self._game_app.maze.make_perception_list(self._game_app.player, self._game_app._display_surf)
        items = list(map(lambda p: self._tile_from_px(*p), map(Input._position_from_rect, items)))
        obstacles = list(map(lambda p: self._tile_from_px(*p), map(Input._position_from_rect, obstacles)))
        monsters = _monsters
        return items, obstacles, monsters

    def maze_info(self):
        start = self._tile_from_px(*self._game_app.maze.start)
        start = (math.floor(start[0]), math.floor(start[1]))

        exit = self._tile_from_px(*Input._position_from_rect(self._game_app.maze.exit))
        exit = (round(exit[0]), round(exit[1]))

        walls = self._round_positions_from_rects(self._game_app.maze.wallList)
        walls.remove(start)

        coins = self._floor_positions_from_rects(self._game_app.maze.coinList)
        obstacles = self._floor_positions_from_rects(self._game_app.maze.obstacleList)
        treasures = self._round_positions_from_rects(self._game_app.maze.treasureList)

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

    def _round_positions_from_rects(self, rects):
        return list(map(lambda p: (round(p[0]), round(p[1])), map(lambda p: self._tile_from_px(*p), map(Input._position_from_rect, rects))))

    def _floor_positions_from_rects(self, rects):
        return list(map(lambda p: (math.floor(p[0]), math.floor(p[1])), map(lambda p: self._tile_from_px(*p), map(Input._position_from_rect, rects))))

    def _tile_from_px(self, x, y):
        return x / self._game_app.maze.tile_size_x, y / self._game_app.maze.tile_size_y 

    def _position_from_rect(rect: Rect):
        return (rect.left, rect.top)
