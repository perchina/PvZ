import random
import time

import pygame
from fun import *
from PIL import Image


class StaticZombie:
    """单个的静态僵尸类"""
    def __init__(self, surface, attribute):
        """静态僵尸基本呢属性"""
        self.screen = surface
        self._create_zombie(attribute)
        self.index = 0
        self.last_plot_time = 0
        self.x_limit = (1400, 1500)
        self.y_limit = (240, 580)

    def _create_zombie(self, attribute):
        """根据属性创建僵尸基本属性"""
        index = random.randint(0, len(attribute[0]) - 1)
        path = attribute[0][index]
        self.width, self.height = attribute[1]
        self.image_width, self.image_height = attribute[2]
        self.align_location = attribute[3]
        self.image_list = self._load_and_get_image(path, self.image_width, self.image_height)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()

    def _load_and_get_image(self, file_path, image_width, image_height):
        """"加载图片之后获取图片的每一帧"""
        image_list = []
        try:
            image = Image.open(file_path)
            while True:
                image.seek(len(image_list))  # 移动到指定帧，
                img = image.copy()  # 对指定的帧进行复制操纵
                img = img.convert("RGBA")  # 支持透明通道，即RGBA模式，没有它图像的第一帧会丢失
                pygame_image = pygame.image.fromstring(img.tobytes(), img.size, img.mode)  # 转换为pygame可识别的surface对象
                # 缩放Surface并显示
                pygame_image = self._set_image_size_or_style(pygame_image, image_width, image_height)
                image_list.append(pygame_image)
        except EOFError:
            pass
        return image_list

    def _set_image_size_or_style(self, original_image, width=270, height=200):
        """设置每张图片的尺寸"""
        return pygame.transform.scale(original_image, (width, height))

    def set_appear_location(self):
        """设置出现位置"""
        x = random.randint(self.x_limit[0], self.x_limit[1])
        y = random.randint(self.y_limit[0], self.y_limit[1])
        self.rect.bottomleft = (x, y)

    def plot_zombie(self, pause, interval_time=0.1):
        """绘制僵尸"""
        current_time = time.time()
        self.surface.fill((0, 255, 255))
        self.surface.set_colorkey((0, 255, 255))
        image = handle_index_error(self.image_list, self.index)
        rect = image.get_rect()
        rect.bottomleft = self.align_location
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)
        if not pause:  # 游戏在选择界面没有开始就绘制僵尸
            if current_time - self.last_plot_time >= interval_time:
                self.last_plot_time = current_time
                self.index = (self.index + 1) % len(self.image_list)


class StaticZombies:
    """所有的静态僵尸类"""
    def __init__(self, ai_game):
        """静态僵尸所属类基本属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.main_screen
        self.ai_game = ai_game
        self.inner_surface = ai_game.surface
        self.zombie_list = []
        self._create_static_zombie_list()
        self._sort_zombie_list()

    def _create_static_zombie_list(self):
        """创建静态僵尸列表"""
        for _ in range(5):
            zombie_list = []
            for zombie_attr in self.setting.zombie_static_attribute_list:
                new_zombie = StaticZombie(self.inner_surface, zombie_attr)
                new_zombie.set_appear_location()
                zombie_list.append(new_zombie)
            self.zombie_list.extend(zombie_list)
            zombie_list.clear()

    def _sort_zombie_list(self):
        """给僵尸按照从上往下的位置依次绘制，防止不合理绘制"""
        self.zombie_list = sorted(self.zombie_list, key=self._sort_by_bottom)

    def _sort_by_bottom(self, zombie):
        """返回僵尸底部的坐标"""
        return zombie.rect.center[1]

    def _check_game_is_start(self):
        """检测是否应该清除僵尸"""
        plant_cards = self.ai_game.plant_cards
        if plant_cards.check_button.is_arrive_location:
            self.zombie_list.clear()

    def blit_zombies(self, pause, coord):
        """绘制所有会出现的僵尸"""
        self._check_game_is_start()
        for index in range(0, len(self.zombie_list)-1):
            self.zombie_list[index].plot_zombie(pause)
        self.screen.blit(self.inner_surface, coord)
