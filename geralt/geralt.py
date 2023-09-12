import math
from swiplserver import PrologMQI

from matplotlib import pyplot as plt
from Games2D import Action, App
from geralt.traveling_witcher import optimal_path
from geralt.genetic import Population, BabyPlayer
from geralt.input import Input
from geralt import geralt_debug as dbg
from geralt.path_finding import a_star
from geralt.fuzzy_controller import create_fuzzy_controller


class Geralt:
    frame = 0
    player_position = None
    player_tile_position = None
    player_relative_position = None
    maze_info = None
    traveling_path = None
    path_objectives = []
    set_player_attributes = None
    get_player_attributes = None
    unlock_door = None
    trained_for_monster = None

    def __init__(self, game_app: App) -> None:
        self.input = Input(game_app)
        self.set_player_attributes = game_app.player.set_attributes
        self.get_player_attributes = game_app.player.get_attributes
        self._fuzz_controller = create_fuzzy_controller()
        self._current_direction = None
        self._prev_action = 0
        self._cache = {}
        self.unlock_door = game_app.maze.unlock_door

        self.update_player_position()

        # for var in self._fuzz_controller.ctrl.fuzzy_variables:
        #     var.view()
        # plt.show()

    def update_player_position(self):
        self.player_position = self.input.player_position()
        self.player_tile_position = (
            math.floor(self.player_position[0]),
            math.floor(self.player_position[1]),
        )
        self.player_relative_position = (
            self.player_position[0] - self.player_tile_position[0],
            self.player_position[1] - self.player_tile_position[1],
        )

    def update_maze_info(self):
        self.maze_info = self.input.maze_info()

    def generate_path_objectives(self, tile):
        path = a_star(self.player_tile_position, tile, self.maze_info["maze"])
        remove = []
        for i in range(1, len(path) - 1):
            prev = path[i - 1]
            next = path[i + 1]
            if prev[0] == next[0] or prev[1] == next[1]:
                remove.append(i)
        remove.reverse()
        for i in remove:
            del path[i]
        return path

    def action(self):
        self.update_player_position()
        self.maze_info = self.input.maze_info()

        if self.traveling_path is None:
            self.traveling_path = optimal_path(
                self.player_tile_position, 
                self.maze_info["exit"], 
                self.maze_info["treasures"] + self.maze_info["coins"],
                self.maze_info["maze"]
            )

        if len(self.path_objectives) == 0:
            self.path_objectives = self.generate_path_objectives(self.traveling_path.pop(0))

        direction_action = 0 
        if len(self.path_objectives) > 0:
            direction_action = Geralt._direction_to_tile(self.player_position, self.path_objectives[0]) 
            if direction_action == 0:
                self.path_objectives.pop(0)

        if self.frame % 50 == 0:
            dbg.print_maze(self.maze_info["maze"], self.player_tile_position, self.path_objectives)

        items, obstacles, monsters, doors = self.input.player_perspective()

        if len(monsters) > 0 and monsters[0] is not self.trained_for_monster:
            m = monsters[0]
            good_enough = False
            while not good_enough:
                population = Population(lambda x: m.mock_fight(x)[1])
                attributes = population.artificial_selection(plot=False)
                nb_win, score = m.mock_fight(BabyPlayer(attributes))
                print(nb_win, score, self.get_player_attributes())
                if nb_win == 4:
                    good_enough = True
            self.set_player_attributes(attributes) 
            self.trained_for_monster = m

        if len(doors) > 0:
            door = doors[0]
            state = door.check_door()
            with PrologMQI() as mqi_file:
                with mqi_file.create_thread() as prolog_thread:
                    prolog_thread.query("[door]")
                    messy_key = prolog_thread.query(f"keysPossible({state}, Res)")
            key = messy_key[0]['Res'][0]
            self.unlock_door(key)
        

        player_input = 0
        item_input = -1
        obstacle_input = -1

        left = 0
        right = 0
        if direction_action == Action.Left:
            player_input = 1 - self.player_relative_position[1]
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
            player_input = self.player_relative_position[1] 
            if len(items) > 0:
                item_input = items[0][1]
                item_input -= item_input // 1
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][1]
                obstacle_input -= obstacle_input // 1
            left = Action.Up
            right = Action.Down
        elif direction_action == Action.Up:
            player_input = self.player_relative_position[0] 
            if len(items) > 0:
                item_input = items[0][0]
                item_input -= item_input // 1
            if len(obstacles) > 0:
                obstacle_input = obstacles[0][0]
                obstacle_input -= obstacle_input // 1
            left = Action.Left
            right = Action.Right
        elif direction_action == Action.Down:
            player_input = 1 - self.player_relative_position[0] 
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

        self._fuzz_controller.input["player"] = player_input
        self._fuzz_controller.input["item"] = item_input
        self._fuzz_controller.input["obstacle"] = obstacle_input
        self._fuzz_controller.compute()
        out = self._fuzz_controller.output["output"]

        # print(direction_action, player_input, item_input, obstacle_input, out)

        action = direction_action
        if out < 0.45:
            action |= left
        elif out > 0.55:
            action |= right

        self._prev_action = action
        self.frame += 1
        return action

    def _cached(self, key, update_fn, refresh=False):
        if key in self._cache and not refresh:
            return self._cache[key]
        else:
            val = update_fn()
            self._cache[key] = val
            return val

    def _direction_to_tile(player_position, tile):
        xp, yp = player_position
        xt, yt = tile
        dx = round(xt - xp + 0.5, 2)
        dy = round(yt - yp + 0.5, 2)

        if abs(dx) > abs(dy):
            if dx > 0.3:
                return Action.Right
            if dx < -0.3:
                return Action.Left

        if dy > 0.3:
            return Action.Down
        if dy < -0.3 :
            return Action.Up

        return 0
