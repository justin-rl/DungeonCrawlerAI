from enum import Enum

from pygame.rect import Rect
from Games2D import Action
from Player import Player
from Maze import Maze
from jaskier import Jaskier


class Geralt:
    def __init__(self, player: Player, maze: Maze) -> None:
        self._player = player
        self._maze = maze
        self.jaskier = Jaskier(maze)
        self.maze_info = None

    def action(self):
        if self.maze_info is None:
            self.maze_info = self.jaskier.maze_info()

        print("maze info", self.maze_info)
        print("position", self.position())
        print("perseption", self.look_around())
        return Action.DOWN | Action.RIGHT

    def position(self) -> tuple[int, int]:
        return self.jaskier.position_to_tile(self._player.get_position())

    def attribute(self) -> any:
        return self._player.get_attributes()

    def look_around(self) -> any:
        w, o, i, m, d = self._maze.make_perception_list(self._player, display_surf=None)
        return {
            "walls": list(
                filter(
                    lambda x: x is not None,
                    map(
                        self.jaskier.rect_to_position, map(self.jaskier.rect_to_tile, w)
                    ),
                )
            ),
            "obstacles": list(map(self.jaskier.rect_to_tile, o)),
            "items": list(map(self.jaskier.rect_to_tile, i)),
            "monsters": list(map(self.jaskier.rect_to_tile, m)),
            "doors": list(map(self.jaskier.rect_to_tile, d)),
            "start": None, 
            "end": None
        }
