from Games2D import Action
from geralt.input import Input


class Geralt:
    def __init__(self, game_app) -> None:
        self.frame = 0
        self.input = Input(game_app)
        self.maze_info = None

    def action(self):
        if self.maze_info is None:
            self.maze_info = self.input.maze_info()

        if self.frame % 50 == 0:
            self.input.print_maze()

        x, y = self.input.player_position()

        self.frame += 1
        return Action.DOWN | Action.RIGHT
