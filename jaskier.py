from pygame.rect import Rect


class Jaskier:
    def __init__(self, maze) -> None:
        self.maze = maze

    def maze_info(self):
        return {
            "walls": list(
                filter(
                    lambda x: x is not None,
                    map(
                        self.rect_to_position,
                        map(self.rect_to_tile, self.maze.wallList),
                    ),
                )
            ),
            "coins": list(
                map(self.rect_to_position, map(self.rect_to_tile, self.maze.coinList))
            ),
            "tresures": list(
                map(
                    self.rect_to_position,
                    map(self.rect_to_tile, self.maze.treasureList),
                )
            ),
            "obstacle": list(
                map(
                    self.rect_to_position,
                    map(self.rect_to_tile, self.maze.obstacleList),
                )
            ),
            # "monsters": list(
            #     map(
            #         self.rect_to_position,
            #         map(self.rect_to_tile, self.maze.monsterList),
            #     )
            # ),
            # "doors": list(
            #     map(self.rect_to_position, map(self.rect_to_tile, self.maze.doorList))
            # ),
        }

    def position_to_tile(self, position):
        x, y = position
        return x / self.maze.tile_size_x, y / self.maze.tile_size_y

    def rect_to_tile(self, rect: Rect):
        return Rect(
            round(rect.left / self.maze.tile_size_x),
            round(rect.top / self.maze.tile_size_y),
            round(rect.width / self.maze.tile_size_x),
            round(rect.height / self.maze.tile_size_y),
        )

    def rect_to_position(self, rect: Rect):
        if (rect.width == 1 and rect.height == 1) or (
            rect.width == 0 and rect.height == 0
        ):
            return rect.left, rect.top
        else:
            None
