import pygame
from pygame.sprite import Sprite


class Car(Sprite):
    """这是一个小推车设置类"""
    def __init__(self, ai_game, car_type):
        """初始化小推车属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.surface
        self.setting = ai_game.setting
        self.car_list = self.setting.tiny_car_list
        self.car_type = car_type
        self.width, self.height = (73, 60)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self._load_and_set_car()
        self.car_index = 0
        self.is_drive = False

    def _load_and_set_car(self):
        """"加载小推车外观"""
        self.car = self.car_list[self.car_type]
        self.car_rect = self.car.get_rect()
        x = self.width // 2 - self.car.get_width() // 2
        y = self.height //2 - self.car.get_height() // 2
        self.car_rect.topleft = (x, y)

    def set_car_location(self, coordinate):
        """"根据坐标确定小推车在屏幕上的位置"""
        self.rect.bottomright = coordinate

    def _moved_car(self):
        """"设置小推车的移动"""
        x = float(self.rect.x)
        x += self.setting.car_speed
        self.rect.x = x

    def _tiny_car_enter_flash(self):
        """小推车进入动画"""
        if self.rect.x <= self.setting.start_location:
            plant_cards = self.ai_game.plant_cards
            if plant_cards.check_button.is_arrive_location:
                x = float(self.rect.x)
                x += self.setting.car_speed
                self.rect.x = x

    def check_car_is_arrive_edge(self):
        """"检查小推车是否达到内部屏幕右边缘"""
        if self.rect.left >= self.setting.inner_screen_width:
            return True
        else:
            return False

    def blit_car(self, pause):
        """"在屏幕对应的位置上绘制小推车"""
        self.surface.fill((0, 255, 0))
        self.surface.set_colorkey((0, 255, 0))
        if self.is_drive and not pause:
            self._moved_car()
        self._tiny_car_enter_flash()
        self.surface.blit(self.car, self.car_rect)
        self.screen.blit(self.surface, self.rect)
