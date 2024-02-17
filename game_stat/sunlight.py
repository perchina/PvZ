import pygame
from math import sin, cos, atan2
from time import time
from pygame.sprite import Sprite
from random import randint
from fun import *


class SunLight(Sprite):
    """创建一个具有植物标志的gif"""
    def __init__(self, ai_game):
        """初始化基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.main_screen
        self.music = ai_game.music
        self.path = self.setting.sun
        self.width, self.height = (self.setting.screen_width * 0.0707, self.setting.screen_width * 0.0707)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.x = randint(self.setting.low_limit_x, self.setting.high_limit_x)
        self.high_limit_y = randint(int(self.setting.screen_height * 0.337), self.setting.high_limit_y)
        self.rect.y = 0
        self.index = 0
        self.line_speed = 5  # 阳光直线速度
        self.move_x_value = 3
        self.alive_time_limit = 25  # 阳光落下后可以存在屏幕设置秒数
        self.image_list = self.setting.sunlight
        self.y = float(self.rect.y)
        self.alive_time = time()
        self.last_plot_time = 0
        self.y_limit = []  # 该空列表中包含一个（Ymin， Ymax）
        self.angle = 0  # 默认角度设置为0度
        self.direction = None
        self.is_click = False
        self.set_move = False  # 是否设置了移动轨迹
        self.is_up = True
        self.is_down = False

    def _move_on_line(self):
        """按照直线下坠运动"""
        if self.rect.y <= self.high_limit_y:
            self.y += self.setting.sun_speed
            self.rect.y = self.y

    def _move_on_fx(self):
        """先是直线往上，紧接着做抛物线运动"""
        if self.is_up:
            if self.rect.center[1] >= self.y_limit[0]:
                x = self.rect.center[0]
                y = self.rect.center[1] - self.line_speed
                self.rect.center = (x, y)
            else:
                self.is_up = False
                self.is_down = True
                # 当上升到指定位置后会随机将这个阳光往左或者往右边移动指定像素
                direction = randint(0, 1)
                if direction == 0:
                    self.direction = -self.move_x_value
                else:
                    self.direction = self.move_x_value
                x, y = self.rect.center
                x += self.direction
                self.rect.center = (x, y)
        elif self.is_down:
            if self.rect.center[1] <= self.y_limit[1]:
                x = self.rect.center[0]
                y = self.rect.center[1] + self.line_speed
                self.rect.center = (x, y)
            else:
                self.is_down = False

    def _update_sunlight_location(self):
        """实时更新阳光位置"""
        if not self.is_click:
            if self.set_move:
                self._move_on_fx()
            else:  # 默认直线往下运动
                self._move_on_line()
        else:
            x = float(self.rect.x)
            y = float(self.rect.y)
            if x >= 0:
                x -= int(self.setting.collect_sun_speed * cos(self.angle))
                self.rect.x = x
            if y >= 0:
                y -= int(self.setting.collect_sun_speed * sin(self.angle))
                self.rect.y = y

    def _update_image(self, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.setting.screen_width * 0.002, 0, 0)

        current_time = time()
        if current_time - self.last_plot_time >= interval_time:
            self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
            self.last_plot_time = current_time

    def check_is_click_sunlight(self, mouse_pos):
        """检查是否点击到了阳光"""
        if self.rect.collidepoint(mouse_pos) and not self.is_click:
            self.music.play_short_time_sound(self.setting.pick_sunlight)
            self.is_click = True
            self._work_angle()
            return True
        return False

    def draw_sunlight(self, pause):
        """更新并绘制阳光"""
        if not pause:
            self._update_image()
            self._update_sunlight_location()
        self.screen.blit(self.surface, self.rect)

    def _work_angle(self):
        """根据矩形此时的位置计算相应的角度"""
        self.angle = atan2(self.rect.y - 0, self.rect.x - 0)
