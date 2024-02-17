import pygame
from time import time
from pygame.sprite import Sprite
from random import randint
from game_stat.sunlight import SunLight
from .bullets import Pea, IcePea, FirePea
from fun import *


class GrowSoil:
    """飞溅的泥土"""
    def __init__(self, ai_game):
        """泥土基础属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (120, 50)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.index = 0
        self.image_list = self.setting.grow_soil
        self.last_plot_time = time()
        self.is_end_play = False
        self.is_play_plant_sound = False

    def draw_soil(self, pause, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        if not self.is_end_play:
            if not self.is_play_plant_sound:
                self.music.play_short_time_sound(self.setting.plant_sound_in_grass)
                self.is_play_plant_sound = True
            image = handle_index_error(self.image_list, self.index)
            self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
            self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
            plot_image(self.surface, image, 17, 18, 0)
            self.screen.blit(self.surface, self.rect)
            if self.index == len(self.image_list) - 1:
                self.is_end_play = True
        if not pause:
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time

    def reset_location(self, plant_mid_bottom):
        """将操作台的底部中央位置设置为传过来的对应坐标"""
        self.rect.midbottom = plant_mid_bottom


class GrowWater:
    """飞溅的水花"""
    def __init__(self, ai_game):
        """水花基础属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (120, 50)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.index = 0
        self.image_list = self.setting.grow_water
        self.last_plot_time = time()
        self.is_end_play = False
        self.is_play_plant_sound = False

    def draw_water(self, pause, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        if not self.is_end_play:
            if not self.is_play_plant_sound:
                self.music.play_short_time_sound(self.setting.plant_sound_in_pool)
                self.is_play_plant_sound = True
            image = handle_index_error(self.image_list, self.index)
            self.surface.fill((0, 0, 255))  # 该语句不可少，用于每次移除上一帧的图像
            self.surface.set_colorkey((0, 0, 255))  # 用于将操作台内指定的RGB颜色设置为透明色
            plot_image(self.surface, image, 17, 18, 0)
            self.screen.blit(self.surface, self.rect)
            if self.index == len(self.image_list) - 1:
                self.is_end_play = True
        if not pause:
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time

    def reset_location(self, plant_mid_bottom):
        """将操作台的底部中央位置设置为传过来的对应坐标"""
        self.rect.midbottom = plant_mid_bottom


class SunFlower(Sprite):
    """"创建向日葵"""
    def __init__(self, ai_game):
        """"向日葵基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.inner_rect = ai_game.rect
        self.music = ai_game.music
        self.sunlight = ai_game.sunlights
        self.width, self. height = (80, 85)
        self.index = 0
        self.count_frame = 0
        self.extra_index = 0
        self.health = 300
        self.light_time = 18  # 这里设置为当开始产生阳光时会播放后面亮起的帧数
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(self.ai_game)
        self.water = GrowWater(self.ai_game)
        self.shadow = self.setting.shadow
        self.surface1 = pygame.Surface((80, 60))
        self.rect1 = self.surface1.get_rect()
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.sunflower_shake
        self.last_plot_time = time()
        self.last_create_sunlight_time = 0
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.can_be_destroy = True
        self.is_light = False
        self.is_end_play = False
        self.is_create_extra_sunlight = False
        self.is_plant_just_now = True

    def check_is_create_sunlight(self):
        """根据时长产出阳光"""
        if self.is_plant_just_now:
            self._reset_create_sunlight_time()
            self.is_plant_just_now = False
        current_time = time()
        # if not self.is_create_extra_sunlight:
        #     self.extra_index = randint(1, 100)
        if current_time - self.last_create_sunlight_time >= 23:
            self.is_light = True
            if current_time - self.last_create_sunlight_time >= 24:
                self.music.play_short_time_sound(self.setting.pea_shoot)
                new_sunlight = SunLight(self.ai_game)
                new_sunlight.set_move = True
                # 设置阳光起始位置
                new_sunlight.rect.center = self._work_and_return_coordinate(self.rect.midbottom)
                x1 = randint(int(self.rect.left), int(self.rect.right))
                y1 = self.rect.center[1]
                x1, y1 = self._work_and_return_coordinate([x1, y1])
                new_sunlight.rect.center = (x1, y1)
                y_min = self.rect.top
                y_max = self.rect.bottom - 20
                new_sunlight.y_limit = (y_min, y_max)
                self.sunlight.add(new_sunlight)
                self.last_create_sunlight_time = current_time

    def _create_plant_shadow(self):
        """创建植物阴影"""
        self.surface1.fill((255, 255, 255))
        self.surface1.set_colorkey((255, 255,255))
        self.surface1.blit(self.shadow, (0, 0))
        self.rect1.bottomleft = (0, 100)

    def _reset_create_sunlight_time(self):
        """向日葵种下之后才计算产生阳光时间"""
        self.last_create_sunlight_time = time()

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 23, left + 67)
        self.attack_coord = (left + 67, top + 30)
        self.mid_bottom = (left + 42, top + 83)

    def _work_and_return_coordinate(self, coord):
        """根据接收的坐标返回一个实际坐标"""
        x, y = coord
        inner_screen = self.inner_rect
        current_x = inner_screen[0] + x
        current_y = inner_screen[1] + y
        c = (current_x, current_y)
        return c

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        x, y = lattice.rect.center
        self.rect.center = (x, y-2)
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause, interval_time=0.085):
        """"在屏幕上绘制向日葵"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((0, 0, 255))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 255))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.is_light:
            plot_image(self.surface, image, self.width/2 - image.get_width()/2, self.height)
            if self.count_frame == self.light_time:
                self.is_light = False
                self.count_frame = 0
        else:
            plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 2, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass
        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                if self.is_light:
                    self.count_frame += 1
                self.last_plot_time = current_time


