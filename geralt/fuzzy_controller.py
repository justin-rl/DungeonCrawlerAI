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
    player = Antecedent(np.linspace(0.2, 0.8, 1000), "player")
    item = Antecedent(np.linspace(-1.0, 1.0, 2000), "item")
    obstacle = Antecedent(np.linspace(-1.0, 1.0, 2000), "obstacle")
    output = Consequent(np.linspace(0.0, 1.0, 1000), "output")
    output.accumulation_method = np.fmax

    t_none = [-1.0, -1.0, 0.0, 0.0]
    t_left = [0.0, 0.0, 0.4, 0.49]
    t_straight = [0.43, 0.47, 0.53, 0.57]
    t_right = [0.51, 0.6, 1.0, 1.0]

    player["left"] = fuzz.trapmf(player.universe, t_left)
    player["center"] = fuzz.trapmf(player.universe, t_straight)
    player["right"] = fuzz.trapmf(player.universe, t_right)

    item["none"] = fuzz.trapmf(item.universe, t_none)
    item["left"] = fuzz.trapmf(item.universe, t_left)
    item["center"] = fuzz.trapmf(item.universe, t_straight)
    item["right"] = fuzz.trapmf(item.universe, t_right)

    obstacle["none"] = fuzz.trapmf(obstacle.universe, t_none)
    obstacle["left"] = fuzz.trapmf(obstacle.universe, [0.0, 0.0, 0.49, 0.5])
    obstacle["center"] = fuzz.trimf(obstacle.universe, [0.49, 0.5, 0.51])
    obstacle["right"] = fuzz.trapmf(obstacle.universe, [0.5, 0.51, 1.0, 1.0])

    output["left"] = fuzz.trapmf(output.universe, t_left)
    output["straight"] = fuzz.trapmf(output.universe, t_straight)
    output["right"] = fuzz.trapmf(output.universe, t_right)

    return ControlSystemSimulation(
        ControlSystem(
            rules=[
                # Go around obstacle
                Rule(
                    antecedent=((obstacle["right"] | obstacle["center"])),
                    consequent=output["left"],
                ),
                Rule(antecedent=(obstacle["left"]), consequent=output["right"]),
                # Fetch Item (Straight) Put item without somewhat left and right
                Rule(
                    antecedent=(item["left"] & player["left"]),
                    consequent=output["straight"],
                ),
                Rule(
                    antecedent=(item["center"] & player["center"]),
                    consequent=output["straight"],
                ),
                Rule(
                    antecedent=(item["right"] & player["right"]),
                    consequent=output["straight"],
                ),
                # Fetch Item (Left)
                Rule(
                    antecedent=((item["center"] | item["left"])),
                    consequent=output["left"],
                ),
                # Fetch Item (Right)
                Rule(antecedent=(item["right"]), consequent=output["right"]),
                # Keep Center
                Rule(antecedent=(player["left"]), consequent=output["right"]),
                Rule(antecedent=(player["center"]), consequent=output["straight"]),
                Rule(antecedent=(player["right"]), consequent=output["left"]),
            ]
        )
    )
