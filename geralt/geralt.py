from Games2D import Action
from geralt.input import Input
from geralt import geralt_debug as dbg


class Geralt:
    def __init__(self, game_app) -> None:
        self.frame = 0
        self.input = Input(game_app)
        self.maze_info = None

    def action(self):
        if self.maze_info is None:
            self.maze_info = self.input.maze_info()

        x, y = self.input.player_position()

        if self.frame % 50 == 0:
            dbg.print_maze(self.maze_info["maze"], player_position=(x, y))

        self.frame += 1
        return Action.DOWN | Action.RIGHT