class IceShooter(Sprite):
    """"创建寒冰射手"""
    def __init__(self, ai_game):
        """"寒冰射手基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (80, 90)
        self.index = 0
        self.health = 300
        self.fire_location_y = [25, 26, 27, 28, 29, 30]
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(self.ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.ice_shooter_shake
        self.last_fire_time = 0
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.can_be_destroy = True
        self.is_end_play = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        index = randint(0, len(self.fire_location_y) - 1)
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 25, left + 70)
        self.attack_coord = (left + 67, top + self.fire_location_y[index])
        self.mid_bottom = (left + 40, top + 77)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_bullet(self, index, current_time):
        """对该植物增加子弹"""
        if current_time - self.last_fire_time >= 1.4:
            new_bullet = IcePea(self.ai_game)
            new_bullet.reset_location(self)
            self.ai_game.bullets_lists[index].add(new_bullet)
            self.last_fire_time = current_time

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause, interval_time=0.085):
        """"在屏幕上绘制寒冰射手"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 10, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            self._update_plant_center_location()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time


class PeaShooter(Sprite):
    """"创建豌豆射手"""
    def __init__(self, ai_game):
        """"豌豆射手基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (86, 90)
        self.index = 0
        self.health = 300
        self.fire_location_y = [25, 26, 27, 28, 29, 30]
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(self.ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.pea_shooter_shake
        self.last_fire_time = 0
        self.fire_times = 0
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.can_be_destroy = True
        self.is_end_play = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x-10, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        index = randint(0, len(self.fire_location_y) - 1)
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 25, left + 70)
        self.attack_coord = (left + 64, top + self.fire_location_y[index])
        self.mid_bottom = (left + 40, top + 77)

    def add_bullet(self, index, current_time):
        """增加豌豆射手射出的豌豆"""
        if current_time - self.last_fire_time >= 1.4:  # 每1.4秒发射一个普通豌豆
            new_bullet = Pea(self.ai_game)
            new_bullet.reset_location(self)
            self.ai_game.bullets_lists[index].add(new_bullet)
            self.fire_times += 1
            self.last_fire_time = current_time
        elif self.fire_times % 5 == 4:  # 每隔四次发射一次火豌豆
            self.ai_game.music.play_short_time_sound(self.setting.pea_shoot)
            new_bullet = FirePea(self.ai_game)
            new_bullet.reset_location(self)
            self.ai_game.bullets_lists[index].add(new_bullet)
            self.fire_times = 0

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause, interval_time=0.085):
        """"在屏幕上绘制豌豆射手"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 10, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            self._update_plant_center_location()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time


