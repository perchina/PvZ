import pygame


class HomeLine:
    """僵尸不可以跨过的区域"""
    def __init__(self, ai_game):
        """"区域的基本属性"""
        self.screen = ai_game.surface
        self.setting = ai_game.setting
        self.width, self.height = (self.setting.screen_width * 0.027, self.setting.screen_height * 0.844)
        self.area_color = (0, 0, 0)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.area_rect = pygame.Rect(0, 0, self.width, self.height)
        self._set_align()

    def _set_align(self):
        """"设置矩形对齐相应的操作台"""
        # 用于查看每一个格子的碰撞面积：
        # pygame.draw.rect(self.surface, self.area_color, self.area_rect)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.2, self.setting.screen_height * 0.111)

    def plot_area(self):
        """"将区域画在屏幕上"""
        self.screen.blit(self.surface, self.rect)
