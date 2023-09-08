
from Games2D import Action
from geralt.input import Input

class Geralt:
    def __init__(self, game_app) -> None:
        self.input = Input(game_app)

    def action(self): 
        x, y = self.input.player_position()
        print(f"Player Position: x:{round(x, 5)}, y:{round(y, 5)}")
        return Action.DOWN | Action.RIGHT