class ManEatingFlower(Sprite):
    """"创建食人花"""
    def __init__(self, ai_game):
        """"食人花基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (120, 120)
        self.index = 0
        self.health = 300
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(ai_game)
        self.attack_times = 0
        self.attack_times_limit = 3
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.man_eating_flower_shake
        self.attack_image_list = self.setting.man_eating_flower_attack
        self.rest_image_list = self.setting.man_eating_flower_rest
        self.rest_start_time = 0
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        # 攻击状态
        self.is_attack = False
        # 休息状态
        self.is_rest = False
        # 是否播放到最后一帧
        self.is_end_play = False
        self.can_be_destroy = True

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        self.shadow_rect.topleft = (35, 107)

    def check_is_attack_zombies(self, zombies):
        """检测僵尸与食人花的位置然后移除僵尸"""
        for zombie in zombies:
            if not zombie.is_dead():
                plant_x_left = self.was_attacked_coord[0]
                zombie_x_center = zombie.attack_coord[0]
                if 0 <= zombie_x_center - plant_x_left <= 130:  # 检测是否有僵尸碰撞过来
                    if self.is_attack:  # 只有到了攻击状态时才会执行
                        if self.index == 7:  # 到了伤害帧才会移除僵尸
                            if not zombie.is_dead():  # 僵尸没有死亡才会移除
                                if self.attack_times < self.attack_times_limit:  # 攻击次数小于3
                                    self.music.play_short_time_sound(self.setting.big_chomp)
                                    zombies.remove(zombie)
                                    self.attack_times += 1
                                    return True  # 消灭了僵尸就会返回该值
                    # 检测到没有超过连击次数就设置为攻击状态
                    elif self.attack_times < self.attack_times_limit:
                        self.is_attack = True
                        self.index = 0
        return False

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 30, left + 75)
        self.attack_coord = (left + 75, top + 65)
        self.mid_bottom = (left + 32, top + 103)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.bottomleft = lattice.rect.bottomleft
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause, interval_time=0.15):
        """"在屏幕上绘制食人花"""
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if not self.is_attack and not self.is_rest:
            image = handle_index_error(self.image_list, self.index)
            plot_image(self.surface, image, 0, 7, 0)
        elif self.is_attack:
            image = handle_index_error(self.attack_image_list, self.index)
            plot_image(self.surface, image, 0, 7, 0)
        elif self.is_rest:
            image = handle_index_error(self.rest_image_list, self.index)
            plot_image(self.surface, image, 0, 7, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if not self.is_attack and not self.is_rest:
                    self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                elif self.is_attack:
                    self.index += 1
                    if self.index == len(self.attack_image_list):  # 已经播放完最后一帧
                        self.is_attack = False
                        self.index = 0
                        if self.attack_times == self.attack_times_limit and not self.is_rest:  # 确定是否已经攻击了三次
                            self.rest_start_time = time()
                            self.is_rest = True
                elif self.is_rest:
                    self.index = (self.index + 1) % len(self.rest_image_list)
                    if current_time - self.rest_start_time >= 20:
                        self.is_rest = False
                        self.attack_times = 0
                        self.index = 0
                self.last_plot_time = current_time


class WallNut(Sprite):
    """"创建坚果墙"""
    def __init__(self, ai_game):
        """"坚果墙基本属性"""
        super().__init__()
        self
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (85, 90)
        self.index = 0
        self.health = 4000
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.potato_shake
        self.image_list1 = self.setting.potato_half_health_shake
        self.image_list2 = self.setting.potato_zero_health_shake
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.can_be_destroy = True
        self.is_end_play = False
        self.health_is_about_two_thirds = False
        self.health_is_about_one_thirds = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 10, left + 75)
        self.attack_coord = (left + 45, top + 45)
        self.mid_bottom = (left + 45, top + 82)

    def check_health_status(self):
        """检查小土豆的生命状态"""
        if self.health <= 2666 and not self.health_is_about_two_thirds:
            self.health_is_about_two_thirds = True
            self.index = 0
        elif self.health <= 1333 and not self.health_is_about_one_thirds:
            self.health_is_about_one_thirds = True
            self.index = 0

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause,  interval_time=0.075):
        """"在屏幕上绘制坚果墙"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.health_is_about_two_thirds and not self.health_is_about_one_thirds:
            image = handle_index_error(self.image_list1, self.index)
            plot_image(self.surface, image, 5, 0, 0)
        elif self.health_is_about_two_thirds and self.health_is_about_one_thirds:
            image = handle_index_error(self.image_list2, self.index)
            plot_image(self.surface, image, 5, 0, 0)
        else:
            image = handle_index_error(self.image_list, self.index)
            plot_image(self.surface, image, 5, 0, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.health_is_about_two_thirds and not self.health_is_about_one_thirds:
                    self.index = (self.index + 1) % len(self.image_list1)
                elif self.health_is_about_one_thirds and self.health_is_about_two_thirds:
                    self.index = (self.index + 1) % len(self.image_list2)
                else:
                    self.index = (self.index + 1) % len(self.image_list)
                self.last_plot_time = current_time


class Cherry(Sprite):
    """"创建樱桃炸弹"""
    def __init__(self, ai_game):
        """"樱桃基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (300, 300)
        self.index = 0
        self.health = 300
        self.row_cols = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(ai_game)
        self.hurt = 1800
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.cherry_grown
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.is_work_hurt = False
        self.is_end_play = False
        self.can_be_destroy = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height - 20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height + 25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.mid_bottom = (left + 150, top + 185)

    def _update_zombies_appearance_boom(self, start, end):
        """根据索引响应所碰撞的僵尸精灵组"""
        plant_x_left = self.rect.topleft[0]
        plant_x_right = self.rect.topright[0]
        for line in range(start, end):
            zombies_collide = []
            for zombie_c in self.ai_game.zombies_lists[line]:
                zombie_center = zombie_c.was_attacked_coord[0]
                if plant_x_left <= zombie_center <= plant_x_right:
                    zombies_collide.append(zombie_c)
            for zombie in zombies_collide:
                zombie.update_zombie_health(self.hurt, False)
                if zombie.is_dead() and not zombie.was_shot_to_die and not zombie.was_boom_to_die:
                    zombie.was_boom_to_die = True
                    zombie.index = 0
        self.is_work_hurt = False  # 计算完所有的碰撞僵尸生命值后将重置伤害状态

    def check_ashes_plants_and_zombies_collide(self, index, sound):
        """检测樱桃炸弹与僵尸的碰撞"""
        self.ai_game.music.play_short_time_sound(sound)
        if index == 0:
            self._update_zombies_appearance_boom(0, 2)
        elif index == 1:
            self._update_zombies_appearance_boom(0, 3)
        elif index == 2:
            self._update_zombies_appearance_boom(1, 4)
        elif index == 3:
            self._update_zombies_appearance_boom(2, 5)
        elif index == 4:
            self._update_zombies_appearance_boom(3, 5)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def show_plant(self, pause,  interval_time=0.03):
        """"在屏幕上绘制樱桃雷"""
        image = handle_index_error(self.image_list, self .index)
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色

        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2,
                        self.height / 2 - image.get_height() / 2, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time
                if self.index == 7 or self.index == 20 or self.index == 33:
                    self.is_work_hurt = True
                if self.index == 45:
                    self.is_end_play = True


