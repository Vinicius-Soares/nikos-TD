from .states import gameplay, menu, credits, gameover
from . import game

def main():
    app = game.Control()
    state_dict = {
        "MENU": menu.Menu(),
        "CREDITS": credits.Credits(),
        "GAMEPLAY": gameplay.Gameplay(),
        "GAMEOVER": gameover.Gameover()
    }
    app.state_machine.setup_states(state_dict, "MENU")
    app.main()
