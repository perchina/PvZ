from time import time

import pygame
from click_area.plant_lattice import Lattice
from tiny_car.car import Car
from fun import *


class Background:
    """这是一个背景类"""
    def __init__(self, ai_game):
        """地图初始属性"""
        self.ai_game = ai_game
        self.screen = ai_game.main_screen
        self.surface = ai_game.surface
        self.rect = ai_game.rect
        self.setting = ai_game.setting
        self.pool_day = self.setting.pool_day  # 白天的泳池
        self.pool_night = self.setting.pool_night  # 夜晚的泳池
        self.surface1 = pygame.Surface((900, 180))
        self.rect1 = self.surface1.get_rect()
        self._load_grass_day_background()
        self._load_grass_night_background()
        self._load_swimming_pool_day_background()
        self._load_swimming_pool_night_background()
        self._load_roof_day_background()
        self._load_roof_night_background()
        self.background_list = [self.grass_day_bg, self.grass_night_bg, self.swimming_pool_day_bg,
                                self.swimming_pool_night_bg, self.roof_day_bg, self.roof_night_bg]
        self._create_grass_click_lattice()
        self._create_swim_pool_click_lattice()
        self._create_roof_click_lattice()
        self._create_grass_cleaner()
        self._create_pool_cleaner()
        self._create_roof_cleaner()
        self.background = None
        self.pool = None
        self.lattices = None
        self.cars = None
        self.last_plot_time = 0
        self.index = 0
        self.interval_time = 0.25

    def _create_grass_cleaner(self):
        """创建草坪清洁者"""
        self.grass_cleaner_list = []
        x_start, y_start = (0, 160)
        y = y_start
        y_interval = 100
        for line in range(1, 6):
            new_car = Car(self.ai_game, 0)
            new_car.set_car_location((x_start, y))
            new_car.car_index = line
            y += y_interval
            self.grass_cleaner_list.append(new_car)

    def _create_pool_cleaner(self):
        """创建泳池清洁者"""
        self.pool_cleaner_list = []
        x_start, y_start = (0, 160)
        y = y_start
        y_interval = 90
        for line in range(1, 7):
            if line == 3 or line == 4:
                new_car = Car(self.ai_game, 1)
            else:
                new_car = Car(self.ai_game, 0)
            if line == 4:
                y_interval = 80
            new_car.set_car_location((x_start, y))
            new_car.car_index = line
            y += y_interval
            self.pool_cleaner_list.append(new_car)

    def _create_roof_cleaner(self):
        """创建屋顶清洁者"""
        self.roof_cleaner_list = []
        x_start, y_start = (0, 280)
        y = y_start
        y_interval = 80
        for line in range(1, 6):
            new_car = Car(self.ai_game, 2)
            new_car.set_car_location((x_start, y))
            new_car.car_index = line
            y += y_interval
            self.roof_cleaner_list.append(new_car)

    def _create_grass_click_lattice(self):
        """创建草坪上的种植区域"""
        self.grass_lattice_list = []
        lattice_size = (86, 89)
        x_start, y_start = (315, 160)
        x, y = (x_start, y_start)
        x_interval, y_interval = (15, 13)
        for rows in range(1, 6):
            for cols in range(1, 10):
                new_lattice = Lattice(self.ai_game, lattice_size[0], lattice_size[1])
                new_lattice.reset_area_location(x, y)
                new_lattice.line = rows
                new_lattice.cols = cols
                self.grass_lattice_list.append(new_lattice)
                x += x_interval + lattice_size[0]
            x = x_start
            y += y_interval + lattice_size[1]

    def _create_swim_pool_click_lattice(self):
        """创建泳池上的种植区域"""
        self.swim_pool_lattice_list = []
        lattice_size = (80, 70)
        x_start, y_start = (318, 160)
        x, y = (x_start, y_start)
        x_interval, y_interval = (20, 18)
        for line in range(1, 7):
            if line == 2:
                y_interval = 35
            elif line == 3:
                y_interval = 10
            elif line == 4 or line == 5:
                y_interval = 8

            else:
                y_interval = 18
            for cols in range(1, 10):
                new_lattice = Lattice(self.ai_game, lattice_size[0], lattice_size[1])
                new_lattice.reset_area_location(x, y)
                new_lattice.line = line
                new_lattice.cols = cols
                if line == 3 or line == 4:
                    new_lattice.is_need_plant_lilypad = True
                self.swim_pool_lattice_list.append(new_lattice)
                x += x_interval + lattice_size[0]
            x = x_start
            y += y_interval + lattice_size[1]

    def _create_roof_click_lattice(self):
        """创建屋顶上的种植区域"""
        self.roof_lattice_list = []
        lattice_size = (85, 80)
        x_start = 320
        x = x_start
        y_start = [290, 380, 465, 550, 640]
        y = y_start[0]
        x_interval, y_interval = (22, 18)
        for line in range(1, 6):
            for cols in range(1, 10):
                if cols < 6:
                    y -= 25
                    temp_y = y
                else:
                    temp_y = y - 5
                if cols < 4:
                    if cols == 1:
                        temp_y -= 5
                elif cols == 4:
                    temp_y += 10
                elif cols == 5:
                    temp_y += 15

                if cols == 1:
                    x_interval = 24
                elif cols == 2:
                    x_interval = 15
                elif cols == 4:
                    x_interval = 13
                elif cols == 5:
                    x_interval = 18
                elif cols == 6:
                    x_interval = 11
                new_lattice = Lattice(self.ai_game, lattice_size[0], lattice_size[1])
                new_lattice.reset_area_location(x, temp_y)
                new_lattice.line = line
                new_lattice.cols = cols
                new_lattice.is_need_plant_flower_pot = True
                self.roof_lattice_list.append(new_lattice)
                x += x_interval + lattice_size[0]
            x = x_start
            if line < 5:
                y = y_start[line]

    def _load_grass_day_background(self):
        """"游戏草坪白天背景"""
        image = pygame.image.load(self.setting.grass_day)
        self.grass_day_bg = (self._set_image_size
                             (image, self.setting.inner_screen_width, self.setting.inner_screen_height))

    def _load_grass_night_background(self):
        """"游戏草坪夜晚背景"""
        image = pygame.image.load(self.setting.grass_night)
        self.grass_night_bg = (self._set_image_size
                               (image, self.setting.inner_screen_width, 620))

    def _load_swimming_pool_day_background(self):
        """"游戏泳池白天背景"""
        image = pygame.image.load(self.setting.swimming_pool_day)
        self.swimming_pool_day_bg = (self._set_image_size
                                     (image, self.setting.inner_screen_width, self.setting.inner_screen_height))

    def _load_swimming_pool_night_background(self):
        """"游戏泳池夜晚背景"""
        image = pygame.image.load(self.setting.swimming_pool_night)
        self.swimming_pool_night_bg = (self._set_image_size
                                       (image, self.setting.inner_screen_width, self.setting.inner_screen_height))

    def _load_roof_day_background(self):
        """"游戏房顶白天背景"""
        image = pygame.image.load(self.setting.roof_day)
        self.roof_day_bg = (self._set_image_size
                            (image, self.setting.inner_screen_width, self.setting.inner_screen_height))

    def _load_roof_night_background(self):
        """"游戏房顶夜晚背景"""
        image = pygame.image.load(self.setting.roof_night)
        self.roof_night_bg = (self._set_image_size
                              (image, self.setting.inner_screen_width, self.setting.inner_screen_height))

    def _set_image_size(self, image, width, height, is_smooth=False):
        """设置图片大小并返回pygame图片对象"""
        if not is_smooth:
            return pygame.transform.scale(image, (width, height))
        else:
            return pygame.transform.smoothscale(image, (width, height))

    def draw_background(self):
        """根据要求绘制相应的背景"""
        self.surface.blit(self.background, (0, 0))
        self._plot_cars()
        self._plot_pool()
        self._plot_lattices()
        self.screen.blit(self.surface, self.rect)

    def select_background(self, index):
        """根据索引选择对应的地图"""
        self.pool = None
        self.index = 0
        self.background = self.background_list[index]
        if index == 0 or index == 1:
            self.lattices = self.grass_lattice_list
            self.cars = self.grass_cleaner_list
        elif index == 2 or index == 3:
            self.lattices = self.swim_pool_lattice_list
            self.cars = self.pool_cleaner_list
            if index == 2:
                self.pool = self.pool_day
            else:
                self.pool = self.pool_night
        elif index == 4 or index == 5:
            self.lattices = self.roof_lattice_list
            self.cars = self.roof_cleaner_list

    def _plot_cars(self):
        """在地图上绘制小腿车"""
        for car in self.cars:
            car.blit_car(self.ai_game.is_pause)

    def _plot_lattices(self):
        """绘制在地图上的格子"""
        for lattice in self.lattices:
            lattice.plot_area()

    def _plot_pool(self):
        """绘制泳池"""
        if self.pool:
            current_time = time()
            self.surface1.fill((255, 255, 255))
            self.surface1.set_colorkey((255, 255, 255))
            image = handle_index_error(self.pool, self.index)
            rect = image.get_rect()
            rect.topleft = (-10, -10)
            self.surface1.blit(image, rect)
            self.surface.blit(self.surface1, (320, 280))
            if not self.ai_game.is_pause:
                if current_time - self.last_plot_time >= self.interval_time:
                    self.index = (self.index + 1) % len(self.pool)
                    self.last_plot_time = current_time