class Clover(Sprite):
    """"创建三叶草"""
    def __init__(self, ai_game):
        """"三叶草基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (110, 120)
        self.index = 0
        self.health = 300
        self.row_cols = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.clover_shake
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.is_end_play = False
        self.can_be_destroy = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.mid_bottom = (left + 55, top + 95)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def show_plant(self, pause,  interval_time=0.085):
        """"在屏幕上绘制三叶草"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 0, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time


class FourPea(Sprite):
    """"创建机枪射手"""
    def __init__(self, ai_game):
        """机枪射手基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (85, 90)
        self.index = 0
        self.health = 300
        self.fire_location_y = [26, 27, 28, 29, 30, 31]
        self.row_cols = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(self.ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.four_pea_shooter_shake
        self.last_fire_time = 0  # 上一次开始开火的时间
        self.bullet_interval_time = 0  # 每一颗子弹间隔的时间
        self.pea_pieces = 0
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.no_fire = False
        self.is_end_play = False
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.can_be_destroy = True

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        index = randint(0, len(self.fire_location_y) - 1)
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 20, left + 65)
        self.attack_coord = (left + 65, top + self.fire_location_y[index])
        self.mid_bottom = (left + 37, top + 77)

    def add_bullet(self, index, current_time):
        """增加机枪射手的子弹"""
        if self.pea_pieces % 5 == 4:
            self.no_fire = True
            self.last_fire_time = current_time
            self.pea_pieces = 0
        elif not self.no_fire:
            if current_time - self.bullet_interval_time >= 0.1:
                new_bullet = FirePea(self.ai_game)
                new_bullet.reset_location(self)
                self.ai_game.bullets_lists[index].add(new_bullet)
                self.pea_pieces += 1
                self.bullet_interval_time = current_time
        elif current_time - self.last_fire_time >= 1.4:
            self.no_fire = False
            self.bullet_interval_time = 0

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause,  interval_time=0.085):
        """"在屏幕上绘制机枪射手"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((0, 0, 255))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 255))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 0, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            self._update_plant_center_location()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time


