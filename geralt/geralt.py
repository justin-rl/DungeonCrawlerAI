import math

from matplotlib import pyplot as plt
from Games2D import Action
from geralt.input import Input
from geralt import geralt_debug as dbg
from geralt.path_finding import a_star
from geralt.fuzzy_controller import create_fuzzy_controller


class Geralt:
    def __init__(self, game_app) -> None:
        self.frame = -1
        self.input = Input(game_app)
        self._fuzz_controller = create_fuzzy_controller()
        for var in self._fuzz_controller.ctrl.fuzzy_variables:
            var.view()
        plt.show()

    def action(self):
        self.frame += 1

        self.maze_info = self.input.maze_info()
        x, y = self.input.player_position()

        tile_position = (math.floor(x), math.floor(y))

        path = a_star(tile_position, self.maze_info["exit"], self.maze_info["maze"])[1:]

        if self.frame % 50 == 0:
            # dbg.print_maze(self.maze_info["maze"], player_position=(x, y), path=path)
            pass

        items, obstacles = self.input.player_perspective()

        action = Geralt._direction_to_tile(tile_position, path[0])

        left = 0
        right = 0
        if action == Action.Left:
            player_input = (1 - (y - tile_position[1]) - 0.30) * 1.43
            left = Action.Down
            right = Action.Up
        elif action == Action.Right:
            player_input = (y - tile_position[1]) * 1.53
            left = Action.Up
            right = Action.Down
        elif action == Action.Up:
            player_input = (x - tile_position[0]) * 1.65
            left = Action.Left
            right = Action.Right
        elif action == Action.Down:
            player_input = ((1 - (x - tile_position[0])) - 0.4) * 1.65
            left = Action.Right
            right = Action.Left
        if player_input < 0:
            player_input = 0
        if player_input > 1:
            player_input = 1
        self._fuzz_controller.input["player"] = player_input
        self._fuzz_controller.compute()
        out = self._fuzz_controller.output["output"]

        if out < 0.45:
            action |= left
        elif out > 0.55:
            action |= right

        return action

    def _direction_to_tile(tile_position, tile):
        xp, yp = tile_position
        xt, yt = tile
        dx = xt - xp
        dy = yt - yp
        direction = 0

        if dx < 0:
            direction |= Action.Left
        elif dx > 0:
            direction |= Action.Right

        if dy < 0:
            direction |= Action.Up
        elif dy > 0:
            direction |= Action.Down

        return direction
