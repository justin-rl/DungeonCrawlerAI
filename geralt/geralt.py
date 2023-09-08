from Games2D import Action
from geralt.input import Input


class Geralt:
    def __init__(self, game_app) -> None:
        self.input = Input(game_app)
        self.walls = None
        self.exit = None
        self.maze_matrix = None

    def action(self):
        if self.walls is None:
            self.walls = self.input.maze_walls()
        if self.exit is None:
            self.exit = self.input.maze_exit()
        if self.maze_matrix is None:
            self.maze_matrix = self.input.generate_maze_matrix()

        x, y = self.input.player_position()

        return Action.DOWN | Action.RIGHT