class ThreePea(Sprite):
    """"创建三线射手"""
    def __init__(self, ai_game):
        """"三线射手基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self. height = (85, 90)
        self.index = 0
        self.health = 300
        self.fire_location_y = [38, 39, 40, 41, 42, 43]
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.row_cols = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(self.ai_game)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        # 僵尸攻击该植物的列表
        self.zombie_list = []
        self.image_list = self.setting.three_pea_shooter_shake
        self.last_fire_time = 0  # 上一次开始开火的时间
        self.bullet_interval_time = 0  # 每一颗子弹间隔的时间
        self.pea_pieces = 0  # 打出的豌豆颗数
        self.last_plot_time = time()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.no_fire = False
        self.is_end_play = False
        self.can_be_destroy = True

    def _add_multi_bullets_by_rand(self):
        """随机弹出一个子弹"""
        index = randint(0, len(self.ai_game.bullet_list) - 1)
        new_bullet = self.ai_game.bullet_list.pop(index)
        if index == 0:
            self.ai_game.bullet_list.insert(index, Pea(self.ai_game))
        elif index == 1:
            self.ai_game.bullet_list.insert(index, IcePea(self.ai_game))
        elif index == 2:
            self.ai_game.bullet_list.insert(index, FirePea(self.ai_game))
        return new_bullet

    def _add_peas_by_three_pea(self, index):
        """根据三线射手所处的位置在相对应的行增加三发或者两发豌豆"""
        plant_mid = self.attack_coord[1]  # 三线射手所处在的中心位置
        distance = 100  # 上下子弹与中间子弹的间距
        if index == 0:
            self._check_line_and_add_pea(0, 2, plant_mid-distance,  plant_mid)
        elif index == 1:
            self._check_line_and_add_pea(0, 3, plant_mid-distance, plant_mid, plant_mid+distance)
        elif index == 2:
            self._check_line_and_add_pea(1, 4, plant_mid-distance, plant_mid, plant_mid+distance)
        elif index == 3:
            self._check_line_and_add_pea(2, 5, plant_mid-distance, plant_mid, plant_mid+distance)
        elif index == 4:
            self._check_line_and_add_pea(3, 5, plant_mid-distance, plant_mid)

    def _check_line_and_add_pea(self, start, end, *y_list):
        """在对应的行中增加豌豆"""
        i = 0
        for num in range(start, end):
            bullet = self._add_multi_bullets_by_rand()
            bullet.reset_location(self, y=y_list[i])
            self.ai_game.bullets_lists[num].add(bullet)
            i += 1

    def _check_zombies_is_arrive(self, zombies, plant=None):
        """检测僵尸是否到达了指定位置"""
        # 仅对子弹类植物做此判断
        if not plant:
            for zombie in zombies:
                if zombie.attack_coord[0] <= self.setting.fire_distance:  # 这一行僵尸已经到了攻击范围内
                    return True
        else:
            for zombie in zombies:
                if plant.attack_coord[0] < zombie.attack_coord[0] <= self.setting.fire_distance:  # 这一行僵尸已经到了攻击范围内
                    if not zombie.was_shot_to_die and not zombie.was_boom_to_die:
                        # 并且僵尸走在植物的前面没有死亡
                        return True
        return False

    def check_zombies_is_appear_in_other_line(self, index):
        """检查在其它行中是否存在僵尸"""
        if index == 0:
            if self._check_zombies_is_arrive(self.ai_game.zombies_lists[1], self):
                return True
        elif index == 1:
            if self._check_zombies_is_arrive(self.ai_game.zombies_lists[0], self):
                return True
            elif self._check_zombies_is_arrive(self.ai_game.zombies_lists[2], self):
                return True
        elif index == 2:
            if self._check_zombies_is_arrive(self.ai_game.zombies_lists[1], self):
                return True
            elif self._check_zombies_is_arrive(self.ai_game.zombies_lists[3], self):
                return True
        elif index == 3:
            if self._check_zombies_is_arrive(self.ai_game.zombies_lists[2], self):
                return True
            elif self._check_zombies_is_arrive(self.ai_game.zombies_lists[4], self):
                return True
        elif index == 4:
            if self._check_zombies_is_arrive(self.ai_game.zombies_lists[3], self):
                return True
        else:
            return False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        index = randint(0, len(self.fire_location_y) - 1)
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 30, left + 73)
        self.attack_coord = (left + 55, top + self.fire_location_y[index])
        self.mid_bottom = (left + 42, top + 82)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.rect.center = lattice.rect.center
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)

    def add_bullet(self, index, current_time):
        """增加三线射手发出的子弹"""
        if self.pea_pieces % 3 == 2:
            self.no_fire = True
            self.last_fire_time = current_time
            self.pea_pieces = 0
        elif not self.no_fire:
            if current_time - self.bullet_interval_time >= 0.1:
                self._add_peas_by_three_pea(index)
                self.pea_pieces += 1
                self.bullet_interval_time = current_time
        elif current_time - self.last_fire_time >= 1.4:
            self.no_fire = False
            self.bullet_interval_time = 0

    def add_zombie_to_attack_list(self, zombie):
        """将攻击该植物的僵尸增加到列表中"""
        self.zombie_list.append(zombie)

    def clear_zombies_status(self):
        """清除正攻击该植物的僵尸状态"""
        if self.zombie_list:
            for zombie in self.zombie_list:
                zombie.is_touch_plant = False
                zombie.is_attack_plant = False
                zombie.index = 0

    def show_plant(self, pause,  interval_time=0.085):
        """"在屏幕上绘制三线射手"""
        image = handle_index_error(self.image_list, self.index)
        self.surface.fill((255, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((255, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        plot_image(self.surface, image, self.width / 2 - image.get_width() / 2, 5, 0)
        self.screen.blit(self.surface, self.rect)
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            self._update_plant_center_location()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time


class Pepper(Sprite):
    """"创建火爆辣椒"""
    def __init__(self, ai_game):
        """"辣椒基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.screen_rect = self.screen.get_rect()
        self.width, self. height = (920, 270)
        self.small_width, self.small_height = (90, 120)
        self.index = 0
        self.health = 300
        self.row_cols = ()
        self.mid_bottom = ()
        self.soil = GrowSoil(ai_game)
        self.water = GrowWater(self.ai_game)
        self.line = -1
        self.hurt = 1800
        self.fire1 = None
        self.fire2 = None
        self.fire3 = None
        # surface对齐位置
        self.surface_location_list = [(310, -10), (310, 91), (310, 191), (310, 292), (310, 392)]
        # 火焰对齐位置
        self.fire_location_list = [(0, 90), (0, 180), (0, 270)]
        self.small_surface = pygame.Surface((self.small_width, self.small_height))
        self.small_rect = self.small_surface.get_rect()
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.pepper_grown
        self.fire_image_list = self.setting.pepper_fire_burn
        self.last_plot_time = time()
        self._create_plant_shadow()
        self.is_in_grass = False
        self.is_in_pool = False
        self.is_in_roof = False
        self.is_work_hurt = False
        self.pepper_is_end_play = False  # 辣椒是否结束播放
        self.is_end_play = False
        self.can_be_destroy = False

    def _create_plant_shadow(self):
        """"创建植物阴影"""
        width, height = (80, 60)
        image = pygame.image.load(self.setting.plant_shadow)
        self.plant_shadow = pygame.transform.smoothscale(image, (width, height-20)).convert_alpha()
        self.shadow_rect = self.plant_shadow.get_rect()
        x = self.width / 2 - width / 2
        self.shadow_rect.topleft = (x, height+25)

    def _update_plant_center_location(self):
        """实时更新植物的中心位置"""
        small_left, small_top = self.small_rect.left, self.small_rect.top
        self.mid_bottom = (small_left + 37, small_top + 100)

    def _update_zombies_appearance_boom(self, start, end):
        """根据索引响应所碰撞的僵尸精灵组"""
        plant_x_left = self.rect.topleft[0]
        plant_x_right = self.rect.topright[0]
        for line in range(start, end):
            zombies_collide = []
            for zombie_c in self.ai_game.zombies_lists[line]:
                zombie_center = zombie_c.was_attacked_coord[0]
                if plant_x_left <= zombie_center <= plant_x_right:
                    zombies_collide.append(zombie_c)
            for zombie in zombies_collide:
                zombie.update_zombie_health(self.hurt, False)
                if zombie.is_dead() and not zombie.was_shot_to_die and not zombie.was_boom_to_die:
                    zombie.was_boom_to_die = True
                    zombie.index = 0
        self.is_work_hurt = False  # 计算完所有的碰撞僵尸生命值后将重置伤害状态

    def check_ashes_plants_and_zombies_collide(self, index, sound):
        """检测樱桃炸弹与僵尸的碰撞"""
        self.ai_game.music.play_short_time_sound(sound)
        if index == 0:
            self._update_zombies_appearance_boom(0, 2)
        elif index == 1:
            self._update_zombies_appearance_boom(0, 3)
        elif index == 2:
            self._update_zombies_appearance_boom(1, 4)
        elif index == 3:
            self._update_zombies_appearance_boom(2, 5)
        elif index == 4:
            self._update_zombies_appearance_boom(3, 5)

    def reset_surface_coordinate(self, lattice):
        """根据程序重新设置操作台在屏幕上的位置"""
        self.small_rect.bottomleft = lattice.rect.bottomleft
        self._update_plant_center_location()
        self.soil.reset_location(self.mid_bottom)
        self.water.reset_location(self.mid_bottom)
        if lattice.line == 1:
            self.rect.topleft = (self.surface_location_list[0][0], self.surface_location_list[0][1])
        elif lattice.line == 2:
            self.rect.topleft = (self.surface_location_list[1][0], self.surface_location_list[1][1])
        elif lattice.line == 3:
            self.rect.topleft = (self.surface_location_list[2][0], self.surface_location_list[2][1])
        elif lattice.line == 4:
            self.rect.topleft = (self.surface_location_list[3][0], self.surface_location_list[3][1])
        elif lattice.line == 5:
            self.rect.topleft = (self.surface_location_list[4][0], self.surface_location_list[4][1])
        self.line = lattice.line
        self._set_fire_burn_location(self.line)

    def _set_fire_burn_location(self, line):
        """根据格子的位置设置火焰燃烧的位置"""
        # 以下位置都在火焰的左下方生效
        if line == 1:
            self.fire2 = self.fire_location_list[1]
            self.fire3 = self.fire_location_list[2]
        elif line == 2:
            self.fire1 = self.fire_location_list[0]
            self.fire2 = self.fire_location_list[1]
            self.fire3 = self.fire_location_list[2]
        elif line == 3:
            self.fire1 = self.fire_location_list[0]
            self.fire2 = self.fire_location_list[1]
            self.fire3 = self.fire_location_list[2]
        elif line == 4:
            self.fire1 = self.fire_location_list[0]
            self.fire2 = self.fire_location_list[1]
            self.fire3 = self.fire_location_list[2]
        if line == 5:
            self.fire1 = self.fire_location_list[0]
            self.fire2 = self.fire_location_list[1]

    def _show_burned_fire(self, image):
        """绘制燃烧的火焰"""
        rect = image.get_rect()
        if self.line == 1:
            rect.bottomleft = self.fire2
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire3
            self.surface.blit(image, rect)
        elif self.line == 2:
            rect.bottomleft = self.fire1
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire2
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire3
            self.surface.blit(image, rect)
        elif self.line == 3:
            rect.bottomleft = self.fire1
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire2
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire3
            self.surface.blit(image, rect)
        elif self.line == 4:
            rect.bottomleft = self.fire1
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire2
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire3
            self.surface.blit(image, rect)
        if self.line == 5:
            rect.bottomleft = self.fire1
            self.surface.blit(image, rect)
            rect.bottomleft = self.fire2
            self.surface.blit(image, rect)

    def show_plant(self, pause,  interval_time=0.05):
        """"在屏幕上绘制辣椒"""
        if not self.pepper_is_end_play:
            image = handle_index_error(self.image_list, self.index)
            self.small_surface.fill((0, 255, 0))
            self.small_surface.set_colorkey((0, 255, 0))
            plot_image(self.small_surface, image, self.small_width / 2 - image.get_width() / 2,
                            self.small_height / 2 - image.get_height() / 2, 0)
            self.screen.blit(self.small_surface, self.small_rect)
            if self.index == 7:  # 播放到最后一帧后重置索引
                self.index = 0
                self.pepper_is_end_play = True
        else:
            image = handle_index_error(self.fire_image_list, self.index)
            self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
            self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
            self._show_burned_fire(image)
            self.screen.blit(self.surface, self.rect)
            if self.index == 7:  # 播放到最后一帧后重置索引
                self.index = 0
                self.is_end_play = True
        if self.is_in_grass:
            if not self.soil.is_end_play:
                self.soil.draw_soil(pause)
        elif self.is_in_pool:
            if not self.water.is_end_play:
                self.water.draw_water(pause)
        elif self.is_in_roof:
            pass

        if not pause:  # 植物只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if not self.pepper_is_end_play:
                    self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路

                else:
                    self.index = (self.index + 1) % len(self.fire_image_list)
                    if self.index == 2:
                        self.is_work_hurt = True

                self.last_plot_time = current_time
