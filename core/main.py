from .states import gameplay, menu
from . import game

def main():
    app = game.Control()
    state_dict = {
        "MENU": menu.Menu(),
        "GAMEPLAY": gameplay.Gameplay()
    }
    app.state_machine.setup_states(state_dict, "MENU")
    app.main()
