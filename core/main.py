from .game import Game


def main():
    g = Game()
    while g.running:
        g.new()
