import numpy as np
import skfuzzy as fuzz
from skfuzzy.control import (
    Consequent,
    Antecedent,
    ControlSystemSimulation,
    ControlSystem,
    Rule,
)


def create_fuzzy_controller():
    player = Antecedent(np.linspace(0.0, 1.0, 100), "player")
    # item = Antecedent(np.linspace(-1.0, 1.0, 200), "item")
    # obstacle = Antecedent(np.linspace(-1.0, 1.0, 200), "obstacle")
    output = Consequent(np.linspace(0.0, 1.0, 100), "output")
    output.accumulation_method = np.fmax

    t_none = [-1.0, -1.0, 0.0, 0.0]
    t_left = [0.0, 0.0, 0.2, 0.25]
    t_sw_left = [0.2, 0.25, 0.4, 0.45]
    t_straight = [0.43, 0.47, 0.53, 0.7]
    t_sw_right = [0.55, 0.6, 0.75, 0.8]
    t_right = [0.75, 0.8, 1.0, 1.0]

    player["left"] = fuzz.trapmf(player.universe, t_left)
    player["sw_left"] = fuzz.trapmf(player.universe, t_sw_left)
    player["center"] = fuzz.trapmf(player.universe, t_straight)
    player["sw_right"] = fuzz.trapmf(player.universe, t_sw_right)
    player["right"] = fuzz.trapmf(player.universe, t_right)

    # item["none"] = fuzz.trapmf(item.universe, t_none)
    # item["left"] = fuzz.trapmf(item.universe, t_left)
    # item["sw_left"] = fuzz.trapmf(item.universe, t_sw_left)
    # item["center"] = fuzz.trapmf(item.universe, t_straight)
    # item["sm_right"] = fuzz.trapmf(item.universe, t_sw_right)
    # item["right"] = fuzz.trapmf(item.universe, t_right)

    # obstacle["none"] = fuzz.trapmf(obstacle.universe, t_none)
    # obstacle["left"] = fuzz.trapmf(obstacle.universe, t_left)
    # obstacle["sw_left"] = fuzz.trapmf(obstacle.universe, t_sw_left)
    # obstacle["center"] = fuzz.trapmf(obstacle.universe, t_straight)
    # obstacle["sw_right"] = fuzz.trapmf(obstacle.universe, t_sw_right)
    # obstacle["right"] = fuzz.trapmf(obstacle.universe, t_right)

    output["left"] = fuzz.trapmf(output.universe, t_left)
    output["straight"] = fuzz.trapmf(output.universe, t_straight)
    output["right"] = fuzz.trapmf(output.universe, t_right)

    return ControlSystemSimulation(
        ControlSystem(
            rules=[
                Rule(antecedent=(player["left"] | player["sw_left"]), consequent=output["right"]),
                Rule(antecedent=(player["center"]), consequent=output["straight"]),
                Rule(antecedent=(player["right"] | player["sw_right"]), consequent=output["left"]),
            ]
        )
    )
