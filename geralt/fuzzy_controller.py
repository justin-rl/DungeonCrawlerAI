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
    output = Consequent(np.linspace(0.0, 1.0, 100), "output")
    output.accumulation_method = np.fmax

    t1 = [0.0, 0.0, 0.4, 0.45]
    t2 = [0.4, 0.45, 0.55, 0.6]
    t3 = [0.55, 0.6, 1.0, 1.0]

    player["left"] = fuzz.trapmf(player.universe, t1)
    player["straight"] = fuzz.trapmf(player.universe, t2)
    player["right"] = fuzz.trapmf(player.universe, t3)

    output["left"] = fuzz.trapmf(output.universe, t1)
    output["straight"] = fuzz.trapmf(output.universe, t2)
    output["right"] = fuzz.trapmf(output.universe, t3)

    return ControlSystemSimulation(
        ControlSystem(
            rules=[
                Rule(antecedent=(player["straight"]), consequent=output["straight"]),
                Rule(antecedent=(player["left"]), consequent=output["right"]),
                Rule(antecedent=(player["right"]), consequent=output["left"]),
            ]
        )
    )
