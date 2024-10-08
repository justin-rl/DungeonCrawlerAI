# Simple interactive dungeon crawler
# This code was written for the AI courses in computer engineering at Université de Sherbrooke
# Author : Audrey Corbeil Therrien

import time
from matplotlib import pyplot as plt
import numpy as np
from Games2D import *
from geralt.geralt import Geralt

if __name__ == "__main__":
    game_app = App("assets/Mazes/mazeLarge_1")
    geralt = Geralt(game_app)
    game_app.on_execute(ai_action_callback=geralt.action)
