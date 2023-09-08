from pygame import Rect

class Input:
    def __init__(self, game_app) -> None:
        self._game_app = game_app

    def player_position(self):
        x, y = self._game_app.player.get_position()
        return self._tile_from_px(x, y)


    def maze_walls(self):
        walls = list(map(self._tile_from_px, map(self._position_from_rect, self._game_app.maze.wallList)))
        # remove start

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
        return rect.left, rect.right 