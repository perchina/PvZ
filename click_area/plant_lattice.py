import pygame
from pygame.sprite import Sprite


class Lattice(Sprite):
    """设置可以在屏幕上捕捉的区域"""
    def __init__(self, ai_game, width, height):
        """"区域的基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = (width, height)
        self.area_color = (0, 0, 0)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.line = 0  # 标记第几行
        self.cols = 0  # 标记第几列
        # 是否需要种植荷叶
        self.is_need_plant_lilypad = False
        # 是否需要种植盆栽
        self.is_need_plant_flower_pot = False
        self.don_t_plant = False
        self.is_plant = False

    def check_is_can_be_plant(self):
        """检测该格子是否能够被种植"""
        if not self.is_need_plant_lilypad:  # 已经种植了荷叶不需要再次种植
            return True
        elif not self.is_need_plant_flower_pot:  # 已经种植了花盆不需要再次种植
            return True
        elif not self.is_need_plant_lilypad and not self.is_need_plant_flower_pot:  # 既不需要种植花盆也不需要种植荷叶
            return True
        else:
            return True

    def reset_area_location(self, x, y):
        """根据新的坐标设置操作台对齐方式"""
        self.rect.bottomleft = (x, y)

    def plot_area(self):
        """"将区域画在屏幕上"""
        self.surface.fill((0, 0, 0))
        # self.surface.set_colorkey((0, 0, 0))
        self.screen.blit(self.surface, self.rect)


