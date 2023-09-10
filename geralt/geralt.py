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
        self._prev_action = 0
        # for var in self._fuzz_controller.ctrl.fuzzy_variables:
        #     var.view()
        # plt.show()

    def action(self):
        self.frame += 1
        self.maze_info = self.input.maze_info()
        # if self.frame % 10 != 0:
        #     return self._prev_action

        player_position = self.input.player_position()
        player_tile_position = (
            math.floor(player_position[0]),
            math.floor(player_position[1]),
        )
        player_relative_position = (
            player_position[0] - player_tile_position[0],
            player_position[1] - player_tile_position[1],
        )

        path = a_star(
            player_tile_position, self.maze_info["exit"], self.maze_info["maze"]
        )

        if self.frame % 50 == 0:
            dbg.print_maze(self.maze_info["maze"], player_tile_position, path)

        items, obstacles = self.input.player_perspective()

        direction_action = Geralt._direction_to_tile(player_tile_position, path[1])

        player_input = 0
        item_input = -1
        obstacle_input = -1

        left = 0
        right = 0
        if direction_action == Action.Left:
            player_input = (1 - player_relative_position[1] - 0.4) * (1 / 0.6)
            if len(items) > 0:
                item_input = items[0][1]
                item_input -= item_input // 1
                item_input = 1 - item_input
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][1]
                obstacle_input -= obstacle_input // 1
                obstacle_input = 1 - obstacle_input
            left = Action.Down
            right = Action.Up
        elif direction_action == Action.Right:
            player_input = player_relative_position[1] * (1 / 0.4)
            if len(items) > 0:
                item_input = items[0][1]
                item_input -= item_input // 1
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][1]
                obstacle_input -= obstacle_input // 1
            left = Action.Up
            right = Action.Down
        elif direction_action == Action.Up:
            player_input = player_relative_position[0] * (1 / 0.4)
            if len(items) > 0:
                item_input = items[0][0]
                item_input -= item_input // 1
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][0]
                obstacle_input -= obstacle_input // 1
            left = Action.Left
            right = Action.Right
        elif direction_action == Action.Down:
            player_input = (1 - player_relative_position[0] - 0.4) * (1 / 0.6)
            if len(items) > 0:
                item_input = items[0][0]
                item_input -= item_input // 1
                item_input = 1 - item_input
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][0]
                obstacle_input -= obstacle_input // 1
                obstacle_input = 1 - obstacle_input
            left = Action.Right
            right = Action.Left

        if player_input < 0:
            player_input = 0
        if player_input > 1:
            player_input = 1
        # prioritize missing the obstacle
        if obstacle_input > 0.0:
            item_input = -1

        self._fuzz_controller.input["player"] = player_input
        # self._fuzz_controller.input["item"] = item_input
        # self._fuzz_controller.input["obstacle"] = obstacle_input
        self._fuzz_controller.compute()
        out = self._fuzz_controller.output["output"] 

        action = direction_action
        if out < 0.45:
            action |= left
        elif out > 0.55:
            action |= right

        self._prev_action = action
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
