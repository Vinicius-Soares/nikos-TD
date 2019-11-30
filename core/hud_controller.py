import pygame as pg

class HudController(object):
    def __init__(self):
        self.match_hud = MatchHud()
        self.tower_hud = TowerHud()

    def reset(self):
        self.tower_hud.reset()

    def initialize(self, money):
        self.match_hud.update_money(money)

    def click_on_any_hud(self, x, y):
        return self.match_hud.click_on_it(x, y) or \
            self.tower_hud.click_on_it(x, y)

    def show_tower_hud(self, tower):
        self.tower_hud.set_tower(tower)

    def update(self, now):
        self.match_hud.update(now)
        self.tower_hud.update(now)

    def draw(self, surface):
        self.match_hud.draw(surface)
        self.tower_hud.draw(surface)


class _Hud(object):
    def __init__(self, x, y, width, length):
        self.screen = pg.Surface((width, length))
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.topleft = (x, y)
        self.color = 0

    def click_on_it(self, x, y):
        return self.screen_rect.collidepoint(x, y)

    def update(self, now):
        pass

    def draw(self, surface):
        self.screen.fill(self.color)
        surface.blit(self.screen, self.screen_rect.topleft)


class MatchHud(_Hud):
    def __init__(self):
        super().__init__(0, 0, 1024, 64)
        self.color = (0, 255, 0)
        self.life = 0
        self.time = 0
        self.money = 0

    def update_money(self, value):
        # Usado para comprar torres também
        # Ex: hud_controller.update_money(-cost), 
        # onde cost é o custo da torre
        self.money += value

    def click_on_it(self, x, y):
        return super().click_on_it(x, y)

    def update(self, now):
        super().update(now)

    def draw(self, surface):
        super().draw(surface)


class TowerHud(_Hud):
    def __init__(self):
        super().__init__(0, 64 * 8, 1024, 64 * 4)
        self.show = False
        self.tower = None

    def reset(self):
        self.show = False

    def set_tower(self, tower):
        self.show = True
        self.tower = tower
        self.color = (255, 0, 0) if self.tower else (0, 0, 255)
        
    def click_on_it(self, x, y):
        return self.show and super().click_on_it(x, y)

    def update(self, now):
        super().update(now)

    def draw(self, surface):
        if self.show: 
            super().draw(surface)
