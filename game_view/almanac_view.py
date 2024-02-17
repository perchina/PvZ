import pygame
from time import time
from random import randint
from fun import *


class Plant:
    """创建一个具有植物标志的gif"""
    def __init__(self, setting):
        """初始化基本属性"""
        self.setting = setting
        self.width, self.height = (102, 105)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.index = 0
        self.image_list = self.setting.sunflower_shake
        self.last_plot_time = time()

    def update_image(self, interval_time=0.135):
        """从列表中按照正常顺序读取一帧"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, 5, 0, 0)

        current_time = time()
        if current_time - self.last_plot_time >= interval_time:
            self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
            self.last_plot_time = current_time


class Zombie:
    """创建一个具有僵尸标志的gif"""
    def __init__(self, setting):
        """初始化基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.0808, self.setting.screen_height * 0.22)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.index = 0
        self.image_list = self.setting.general_zombie_image_list[randint(0, 2)]
        self.last_plot_time = time()

    def update_image(self, interval_time=0.135):
        """从列表中按照正常顺序读取一帧"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, -self.setting.screen_width * 0.065, -
                   self.setting.screen_height * 0.03, 0)

        current_time = time()
        if current_time - self.last_plot_time >= interval_time:
            self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
            self.last_plot_time = current_time


class AlmanacView:
    """这是一个图鉴视图类"""
    def __init__(self, ai_game):
        """初始化图鉴属性"""
        self.screen = ai_game.main_screen
        self.setting = ai_game.setting
        self.sunflower = Plant(self.setting)
        self.general_zombie = Zombie(self.setting)
        self._load_almanac_background_image()
        self._load_check_plant_button()
        self._load_check_zombie_button()
        self._load_off_and_on_button()
        self._load_almanac_title()
        self.is_enter = False
        self.is_light = False
        self.plant_view_is_light = False

    def _load_almanac_background_image(self):
        """加载图鉴背景"""
        size = (self.setting.screen_width, self.setting.screen_height)
        image = pygame.image.load(self.setting.almanac_background)
        self.almanac = pygame.transform.scale(image, size)
        self.almanac_rect = self.almanac.get_rect()
        self.almanac_rect.topleft = (0, 0)

    def _load_check_plant_button(self):
        """设置具体的按钮样式"""
        size = (self.setting.screen_width * 0.16, self.setting.screen_height * 0.067)
        self.surface1 = pygame.Surface(size, pygame.SRCALPHA)
        self.rect1 = self.surface1.get_rect()
        image1 = pygame.image.load(self.setting.check_plant_button_dark)
        image2 = pygame.image.load(self.setting.check_plant_button_light)
        self.button_dark = pygame.transform.scale(image1, size)
        self.button_light = pygame.transform.scale(image2, size)
        self.button_rect = self.button_dark.get_rect()
        self.button_rect.topleft = (0, 0)
        self.rect1.topleft = (self.setting.screen_width * 0.187, self.setting.screen_height * 0.578)

    def _load_check_zombie_button(self):
        """设置具体的按钮样式"""
        size = (self.setting.screen_width * 0.16, self.setting.screen_height * 0.067)
        self.surface2 = pygame.Surface(size, pygame.SRCALPHA)
        self.rect2 = self.surface2.get_rect()
        image = pygame.image.load(self.setting.check_zombie_button)
        self.zombie_button = pygame.transform.scale(image, size)
        self.zombie_button_rect = self.zombie_button.get_rect()
        self.zombie_button_rect.topleft = (0, 0)
        self.rect2.topleft = (self.setting.screen_width * 0.66, self.setting.screen_height * 0.578)

    def _load_off_and_on_button(self):
        """设置具体的按钮样式"""
        size = (self.setting.screen_width * 0.08, self.setting.screen_height * 0.05)
        self.surface3 = pygame.Surface(size, pygame.SRCALPHA)
        self.rect3 = self.surface3.get_rect()
        image = pygame.image.load(self.setting.almanac_main_menu)
        self.off_button = pygame.transform.scale(image,
        (self.setting.screen_width * 0.08, self.setting.screen_height * 0.103))
        self.off_button_rect = self.off_button.get_rect()
        self.rect3.topleft = (self.setting.screen_width*0.88, self.setting.screen_height * 0.939)

    def _load_almanac_title(self):
        """设置具体的按钮样式"""
        size = (self.setting.screen_width * 0.76, self.setting.screen_height * 0.098)
        self.surface4 = pygame.Surface(size, pygame.SRCALPHA)
        self.rect4 = self.surface4.get_rect()
        image = pygame.image.load(self.setting.almanac_index)
        self.almanac_index = pygame.transform.scale(image, size)
        self.almanac_index_rect = self.zombie_button.get_rect()
        x = self.setting.screen_width / 2 - self.almanac_index.get_width() / 2
        self.almanac_index_rect.topleft = (0, 0)
        self.rect4.topleft = (x, self.setting.screen_height * 0.0325)

    def check_mouse_is_click_or_pass_main_menu(self, mouse_pos):
        """检查鼠标是否点击关闭按钮"""
        if self.rect3.collidepoint(mouse_pos):
            self.is_light = True
            return True
        else:
            self.is_light = False
            return False

    def check_mouse_is_click_or_pass_plant_view(self, mouse_pos):
        """检查鼠标是否移动或者点击到植物视图"""
        if self.rect1.collidepoint(mouse_pos):
            self.plant_view_is_light = True
            return True
        else:
            self.plant_view_is_light = False
            return False

    def plot_almanac_view(self):
        """在屏幕上绘制图鉴视图"""
        # 绘制背景和标题
        self.screen.blit(self.almanac, self.almanac_rect)
        # 绘制动态图像
        self.sunflower.update_image()
        self.general_zombie.update_image()

        # 绘制可检测的碰撞区域
        if self.plant_view_is_light:
            self.surface1.blit(self.button_light, (-1, -1))
        else:
            self.surface1.blit(self.button_dark, self.button_rect)
        self.surface2.blit(self.zombie_button, self.zombie_button_rect)
        if self.is_light:
            self.off_button_rect.bottomleft = (0, self.setting.screen_height * 0.0517)
        else:
            self.off_button_rect.topleft = (0, 0)
        self.surface3.blit(self.off_button, self.off_button_rect)
        self.surface4.blit(self.almanac_index, self.almanac_index_rect)
        # 所有元素绘制到屏幕上
        self.screen.blit(self.sunflower.surface,
                         (self.setting.screen_width * 0.222, self.setting.screen_height * 0.37))
        self.screen.blit(self.general_zombie.surface,
                         (self.setting.screen_width * 0.697, self.setting.screen_height * 0.35))
        self.screen.blit(self.surface1, self.rect1)
        self.screen.blit(self.surface2, self.rect2)
        self.screen.blit(self.surface3, self.rect3)
        self.screen.blit(self.surface4, self.rect4)
