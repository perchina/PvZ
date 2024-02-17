import pygame
from time import time
from pygame.sprite import Sprite
from random import randint
from fun import *


def take_and_back_zombie(ai_game, line, x, y):
    """拿走然后放回僵尸"""
    index = randint(0, (len(ai_game.zombie_list) - 1))
    new_zombie = ai_game.zombie_list.pop(index)
    new_zombie.lattice_index = line
    new_zombie.reset_location(x, y)
    new_zombie.is_invincible = True
    new_zombie.was_called = True
    if new_zombie.lattice_index == 0:
        ai_game.zombies_lists[0].add(new_zombie)
    elif new_zombie.lattice_index == 1:
        ai_game.zombies_lists[1].add(new_zombie)
    elif new_zombie.lattice_index == 2:
        ai_game.zombies_lists[2].add(new_zombie)
    elif new_zombie.lattice_index == 3:
        ai_game.zombies_lists[3].add(new_zombie)
    elif new_zombie.lattice_index == 4:
        ai_game.zombies_lists[4].add(new_zombie)

    if index == 0:
        ai_game.zombie_list.insert(index, GeneralZombie(ai_game))
    elif index == 1:
        ai_game.zombie_list.insert(index, FlagZombie(ai_game))
    elif index == 2:
        ai_game.zombie_list.insert(index, RoadBlockZombie(ai_game))
    elif index == 3:
        ai_game.zombie_list.insert(index, DrumZombie(ai_game))
    elif index == 4:
        ai_game.zombie_list.insert(index, FootballZombie(ai_game))
    elif index == 5:
        ai_game.zombie_list.insert(index, PoleVaultZombie(ai_game))
    elif index == 6:
        ai_game.zombie_list.insert(index, IceCarZombie(ai_game))
    elif index == 7:
        ai_game.zombie_list.insert(index, ImpZombie(ai_game))
    elif index == 8:
        ai_game.zombie_list.insert(index, ClownZombie(ai_game))
    elif index == 9:
       ai_game.zombie_list.insert(index, ScreenDoorZombie(ai_game))
    elif index == 10:
        ai_game.zombie_list.insert(index, NewspaperZombie(ai_game))
    elif index == 11:
        ai_game.zombie_list.insert(index, SnorkelZombie(ai_game))
    elif index == 12:
        ai_game.zombie_list.insert(index, DolphinRiderZombie(ai_game))
    elif index == 13:
        ai_game.zombie_list.insert(index, DuckyDrumZombie(ai_game))
    elif index == 14:
        ai_game.zombie_list.insert(index, DuckyRoadBlockZombie(ai_game))
    elif index == 15:
        ai_game.zombie_list.insert(index, DuckyGeneralZombie(ai_game))
    elif index == 16:
        ai_game.zombie_list.insert(index, DancingZombie(ai_game))
    elif index == 17:
        ai_game.zombie_list.insert(index, BuckupDancerZombie(ai_game))


class ZombieAppearSoil:
    """僵尸出现时冒出的泥土"""
    def __init__(self, ai_game):
        """泥土初始化类"""
        self.setting = ai_game.setting
        self.music = ai_game.music
        self.screen = ai_game.surface
        self.width, self.height = (100, 70)
        self.index = 0
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.zombie_appear_soil
        self.last_plot_time = time()
        self.is_end_play = False
        self.is_play_one_frame = True
        self.is_play_appear_sound = False

    def set_surface_location(self, coord):
        """将这个矩形的底部位置对准僵尸矩形的底部中央位置"""
        self.rect.midbottom = coord

    def show_soil(self, pause, interval_time=0.08):
        """"在屏幕上绘制往上冒的泥土"""
        if not self.is_end_play:
            if not self.is_play_appear_sound:
                self.music.play_short_time_sound(self.setting.dirt_rise)
                self.is_play_appear_sound = True
            self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
            self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
            image = handle_index_error(self.image_list, self.index)
            plot_image(self.surface, image, -2, self.height)
            self.screen.blit(self.surface, self.rect)
            if self.index == len(self.image_list) - 1:
                self.is_end_play = True
            if self.is_play_one_frame:
                self.is_play_one_frame = False
            if not pause:  # 僵尸只有在非暂停状态时才更新动作
                current_time = time()
                if current_time - self.last_plot_time >= interval_time:
                    if self.index < len(self.image_list) - 1:
                        self.index = (self.index + 1) % len(self.image_list)
                        self.is_play_one_frame = True
                    self.last_plot_time = current_time


class FlyingZombieHead:
    """飞翔的脑袋"""
    def __init__(self, ai_game, *surface_size):
        """"普通僵尸基本属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = surface_size
        self.index = 0
        self.die_after_stay_time = 1.5  # 死亡之后停留两秒
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.flying_head
        self.last_plot_time = time()
        self.dead_time = 0  # 死亡时间
        self.name = '脑袋'
        self.is_start_timing = False
        self.is_end_play = False

    def set_surface_location(self, coord, align=1):
        """从死亡的僵尸哪里获取坐标"""
        # 将这个矩形的坐下角对准僵尸矩形的底部中央位置
        if align == 0:
            self.rect.midbottom = coord
        elif align == 1:
            self.rect.bottomleft = coord
        elif align == 2:
            self.rect.midbottom = coord

    def show_head(self, pause, interval_time=0.1):
        """"在屏幕上绘制普通僵尸飞翔的脑袋"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        image = handle_index_error(self.image_list, self.index)
        plot_image(self.surface, image, -10, self.height - 5)
        self.screen.blit(self.surface, self.rect)

        if not pause:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.index < len(self.image_list) - 1:
                    self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                elif float(current_time - self.dead_time) >= self.die_after_stay_time and self.is_start_timing:
                    self.is_end_play = True
                elif self.index == len(self.image_list) - 1 and not self.is_start_timing:
                    self.dead_time = current_time
                    self.is_start_timing = True
                self.last_plot_time = current_time


class IceRoad(Sprite):
    """创建冰道"""
    def __init__(self, ai_game, *label):
        """冰道基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = (30, 70)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (label[0], label[1])
        self.ice_road = self.setting.ice_road_image

    def show_ice_road(self):
        """在屏幕上绘制冰道"""
        self.surface.fill((255, 255, 255))
        self.surface.set_colorkey((255, 255, 255))
        self.surface.blit(self.ice_road, (0, 0))
        self.screen.blit(self.surface, self.rect)


class IceRoadHead(Sprite):
    """创建冰道头"""
    def __init__(self, ai_game, *label):
        """冰道头基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = (20, 70)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (label[0], label[1])
        self.ice_road_head = self.setting.ice_road_head_image
        self.last_plot_time = 0

    def show_ice_road(self):
        """在屏幕上绘制冰道"""
        self.surface.fill((255, 255, 255))
        self.surface.set_colorkey((255, 255, 255))
        self.surface.blit(self.ice_road_head, (0, 0))
        self.screen.blit(self.surface, self.rect)
# ************************************************ 僵尸类 **********************************************#


class GeneralZombie(Sprite):
    """"创建普通僵尸"""
    def __init__(self, ai_game):
        """"普通僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.speed = 0.3
        self.original_speed = 0.3
        self.health = 270
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.zombie_index = 0  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.general_zombie_walk_image_list[randint(0, 2)]  # 行走状态下的僵尸
        self.walk_image_list_without_head = self.setting.general_zombie_walk_without_head  # 没有头行走
        self.attack_image_list = self.setting.general_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_head = self.setting.general_zombie_attack_without_head  # 没有头攻击
        self.boom_image_list = self.setting.general_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.general_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.general_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 普通僵尸正常状态
        self.is_alive = True
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '普通'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 67, top + 60)
        self.attack_coord = (left + 47, top + 60)
        self.was_frozen_coord = (left + 82, top + 115)

    def is_dead(self):
        """根据僵尸血量确认是否移除僵尸"""
        if self.health <= 0:
            self.is_alive = False
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 82
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制普通僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
                if not pause:
                    self._update_zombie_location()
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 3, self.height - 5)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_alive and not self.was_called:  # 正常行走状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
            else:
                image = handle_index_error(self.image_list, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
                if not pause:
                    self._update_zombie_location()
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -10, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                        self._update_zombie_location()
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_alive and not self.was_called:  # 正常行走状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class FlagZombie(Sprite):
    """"创建旗子僵尸"""
    def __init__(self, ai_game):
        """"旗子僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.speed = 0.4
        self.original_speed = 0.4
        self.health = 270
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.zombie_index = 0  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = self.height * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.flag_zombie_walk  # 行走状态下的僵尸
        self.walk_image_list_without_head = self.setting.flag_zombie_walk_without_head  # 没有头行走
        self.attack_image_list = self.setting.flag_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_head = self.setting.flag_zombie_attack_without_head  # 没有头攻击
        self.boom_image_list = self.setting.general_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.general_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.flag_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 普通僵尸正常状态
        self.is_alive = True
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '普通'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 74, top + 64)
        self.attack_coord = (left + 55, top + 64)
        self.was_frozen_coord = (left + 93, top + 112)

    def is_dead(self):
        """根据僵尸血量确认是否移除僵尸"""
        if self.health <= 0:
            self.is_alive = False
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 93
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制旗子僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 7, self.height + 2)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -10, self.height - 5)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 3, self.height - 5)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_alive and not self.was_called:  # 正常行走状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -10, self.height)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -10, self.height)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -10, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height:
                    self.image_move_height -= 5.91
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_alive and not self.was_called:  # 正常行走状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class RoadBlockZombie(Sprite):
    """"创建路障僵尸"""
    def __init__(self, ai_game):
        """"路障基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.health = 640
        self.index = 0
        self.zombie_index = 1  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.roadblock_zombie_walk_with_armor  # 行走状态下的僵尸
        self.attack_image_list = self.setting.roadblock_zombie_attack_with_armor  # 发起攻击动作的僵尸
        self.attack_image_without_armor_list = self.setting.roadblock_zombie_attack_without_armor  # 没有防具发起攻击的僵尸
        self.attack_image_list_without_head = self.setting.roadblock_zombie_attack_without_head
        self.walk_image_list_without_head = self.setting.roadblock_zombie_walk_without_head
        self.lost_armor_image_list = self.setting.roadblock_zombie_walk_image_list[randint(0, 2)]  # 防具掉落之后的僵尸
        self.boom_image_list = self.setting.roadblock_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.roadblock_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.roadblock_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸是否有防具
        self.is_wear_armor = True
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '路障'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 65, top + 65)
        self.attack_coord = (left + 50, top + 65)
        self.was_frozen_coord = (left + 82, top + 115)

    def is_dead(self):
        """根据僵尸血量确认是否移除僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 82
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制路障僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -10, self.height - 5)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 3, self.height - 5)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_armor:
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_without_armor_list, self.index)
                plot_image(self.surface, image, -10, self.height - 5)
            else:
                image = handle_index_error(self.lost_armor_image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -10, self.height - 5)
        elif self.is_wear_armor and not self.was_called:  # 正常行走状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -20, self.height - 5)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -20, self.height - 5)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -20, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_lost_armor:  # 丢掉防具的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_without_armor_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.lost_armor_image_list)
                elif self.is_wear_armor and not self.was_called:  # 普通奔跑状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if self.is_wear_armor and was_shoot:
            self.music.play_short_time_sound(self.setting.roadblock_zombie_was_hit)
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self.is_lost_armor = True
            self.is_wear_armor = False
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class DrumZombie(Sprite):
    """"创建铁桶僵尸"""
    def __init__(self, ai_game):
        """铁桶僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1370
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.index = 0
        self.zombie_index = 2  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.drum_zombie_walk_with_armor  # 行走状态下的僵尸
        self.attack_image_list = self.setting.drum_zombie_attack_with_armor  # 发起攻击动作的僵尸
        self.attack_image_without_armor_list = self.setting.drum_zombie_attack_without_armor  # 没有防具发起攻击的僵尸
        self.attack_image_list_without_head = self.setting.drum_zombie_attack_without_head
        self.walk_image_list_without_head = self.setting.drum_zombie_walk_without_head
        self.lost_armor_image_list = self.setting.drum_zombie_walk_image_list[randint(0, 2)]  # 防具掉落之后的僵尸
        self.boom_image_list = self.setting.drum_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.drum_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.drum_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸是否有防具
        self.is_wear_armor = True
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '铁桶'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 65, top + 60)
        self.attack_coord = (left + 45, top + 60)
        self.was_frozen_coord = (left + 77, top + 110)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 77
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制铁桶僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, -12, self.height - 5)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 3, self.height - 5)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_armor:
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_without_armor_list, self.index)
                plot_image(self.surface, image, -12, self.height - 5)
            else:
                image = handle_index_error(self.lost_armor_image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
        elif self.is_wear_armor and not self.was_called:  # 正常奔跑状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_lost_armor:  # 丢掉防具的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_without_armor_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.lost_armor_image_list)
                elif self.is_wear_armor and not self.was_called:  # 普通奔跑状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if self.is_wear_armor and was_shoot:
            self.music.play_short_time_sound(self.setting.drum_zombie_was_hit)
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self.is_lost_armor = True
            self.is_wear_armor = False
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class FootballZombie(Sprite):
    """"创建橄榄球僵尸"""
    def __init__(self, ai_game):
        """"橄榄僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (160, 145)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1670
        self.health_limit = 1000  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.zombie_index = 3  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 0.6
        self.original_speed = 0.6
        self.image_move_height = (self.height - 2) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.football_zombie_walk_with_armor  # 奔跑状态下的僵尸
        self.attack_image_list = self.setting.football_zombie_attack_with_armor  # 发起攻击动作的僵尸
        self.attack_image_without_armor_list = self.setting.football_zombie_attack_without_armor  # 没有防具发起攻击的僵尸
        self.walk_image_list_without_head = self.setting.football_zombie_run_without_head
        self.attack_image_list_without_head = self.setting.football_zombie_attack_without_head
        self.lost_armor_image_list = self.setting.football_zombie_walk_without_armor  # 防具掉落之后的僵尸
        self.boom_image_list = self.setting.football_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.football_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.football_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸是否有防具
        self.is_wear_armor = True
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '橄榄'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 100, top + 50)
        self.attack_coord = (left + 55, top + 55)
        self.was_frozen_coord = (left + 110, top + 125)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 110
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制橄榄球僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 25, self.height + 10)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 40, self.height - 2)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, 40, self.height - 2)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, -20, self.height)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_armor:  # 防具掉落
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_without_armor_list, self.index)
                plot_image(self.surface, image, 40, self.height - 2)
            else:
                image = handle_index_error(self.lost_armor_image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 40, self.height - 2)
        elif self.is_wear_armor and not self.was_called:  # 正常奔跑状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 40, self.height - 2)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 40, self.height - 2)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)

            plot_image(self.surface, image, 40, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 2:
                    self.image_move_height -= 6.5
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_lost_armor:  # 丢掉防具的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_without_armor_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.lost_armor_image_list)
                elif self.is_wear_armor and not self.was_called:  # 普通奔跑状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 2 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self.is_lost_armor = True
            self.is_wear_armor = False
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class PoleVaultZombie(Sprite):
    """"创建撑杆跳僵尸"""
    def __init__(self, ai_game):
        """"撑杆跳僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (290, 200)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 500
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 1
        self.original_speed = 1
        self.current_speed = 0.4
        self.image_move_height = (self.height + 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.pole_vault_zombie_run  # 奔跑状态下的僵尸
        self.run_image_list_without_head = self.setting.pole_vault_zombie_run_without_head
        self.attack_image_list = self.setting.pole_vault_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_head = self.setting.pole_vault_zombie_attack_without_head
        self.jump_image_list = self.setting.pole_vault_zombie_jump  # 跳跃动作
        self.stand_on_group_image_list = self.setting.pole_vault_zombie_fall  # 落地动作
        self.walk_image_list = self.setting.pole_vault_zombie_walk  # 正常行走
        self.walk_image_list_without_head = self.setting.pole_vault_zombie_walk_without_head
        self.boom_image_list = self.setting.pole_vault_zombie_boom  # 被炸成灰烬的僵尸
        self.body_fall_image_list = self.setting.pole_vault_zombie_body_fall  # 身体落下
        self.head_fall_image_list = self.setting.pole_vault_zombie_head_fall  # 头落下
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_exist_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.pole_vault_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        self.is_play_jump_music = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否奔跑而死
        self.is_run = False
        # 奔跑而死的动画播放完毕
        self.run_is_end_play = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸防具已经掉落
        self.is_lost_pole = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_jump = False
        self.is_fall = False
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '撑杆'
        self._update_zombie_center_location()

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 173, top + 115)
        self.attack_coord = (left + 160, top + 115)
        self.was_frozen_coord = (left + 188, top + 182)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 188
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制撑杆跳僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 0, self.height + 10)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            if self.is_get_dead_location and time() - self.last_exist_time <= 2.5:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image, 0, self.height + 5)
                self.screen.blit(self.surface1, self.rect1)
            if self.is_run and not self.run_is_end_play:
                image = handle_index_error(self.run_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height + 5)
                if self.index == len(self.run_image_list_without_head) - 1:
                    self.run_is_end_play = True
                    self.is_run = False
                    self.index = 0
            elif self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height + 15)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, 0, self.height + 15)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif not self.is_walk and not self.is_attack and not self.is_run:
                image = handle_index_error(self.body_fall_image_list, self.index)
                plot_image(self.surface, image, 0, self.height + 5)
                if self.index == len(self.body_fall_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_pole:  # 撑杆掉落
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 0, self.height + 15)
            else:
                image = handle_index_error(self.walk_image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height + 15)
        elif not self.is_lost_pole and not self.was_called:  # 没有丢失撑杆
            if self.is_touch_plant:
                if self.is_jump and not self.is_fall:  # 跳了起来
                    image = handle_index_error(self.jump_image_list, self.index)
                    plot_image(self.surface, image, 0, self.height)
                    if self.index == len(self.jump_image_list) - 1:
                        self.is_fall = True
                        self.index = 0
                        self.x -= 90
                        self.rect.x = self.x
                        self._update_zombie_center_location()
                    if not self.is_play_jump_music and self.index == 3:
                        self.music.play_short_time_sound(self.setting.pole_vault_jump)
                        self.is_play_jump_music = True
                elif self.is_jump and self.is_fall:  # 落了下来
                    image = handle_index_error(self.stand_on_group_image_list, self.index)
                    plot_image(self.surface, image, 0, self.height + 15)
                    if self.index == len(self.stand_on_group_image_list) - 1:
                        self.is_fall = False
                        self.is_lost_pole = True
                        self.is_touch_plant = False
                        self.index = 0
                        self.speed = self.current_speed
            else:  # 正常奔跑状态
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height + 5)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, 0, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height + 5:
                    self.image_move_height -= 9.32
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.head_fall_image_list)
                    if self.is_run and not self.run_is_end_play:
                        self.index = (self.index + 1) % len(self.run_image_list_without_head)
                    elif self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and not self.is_run:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif self.is_lost_pole:  # 丢掉撑杆的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list)
                elif not self.is_lost_pole and not self.was_called:  # 普通奔跑状态
                    if self.is_touch_plant:
                        if self.is_jump and not self.is_fall:
                            self.index = (self.index + 1) % len(self.jump_image_list)
                        elif self.is_fall and self.is_fall:
                            self.index = (self.index + 1) % len(self.stand_on_group_image_list)
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height + 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_run and self.was_shot_to_die and not self.is_touch_plant and not self.is_lost_pole:
            # 僵尸是因为在奔跑过程中打死,这个时候没有丢失撑杆
            self.is_run = True
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant and self.is_lost_pole:
            # 僵尸是因为在行走过程中打死， 这个时候丢失了撑杆
            self.is_walk = True
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant and self.is_lost_pole:
            # 僵尸是因为在攻击途中被打死， 这个时候丢失了撑杆
            self.is_attack = True


class IceCarZombie(Sprite):
    """"创建冰车僵尸"""
    def __init__(self, ai_game):
        """"冰车僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.ai_game = ai_game
        self.width, self. height = (420, 400)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1350
        self.hurt = 70
        self.index = 0
        self.zombie_index = 5  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 0.6
        self.original_speed = 0.6
        self.image_move_height = 510
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((170, 170))
        self.rect = self.surface.get_rect()
        self.rect1 = self.surface1.get_rect()
        self.lattice_index = randint(0, 4)
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.x = self.setting.appear_locations[self.lattice_index][0]
        self.y = self.setting.appear_locations[self.lattice_index][1] + 100
        self.rect.bottomleft = (self.x, self.y)
        self.rect1.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.ice_car_zombie_drive_full_health
        self.health_about_half_image_list = self.setting.ice_car_zombie_drive_half_health  # 半血状态下的冰车
        self.health_about_zero_image_list = self.setting.ice_car_zombie_drive_zero_health  # 残血状态下的冰车
        self.shot_image_list = self.setting.ice_car_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.boom_image_list = self.setting.ice_car_zombie_boom  # 被炸成灰烬的僵尸
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_plot_location_x = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.ice_car_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 僵尸半血
        self.health_about_half = False
        # 僵尸残血
        self.health_about_zero = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.is_plot_ice_road_head = False
        self.can_be_controlled = False
        self.is_play_enter_sound = False
        self.is_play_explosion_sound = False
        self.is_reset_index = False
        self.is_frozen_time = 0
        self.name = '冰车'
        self._update_zombie_center_location()

    def _update_zombie_location(self, ice_road_list):
        """更新僵尸的位置"""
        if not self.is_dead():
            if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
                if not self.is_play_enter_sound and self.rect.center[0] - 150 <= self.setting.pea_max_distance:
                    self.music.play_short_time_sound(self.setting.ice_car_enter)
                    self.is_play_enter_sound = True
                self.x -= self.speed
                self.rect.x = self.x
                self._update_zombie_center_location()
            if self.rect.center[0] <= self.setting.pea_max_distance + 100:
                if abs(self.rect.center[0] - self.last_plot_location_x) >= 30:
                    self.last_plot_location_x = self.rect.center[0]
                    x = self.last_plot_location_x - 30
                    y = self.setting.appear_locations[self.lattice_index][1]
                    new_ice_road = IceRoad(self.ai_game, x, y)
                    ice_road_list.add(new_ice_road)
        else:
            if not self.was_boom_to_die:
                self.last_plot_location_x = self.rect.center[0]
                x = self.last_plot_location_x - 15
                y = self.setting.appear_locations[self.lattice_index][1]
                new_ice_road_head = IceRoadHead(self.ai_game, x, y)
                new_ice_road_head.last_plot_time = time()
                ice_road_list.add(new_ice_road_head)

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        if self.was_called:
            left, top = self.rect1.left, self.rect1.top
            self.was_attacked_coord = (left + 238, top + 189)
            self.attack_coord = (left + 170, top + 220)
            self.was_frozen_coord = (left + 90, top + 160)
        else:
            left, top = self.rect.left, self.rect.top
            self.was_attacked_coord = (left + 238, top + 189)
            self.attack_coord = (left + 170, top + 220)
            self.was_frozen_coord = (left + 204, top + 285)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 204
        self.y = self.setting.appear_locations[self.lattice_index][1] + 100
        self.rect.bottomleft = (self.x, self.y)
        self.rect1.bottomleft = (x - 90, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, ice_road_list, interval_time=0.1):
        """"在屏幕上绘制冰车僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.is_dead():  # 这个时候僵尸已经死掉了
            if self.was_boom_to_die:  # 被炸死的状态
                image = handle_index_error(self.boom_image_list, self.index)
                plot_image(self.surface, image, 15, 390)
                if len(self.boom_image_list) - 1 == self.index:
                    self.is_end_play = True
            elif self.was_shot_to_die:  # 如果被射死
                if not self.is_reset_index:
                    self.index = 2
                    self.is_reset_index = True
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 15, 390)
                if len(self.shot_image_list) - 1 == self.index:
                    self.is_end_play = True
            if not self.is_plot_ice_road_head:
                self._update_zombie_location(ice_road_list)
                self.is_plot_ice_road_head = True  # 保证只绘制一张
            self.screen.blit(self.surface, self.rect)
        elif not self.is_dead() and not self.was_called:
            if self.health_about_half and not self.health_about_zero:  # 生命过半但并没有残血
                image = handle_index_error(self.health_about_half_image_list, self.index)
                if not pause:
                    self._update_zombie_location(ice_road_list)
                plot_image(self.surface, image, 15, 390)
            elif self.health_about_half and self.health_about_zero:  # 已经残血但没有死亡
                image = handle_index_error(self.health_about_zero_image_list, self.index)
                if not pause:
                    self._update_zombie_location(ice_road_list)
                plot_image(self.surface, image, 15, 390)
            elif not self.health_about_half and not self.health_about_zero:  # 健康状态
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location(ice_road_list)
                plot_image(self.surface, image, 15, 390)
            self.screen.blit(self.surface, self.rect)
        elif self.was_called:
            self.surface1.fill((0, 255, 0))
            self.surface1.set_colorkey((0, 255, 0))
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface1, image, -100, self.image_move_height)
            self.screen.blit(self.surface1, self.rect1)
            self.soil.show_soil(pause)
            if self.soil.is_play_one_frame:
                if self.image_move_height > 255:
                    self.image_move_height -= 12.2

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.is_dead():
                    if self.was_boom_to_die:  # 被炸成灰的图片
                        self.index = (self.index + 1) % len(self.boom_image_list)
                    elif self.was_shot_to_die:  # 被射死的图片
                        self.index = (self.index + 1) % len(self.shot_image_list)
                        if not self.is_play_explosion_sound and self.index == 29:
                            self.music.play_short_time_sound(self.setting.ice_car_explosion)
                            self.is_play_explosion_sound = True
                elif not self.is_dead() and not self.was_called:
                    if self.health_about_half and not self.health_about_zero:  # 生命不足一半
                        self.index = (self.index + 1) % len(self.health_about_half_image_list)
                    elif self.health_about_half and self.health_about_zero:  # 生命几乎为零
                        self.index = (self.index + 1) % len(self.health_about_zero_image_list)
                    elif not self.health_about_half and not self.health_about_zero:  # 生命很健康
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= 255 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if self.health <= 700 and not self.health_about_half:
            self.health_about_half = True
            self.index = 0
        elif self.health <= 270 and not self.health_about_zero:
            self.health_about_zero = True
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class ImpZombie(Sprite):
    """"创建小鬼僵尸"""
    def __init__(self, ai_game):
        """小鬼僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (80, 120)
        self.soil = ZombieAppearSoil(ai_game)
        self.speed = 0.3
        self.original_speed = 0.3
        self.health = 270
        self.hurt = 70
        self.hurt_interval = 0.1  # 伤害间隔时间
        self.index = 0
        self.zombie_index = 6  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height + 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.imp_zombie_walk  # 奔跑状态下的僵尸
        self.attack_image_list = self.setting.imp_zombie_attack
        self.boom_image_list = self.setting.imp_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.imp_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = time()
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.imp_zombie_static
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 是否攻击植物
        self.is_attack_plant = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.is_play_head_to_fly_sound = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.name = '大鬼'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 42, top + 77)
        self.attack_coord = (left + 25, top + 77)
        self.was_frozen_coord = (left + 42, top + 100)

    def is_dead(self):
        """根据僵尸血量确认是否移除僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 42
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.15):
        """"在屏幕上绘制小鬼僵尸"""
        self.surface.fill((0, 255, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 255, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 如果被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 5, self.height + 5)
        elif self.was_shot_to_die:  # 如果被射死
            image = handle_index_error(self.shot_image_list, self.index)
            plot_image(self.surface, image, 5, self.height + 5)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
        elif not self.was_called:  # 正常奔跑状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 5, self.height + 5)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 5, self.height + 5)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, 5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height + 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    self.index = (self.index + 1) % len(self.shot_image_list)
                    if len(self.shot_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif not self.was_called:
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height + 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class ClownZombie(Sprite):
    """"创建小丑僵尸"""
    def __init__(self, ai_game):
        """"小丑僵尸基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (270, 270)
        self.flying_head = FlyingZombieHead(ai_game, 150, 150)
        self.soil = ZombieAppearSoil(ai_game)
        self.speed = 0.4
        self.original_speed = 0.4
        self.health = 500
        self.hurt = 70
        self.hurt_interval = 0.2  # 伤害间隔时间
        self.index = 0
        self.zombie_index = 0  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = 250
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((100, 120))
        self.rect = self.surface.get_rect()
        self.rect1 = self.surface1.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.explode_distance = randint(400, 900)  # 设置爆炸触发距离范围
        self.x = self.setting.appear_locations[self.lattice_index][0]
        self.y = self.setting.appear_locations[self.lattice_index][1] + 95
        self.rect.bottomleft = (self.x, self.y)
        self.rect1.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.image_list = self.setting.clown_zombie_walk  # 行走状态下的僵尸
        self.walk_image_list_without_head = self.setting.clown_zombie_walk_without_head  # 没有头行走
        self.attack_image_list = self.setting.clown_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_head = self.setting.clown_zombie_attack_without_head  # 没有头攻击

        self.was_scared_image_list = self.setting.clown_was_scared
        self.boom_image_list = self.setting.clown_zombie_boom  # 被炸成灰烬的僵尸

        self.explode_image_list = self.setting.clown_zombie_explode  # 爆炸动画
        self.shot_image_list = self.setting.clown_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.is_frozen_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.clown_zombie_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        self.is_play_enter_music = False
        self.is_play_explode_sound = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否被吓住
        self.is_scare = False
        # 被吓住的动画播放完毕
        self.scare_is_end_play = False
        # 是否爆炸
        self.is_explode = False
        # 爆炸的动画播放完毕
        self.explode_is_end_play = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 普通僵尸正常状态
        self.is_alive = True
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_play_head_to_fly_sound = False
        self.name = '小丑'
        self._update_zombie_center_location()

    def _check_is_collide_plants(self):
        """检测爆炸范围是否存在植物"""
        plants_lists = self.ai_game.plants_lists
        if self.lattice_index == 0:
            self._remove_relative_line_plants(0, 2, plants_lists)
        elif self.lattice_index == 1:
            self._remove_relative_line_plants(0, 3, plants_lists)
        elif self.lattice_index == 2:
            self._remove_relative_line_plants(1, 4, plants_lists)
        elif self.lattice_index == 3:
            self._remove_relative_line_plants(2, 5, plants_lists)
        elif self.lattice_index == 4:
            self._remove_relative_line_plants(3, 5, plants_lists)

    def _remove_relative_line_plants(self, start, end, plants_lists):
        """根据僵尸所在的行移除相邻行的植物"""
        left, right = self.rect.left, self.rect.right
        for index in range(start, end):
            for plant in plants_lists[index]:
                if plant.can_be_destroy:
                    plant_x_left, plant_x_right = plant.was_attacked_coord
                    if plant_x_left >= left and plant_x_right <= right:
                        plant.health = 0
                    elif plant_x_left <= left <= plant_x_right:
                        plant.health = 0
                    elif plant_x_left <= right <= plant_x_right:
                        plant.health = 0

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            if self.attack_coord[0] <= self.setting.pea_max_distance and not self.is_play_enter_music:
                self.music.play_short_time_sound(self.setting.clown_zombie_enter)
                self.is_play_enter_music = True
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()
        if self.is_alive and self.attack_coord[0] <= self.explode_distance:
            self.music.play_short_time_sound(self.setting.clown_zombie_shout)
            self.is_scare = True
            self.is_alive = False
            self.is_touch_plant = False
            self.index = 0

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        if self.was_called:
            left, top = self.rect1.left, self.rect1.top
            self.was_frozen_coord = (left + 65, top + 110)
        else:
            left, top = self.rect.left, self.rect.top
            self.was_attacked_coord = (left + 215, top + 92)
            self.attack_coord = (left + 202, top + 92)
            self.was_frozen_coord = (left + 232, top + 160)
            # rect = pygame.Rect(42,  83, 20, 20)
            # pygame.draw.rect(self.surface, (255, 0, 0), rect)

    def is_dead(self):
        """根据僵尸血量确认是否移除僵尸"""
        if self.health <= 0:
            self.is_alive = False
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 232
        self.y = self.setting.appear_locations[self.lattice_index][1] + 95
        self.rect.bottomleft = (self.x, self.y)
        self.rect1.bottomleft = (x - 65, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制小丑僵尸"""
        self.surface.fill((0, 255, 255))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 255, 255))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 110, 180)
            self.screen.blit(self.surface, self.rect)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 110, 180)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, 110, 180)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif not self.is_walk and not self.is_attack:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 110, 180)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
            self.screen.blit(self.surface, self.rect)
        elif self.is_scare and not self.scare_is_end_play:
            image = handle_index_error(self.was_scared_image_list, self.index)
            plot_image(self.surface, image, 110, 180)
            if self.index == len(self.was_scared_image_list) - 1:
                self.scare_is_end_play = True
                self.is_explode = True
                self.is_scare = False
            self.screen.blit(self.surface, self.rect)
        elif self.is_explode and not self.explode_is_end_play:
            image = handle_index_error(self.explode_image_list, self.index)
            plot_image(self.surface, image, 12, self.height - 7)
            if self.index == len(self.explode_image_list) - 1:
                self.explode_is_end_play = True
                self.is_end_play = True
            if not self.is_play_explode_sound and self.index == 3:
                self.music.play_short_time_sound(self.setting.clown_zombie_explode_sound)
                self.is_play_explode_sound = True
            self.screen.blit(self.surface, self.rect)
        elif self.is_alive and not self.was_called:  # 正常行走状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 110, 180)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 110, 180)
            self.screen.blit(self.surface, self.rect)
        elif self.was_called:
            self.surface1.fill((0, 255, 0))
            self.surface1.set_colorkey((0, 255, 0))
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface1, image, -55, self.image_move_height)
            self.screen.blit(self.surface1, self.rect1)
            if self.soil.is_play_one_frame:
                if self.image_move_height > 125:
                    self.image_move_height -= 7
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif not self.is_walk and not self.is_attack and self.index < len(self.shot_image_list) - 1:
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_scare:
                    self.index = (self.index + 1) % len(self.was_scared_image_list)
                elif self.is_explode:
                    self.index = (self.index + 1) % len(self.explode_image_list)
                    if self.index == 2:
                        self._check_is_collide_plants()
                elif self.is_alive and not self.was_called:  # 正常行走状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= 125 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if not self.is_walk and self.was_shot_to_die and not self.is_touch_plant:  # 僵尸是因为在行走过程中打死
            self.is_walk = True
            self.flying_head.set_surface_location(
                (self.was_attacked_coord[0], self.setting.appear_locations[self.lattice_index][1]), 1)
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant:  # 僵尸是因为在攻击途中被打死
            self.is_attack = True
            self.flying_head.set_surface_location(
                (self.was_attacked_coord[0], self.setting.appear_locations[self.lattice_index][1]), 1)


class ScreenDoorZombie(Sprite):
    """"创建铁栅门僵尸"""
    def __init__(self, ai_game):
        """铁栅门僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1370
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.index = 0
        self.zombie_index = 2  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]

        self.image_list = self.setting.screen_door_zombie_walk  # 行走状态下的僵尸
        # 防具掉落之后的僵尸
        self.lost_armor_image_list = self.setting.screen_door_zombie_walk_without_armor_image_list[randint(0, 2)]
        self.walk_image_list_in_armor_without_head = self.setting.screen_door_zombie_walk_without_head
        self.walk_image_list_without_armor_and_head = self.setting.screen_door_zombie_walk_without_armor_and_head

        self.attack_image_list = self.setting.screen_door_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_armor = self.setting.screen_door_attack_without_armor
        self.attack_image_list_in_armor_without_head = self.setting.screen_door_zombie_attack_without_head
        self.attack_image_list_without_armor_and_head = self.setting.screen_door_zombie_attack_without_armor_and_head

        self.boom_image_list = self.setting.screen_door_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.screen_door_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.is_frozen_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.screen_door_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在行走过程中被穿透而死
        self.is_walk_in_armor = False
        # 行走过程中穿透而死的动画播放完毕
        self.walk_in_armor_is_end_play = False
        # 是否在攻击过程中被穿透而死
        self.is_attack_in_armor = False
        # 行走过程中穿透而死的动画播放完毕
        self.attack_in_armor_is_end_play = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸是否有防具
        self.is_wear_armor = True
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_play_head_to_fly_sound = False
        self.name = '铁栅门'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_wear_armor:
            self.was_attacked_coord = (left + 52, top + 77)
            self.was_frozen_coord = (left + 78, top + 115)
        elif self.is_lost_armor:
            self.was_attacked_coord = (left + 70, top + 57)
            self.was_frozen_coord = (left + 83, top + 115)
        self.attack_coord = (left + 48, top + 77)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 78
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制铁栅门僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True

            if self.is_walk_in_armor and not self.walk_in_armor_is_end_play:
                image = handle_index_error(self.walk_image_list_in_armor_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height - 5)
                if self.index == len(self.walk_image_list_in_armor_without_head) - 1:
                    self.walk_in_armor_is_end_play = True
                    self.is_walk_in_armor = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack_in_armor and not self.attack_in_armor_is_end_play:
                image = handle_index_error(self.attack_image_list_in_armor_without_head, self.index)
                plot_image(self.surface, image, 0, self.height - 5)
                if self.index == len(self.attack_image_list_in_armor_without_head) - 1:
                    self.attack_in_armor_is_end_play = True
                    self.is_attack_in_armor = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_armor_and_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.walk_image_list_without_armor_and_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
                    self.x -= 20
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_armor_and_head, self.index)
                plot_image(self.surface, image, -12, self.height - 5)
                if self.index == len(self.attack_image_list_without_armor_and_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
                    self.x += 10
                    self.rect.x = self.x
                    self._update_zombie_center_location()
            elif not self.is_walk and not self.is_attack and not self.is_walk_in_armor and not self.is_attack_in_armor:
                image = handle_index_error(self.shot_image_list, self.index)
                plot_image(self.surface, image, 3, self.height - 5)
                if self.flying_head.is_end_play and self.index == len(self.shot_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_armor:
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list_without_armor, self.index)
                plot_image(self.surface, image, -12, self.height - 5)
            else:
                image = handle_index_error(self.lost_armor_image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
        elif self.is_wear_armor and not self.was_called:  # 带着防具
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 0, self.height - 5)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 0, self.height - 5)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, 0, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.is_walk_in_armor and not self.walk_in_armor_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_in_armor_without_head)
                    elif self.is_attack_in_armor and not self.attack_in_armor_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_in_armor_without_head)
                    elif self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_armor_and_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_armor_and_head)
                    elif (not self.is_walk and not self.is_attack and not self.is_walk_in_armor and
                          not self.is_attack_in_armor and self.index < len(self.shot_image_list) - 1):
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_lost_armor:  # 丢掉防具的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_armor)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.lost_armor_image_list)
                elif self.is_wear_armor and not self.was_called:  # 普通奔跑状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if self.is_wear_armor and was_shoot:
            self.music.play_short_time_sound(self.setting.drum_zombie_was_hit)
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self._update_zombie_center_location()
            self.is_lost_armor = True
            self.is_wear_armor = False
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        # 僵尸穿着防具被打死
        if not self.is_walk_in_armor and self.was_shot_to_die and not self.is_touch_plant and self.is_wear_armor:
            self.is_walk_in_armor = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        # 僵尸是因为在攻击途中被打死穿着防具
        elif not self.is_attack_in_armor and self.was_shot_to_die and self.is_touch_plant and self.is_wear_armor:
            self.is_attack_in_armor = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        # 僵尸是因为在行走过程中打死, 没有穿防具
        elif not self.is_walk and self.was_shot_to_die and not self.is_touch_plant and self.is_lost_armor:
            self.is_walk = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)
        # 僵尸是因为在攻击途中被打死， 没有穿防具
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant and self.is_lost_armor:
            self.is_attack = True
            self.flying_head.set_surface_location(self.rect.midbottom, 1)


class NewspaperZombie(Sprite):
    """"创建读报僵尸"""
    def __init__(self, ai_game):
        """"读报僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (160, 135)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 420
        self.health_limit = 270
        self.hurt = 70
        self.excite_hurt = 200
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.excite_hurt_interval = 0.05
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 0.3
        self.original_speed = 0.3
        self.excite_speed = 3
        self.image_move_height = self.height * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        # 行走状态
        self.image_list = self.setting.newspaper_zombie_walk  # 行走状态下的僵尸
        self.walk_image_list_without_head = self.setting.newspaper_zombie_walk_without_head
        self.walk_image_list_without_newspaper = self.setting.newspaper_zombie_walk_without_newspaper
        self.walk_image_list_without_newspaper_and_head = self.setting.newspaper_zombie_walk_without_newspaper_and_head
        # 攻击状态
        self.attack_image_list = self.setting.newspaper_zombie_attack  # 发起攻击动作的僵尸
        self.attack_image_list_without_head = self.setting.newspaper_zombie_attack_without_head
        self.attack_image_list_without_newspaper = self.setting.newspaper_zombie_attack_without_newspaper
        self.attack_image_list_without_newspaper_and_head = self.setting.newspaper_zombie_walk_without_newspaper_and_head
        self.doubt_image_list = self.setting.newspaper_zombie_doubt  # 疑惑状态
        self.boom_image_list = self.setting.newspaper_zombie_boom  # 被炸成灰烬的僵尸
        self.body_fall_image_list = self.setting.newspaper_zombie_body_fall  # 身体落下
        self.head_fall_image_list = self.setting.newspaper_zombie_head_fall  # 头落下
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_exist_time = 0
        self.x = float(self.rect.x)
        self.static_image_list = self.setting.newspaper_zombie_static
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        self.is_play_doubt_music = False
        # 是否怀疑
        self.is_doubt = False
        # 怀疑动画播放完毕
        self.doubt_is_end_play = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在行走过程中被穿透而死
        self.is_walk_in_armor = False
        # 行走过程中穿透而死的动画播放完毕
        self.walk_in_armor_is_end_play = False
        # 是否在攻击过程中被穿透而死
        self.is_attack_in_armor = False
        # 行走过程中穿透而死的动画播放完毕
        self.attack_in_armor_is_end_play = False
        # 是否奔跑而死
        self.is_run = False
        # 奔跑而死的动画播放完毕
        self.run_is_end_play = False
        # 是否行走而死
        self.is_walk = False
        # 行走而死的动画播放完毕
        self.walk_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 确定该僵尸报纸已经掉落
        self.is_lost_newspaper = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.is_play_excite_sound = False
        self.name = '读报'
        self._update_zombie_center_location()

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit and not self.is_touch_plant:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.attack_coord = (left + 90, top + 60)
        if not self.is_lost_newspaper:
            self.was_attacked_coord = (left + 98, top + 88)
        else:
            self.was_attacked_coord = (left + 110, top + 60)
        self.was_frozen_coord = (left + 128, top + 120)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 128
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制读报僵尸"""
        current_time = time()
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 35, self.height + 10)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            if self.is_get_dead_location and current_time - self.last_exist_time <= 2.5:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image, 10, self.height)
                self.screen.blit(self.surface1, self.rect1)
            if self.is_walk_in_armor and not self.walk_in_armor_is_end_play:
                image = handle_index_error(self.walk_image_list_without_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 35, self.height)
                if self.index == len(self.walk_image_list_without_head) - 1:
                    self.walk_in_armor_is_end_play = True
                    self.is_walk_in_armor = False
                    self.index = 0
            elif self.is_attack_in_armor and not self.attack_in_armor_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, 35, self.height)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_in_armor_is_end_play = True
                    self.is_attack_in_armor = False
                    self.index = 0
            elif self.is_walk and not self.walk_is_end_play:
                image = handle_index_error(self.walk_image_list_without_newspaper_and_head, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 35, self.height)
                if self.index == len(self.walk_image_list_without_newspaper_and_head) - 1:
                    self.walk_is_end_play = True
                    self.is_walk = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_newspaper_and_head, self.index)
                plot_image(self.surface, image, 35, self.height)
                if self.index == len(self.attack_image_list_without_newspaper_and_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif not self.is_walk and not self.is_attack and not self.is_walk_in_armor and not self.is_attack_in_armor:
                image = handle_index_error(self.body_fall_image_list, self.index)
                plot_image(self.surface, image, 35, self.height)
                if self.index == len(self.body_fall_image_list) - 1 and current_time - self.last_exist_time >= 2.5:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif self.is_lost_newspaper and self.doubt_is_end_play:  # 报纸被打掉并且已经进入狂怒状态
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list_without_newspaper, self.index)
                plot_image(self.surface, image, 35, self.height)
            else:
                image = handle_index_error(self.walk_image_list_without_newspaper, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 35, self.height)
        elif self.is_doubt and self.is_lost_newspaper:
            if not self.is_play_excite_sound and self.index == 5:
                self.music.play_short_time_sound(self.setting.newspaper_zombie_excite)
                self.is_play_excite_sound = True
            image = handle_index_error(self.doubt_image_list, self.index)
            plot_image(self.surface, image, 35, self.height)
            if self.index == len(self.doubt_image_list) - 1:
                self.is_doubt = False
                self.doubt_is_end_play = True
        elif not self.is_lost_newspaper and not self.was_called:  # 带着报纸
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 35, self.height)
            else:
                image = handle_index_error(self.image_list, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, 40, self.height)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, 40, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height:
                    self.image_move_height -= 6.25
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.head_fall_image_list)
                    if self.is_walk_in_armor and not self.walk_in_armor_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_head)
                    elif self.is_attack_in_armor and not self.attack_in_armor_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif self.is_walk and not self.walk_is_end_play:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_newspaper_and_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_newspaper_and_head)
                    elif (not self.is_walk and not self.is_attack and not self.is_walk_in_armor and
                          not self.is_attack_in_armor and self.index < len(self.body_fall_image_list) - 1):
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif self.is_lost_newspaper and self.doubt_is_end_play:  # 丢掉防具的图片
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_newspaper)
                        if current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list_without_newspaper)
                elif self.is_doubt and self.is_lost_newspaper:
                    self.index = (self.index + 1) % len(self.doubt_image_list)
                elif not self.is_lost_newspaper and not self.was_called:  # 普通行走状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if self.health <= self.health_limit and not self.is_doubt:
            self.is_doubt = True
            self.is_lost_newspaper = True
            self.hurt = self.excite_hurt
            self.hurt_interval = self.excite_hurt_interval
            self.speed = self.excite_speed
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        if (not self.is_walk_in_armor and self.was_shot_to_die and not self.is_touch_plant and
                not self.is_lost_newspaper):  # 拿着报纸走路被打死
            self.is_walk_in_armor = True
        elif (not self.is_attack_in_armor and self.was_shot_to_die and self.is_touch_plant and
                not self.is_lost_newspaper):  # 拿着报纸吃被打死
            self.is_walk = True
        elif not self.is_walk and self.was_shot_to_die and not self.is_touch_plant and self.is_lost_newspaper:
            self.is_walk = True  # 报纸丢掉走路被打死
        elif not self.is_attack and self.was_shot_to_die and self.is_touch_plant and self.is_lost_newspaper:
            self.is_attack = True  # 报纸丢掉吃被打死


class SnorkelZombie(Sprite):
    """"创建潜水僵尸"""
    def __init__(self, ai_game):
        """"潜水僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (110, 170)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 270
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 0.5
        self.original_speed = 0.5
        self.current_speed = 0.3
        self.image_move_height = (self.height + 15) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.snorkel_zombie_static
        self.walk_image_list1 = self.setting.snorkel_zombie_walk_in_land
        self.walk_image_list2 = self.setting.snorkel_zombie_walk_in_river
        self.jump_image_list = self.setting.snorkel_zombie_jump
        self.attack_image_list = self.setting.snorkel_zombie_attack_in_river
        self.sink_image_list = self.setting.snorkel_zombie_sink
        self.risk_image_list = self.setting.snorkel_zombie_risk
        self.body_fall_image_list = self.setting.snorkel_zombie_body_fall
        self.head_fall_image_list = self.setting.snorkel_zombie_head_fall
        self.boom_image_list = self.setting.snorkel_zombie_boom
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_exist_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        self.is_play_jump_music = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在岸上
        self.is_in_land = True
        # 是否在河里
        self.is_in_river = False

        # 是否起跳
        self.is_jump = False
        # 起跳动画是否播放完毕
        self.jump_is_end_play = False
        # 是否下潜
        self.is_sink = False
        # 下潜动画播放完毕
        self.sink_is_end_play = False
        # 是否升起
        self.is_rise = False

        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.is_play_enter_water_sound = False
        self.name = '潜水'
        self._update_zombie_center_location()

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_in_river:
            self.was_attacked_coord = (left + 42, top + 135)
            self.attack_coord = (left + 32, top + 90)
            self.was_frozen_coord = (left + 60, top + 145)
        elif self.is_in_land:
            self.was_attacked_coord = (left + 47, top + 90)
            self.attack_coord = (left + 32, top + 90)
            self.was_frozen_coord = (left + 60, top + 145)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        if self.is_in_river:
            self.x = x - 188
            self.rect.bottomleft = (self.x, y)
            self.soil.set_surface_location((x, y))
        elif self.is_in_land:
            self.x = x - 60
            self.rect.bottomleft = (self.x, y)
            self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制潜水僵尸"""
        self.surface.fill((0, 255, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 255, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -15, self.height + 10)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            else:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image1 = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image1, -5, self.height + 5)
                self.screen.blit(self.surface1, self.rect1)
            image = handle_index_error(self.body_fall_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 15)
            if self.index == len(self.body_fall_image_list) - 1 and time() - self.last_exist_time >= 2.5:
                # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                self.is_end_play = True
        elif self.is_in_river:  # 在河里面
            if self.is_touch_plant:
                if not self.is_rise:  # 升起的动画播放结束
                    image = handle_index_error(self.attack_image_list, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
                else:
                    image = handle_index_error(self.risk_image_list, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
                    if self.index == len(self.risk_image_list) - 1:
                        self.index = 0
                        self.is_rise = False
            else:  # 潜水状态免疫直线攻击
                image = handle_index_error(self.walk_image_list2, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height - 5)
                self.is_invincible = True
        elif self.is_in_land and not self.was_called:  # 在岸上
            if not self.is_jump and self.is_sink:  # 已经跳下开始潜水
                image = handle_index_error(self.sink_image_list, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.sink_image_list) - 1:
                    self.is_in_river = True
                    self.is_invincible = True
                    self.is_jump = False
                    self.is_sink = False
                    self.index = 0
            elif not self.is_sink and self.is_jump:  # 开始跳下还没有潜水
                image = handle_index_error(self.jump_image_list, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.jump_image_list) - 7 and not self.is_play_enter_water_sound:
                    self.music.play_short_time_sound(self.setting.zombie_enter_water)
                    self.is_play_enter_water_sound = True
                if self.index == len(self.jump_image_list) - 1:
                    self.is_jump = False
                    self.is_sink = True
                    self.index = 0
            elif not self.is_jump and not self.is_sink:  # 既没有跳下也没有潜水
                image = handle_index_error(self.walk_image_list1, self.index)
                if not pause:
                    self._update_zombie_location()
                plot_image(self.surface, image, -5, self.height + 15)
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height + 15:
                    self.image_move_height -= 8.5
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.head_fall_image_list)
                    if self.index < len(self.body_fall_image_list) - 1:
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif self.is_in_river:  # 在水里面
                    if self.is_touch_plant:
                        if not self.is_rise:
                            self.index = (self.index + 1) % len(self.attack_image_list)
                            if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                                self.music.play_short_time_sound(self.setting.zombie_eat)
                                self.last_attack_time = current_time
                                self.is_attack_plant = True
                        else:
                            self.index = (self.index + 1) % len(self.risk_image_list)
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list2)
                elif self.is_in_land and not self.was_called:  # 在岸上
                    if not self.is_jump and self.is_sink:
                        self.index = (self.index + 1) % len(self.sink_image_list)
                    elif self.is_jump and not self.is_sink:
                        self.index = (self.index + 1) % len(self.jump_image_list)
                    elif not self.is_jump and not self.is_sink:
                        self.index = (self.index + 1) % len(self.walk_image_list1)
                elif self.was_called:
                    if self.image_move_height <= self.height + 15 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class DolphinRiderZombie(Sprite):
    """"创建海豚僵尸"""
    def __init__(self, ai_game):
        """海豚僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (220, 220)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 500
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 0.8
        self.original_speed = 0.8
        self.ride_speed = 3
        self.image_move_height = (self.height + 3) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.dolphin_rider_zombie_static
        self.walk_image_list1 = self.setting.dolphin_rider_zombie_walk_in_land_with_dolphin
        self.walk_image_list2 = self.setting.dolphin_rider_zombie_walk_in_river_ride_dolphin
        self.walk_image_list3 = self.setting.dolphin_rider_zombie_walk_in_river_without_dolphin
        self.walk_image_list4 = self.setting.dolphin_rider_zombie_walk_in_land_without_dolphin
        self.enter_water_image_list = self.setting.dolphin_rider_zombie_throw_dolphin
        self.jump_image_list = self.setting.dolphin_rider_zombie_jump
        self.attack_image_list = self.setting.dolphin_rider_zombie_attack_in_river_without_dolphin
        self.die1_image_list = self.setting.dolphin_rider_zombie_die_on_dolphin
        self.body_fall_image_list = self.setting.dolphin_rider_zombie_body_fall_water
        self.head_fall_image_list = self.setting.dolphin_rider_zombie_head_fall
        self.boom_image_list = self.setting.dolphin_rider_zombie_boom
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_exist_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        self.is_play_jump_music = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在岸上
        self.is_in_land = True
        # 是否在河里
        self.is_in_river = False
        # 是否进入水中
        self.is_enter_water = False
        # 准备起跳动画播放完毕
        self.enter_water_is_end_play = False
        # 是否起跳
        self.is_jump = False
        # 起跳动画是否播放完毕
        self.jump_is_end_play = False
        # 被植物射击而死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_lost_dolphin = False
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.is_play_enter_water_sound = False
        self.name = '海豚'
        self._update_zombie_center_location()

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_in_river:
            if self.is_touch_plant:  # 碰到植物然后攻击植物(此时海豚已经丢失)
                self.was_attacked_coord = (left + 60, top + 185)
                self.attack_coord = (left + 40, top + 185)
                self.was_frozen_coord = (left + 70, top + 200)
            else:
                if self.is_lost_dolphin:  # 在河里走没有海豚
                    self.was_attacked_coord = (left + 60, top + 185)
                    self.attack_coord = (left + 40, top + 185)
                    self.was_frozen_coord = (left + 70, top + 200)
                else:  # 在河里骑着海豚走
                    self.was_attacked_coord = (left + 60, top + 165)
                    self.attack_coord = (left + 40, top + 165)
                    self.was_frozen_coord = (left + 80, top + 195)
        elif self.is_in_land:
            if self.is_lost_dolphin:
                self.was_attacked_coord = (left + 47, top + 142)
                self.attack_coord = (left + 32, top + 142)
                self.was_frozen_coord = (left + 65, top + 200)
            else:  # 在陆地上拿着海豚走
                self.was_attacked_coord = (left + 140, top + 145)
                self.attack_coord = (left + 127, top + 145)
                self.was_frozen_coord = (left + 165, top + 205)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        if self.is_in_river:
            self.x = x - 188
            self.rect.bottomleft = (self.x, y)
            self.soil.set_surface_location((x, y))
        elif self.is_in_land:
            self.x = x - 165
            self.rect.bottomleft = (self.x, y)
            self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制海豚僵尸"""
        self._update_zombie_center_location()
        self.surface.fill((0, 255, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 255, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            if self.is_in_land and not self.is_lost_dolphin:
                x = 80
            else:
                x = -15
            plot_image(self.surface, image, x, self.height + 7)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            else:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image1 = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image1, 40, self.height - 10)
                self.screen.blit(self.surface1, self.rect1)
            if self.is_lost_dolphin:
                image = handle_index_error(self.body_fall_image_list, self.index)
                plot_image(self.surface, image, 50, self.height + 3)
                if self.index == len(self.body_fall_image_list) - 1 and time() - self.last_exist_time >= 2.5:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
            else:
                image = handle_index_error(self.die1_image_list, self.index)
                plot_image(self.surface, image, -80, self.height + 3)
                if self.index == len(self.die1_image_list) - 1:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_lost_dolphin = True
                    self.index = 0
        elif self.is_in_river:  # 在河里面
            if self.is_touch_plant:
                if self.is_lost_dolphin and self.jump_is_end_play:  # 碰到了植物并且丢失了海豚,进行攻击动画
                    image = handle_index_error(self.attack_image_list, self.index)
                    plot_image(self.surface, image, 0, self.height + 3)
                else:
                    if self.is_jump and not self.jump_is_end_play:  # 碰到了第一颗植物, 执行跳起动画
                        image = handle_index_error(self.jump_image_list, self.index)
                        plot_image(self.surface, image, 0, self.height + 3)
                        if self.index == len(self.jump_image_list) - 1:
                            self.index = 0
                            self.speed = self.original_speed
                            self.jump_is_end_play = True
                            self.is_lost_dolphin = True
                            self.is_invincible = False
                            self.is_touch_plant = False
                            self.is_jump = False
            else:
                if self.is_lost_dolphin:  # 丢失了海豚行走
                    image = handle_index_error(self.walk_image_list3, self.index)
                    plot_image(self.surface, image, 0, self.height + 3)
                else:  # 没有丢失海豚行走
                    image = handle_index_error(self.walk_image_list2, self.index)
                    plot_image(self.surface, image, -120, self.height + 3)
                if not pause:
                    self._update_zombie_location()
        elif self.is_in_land and not self.was_called:  # 在岸上
            if self.is_lost_dolphin:  # 在陆地上海豚丢了
                image = handle_index_error(self.walk_image_list4, self.index)
                plot_image(self.surface, image, 2, self.height + 3)
                if not pause:
                    self._update_zombie_location()
            else:  # 在陆地上海豚没丢
                if self.is_enter_water:  # 检测到水池
                    image = handle_index_error(self.enter_water_image_list, self.index)
                    plot_image(self.surface, image, 0, self.height + 3)
                    if self.index == len(self.enter_water_image_list) - 1:
                        self.index = 0
                        self.speed = self.ride_speed
                        self.is_enter_water = False
                        self.is_in_land = False
                        self.is_in_river = True
                        self.is_invincible = False
                else:
                    image = handle_index_error(self.walk_image_list1, self.index)
                    plot_image(self.surface, image, 35, self.height + 3)
                    if not pause:
                        self._update_zombie_location()
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, 35, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height + 3:
                    self.image_move_height -= 10.2
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.head_fall_image_list)
                    if self.index < len(self.body_fall_image_list) - 1:
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif self.is_in_river:  # 在水里面
                    if self.is_touch_plant:
                        if self.is_lost_dolphin:
                            if self.is_lost_dolphin and self.jump_is_end_play:
                                self.index = (self.index + 1) % len(self.attack_image_list)
                                if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                                    self.music.play_short_time_sound(self.setting.zombie_eat)
                                    self.last_attack_time = current_time
                                    self.is_attack_plant = True
                        else:
                            if self.is_jump and not self.jump_is_end_play:
                                self.index = (self.index + 1) % len(self.jump_image_list)
                    else:
                        if self.is_lost_dolphin:
                            self.index = (self.index + 1) % len(self.walk_image_list3)
                        else:
                            self.index = (self.index + 1) % len(self.walk_image_list2)
                elif self.is_in_land and not self.was_called:  # 在岸上
                    if self.is_lost_dolphin:
                        self.index = (self.index + 1) % len(self.walk_image_list4)
                    else:
                        if self.is_enter_water:
                            self.index = (self.index + 1) % len(self.enter_water_image_list)
                        else:
                            self.index = (self.index + 1) % len(self.walk_image_list1)
                elif self.was_called:
                    if self.image_move_height <= self.height + 3 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class DuckyDrumZombie(Sprite):
    """"创建鸭子铁桶僵尸"""
    def __init__(self, ai_game):
        """鸭子铁桶僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1370
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.index = 0
        self.zombie_index = 2  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.ducky_drum_zombie_static
        self.walk_image_list1_with_armor = self.setting.ducky_drum_zombie_walk_in_land_with_armor
        self.walk_image_list2_with_armor = self.setting.ducky_drum_zombie_walk_in_river_with_armor
        self.walk_image_list1_without_armor = self.setting.ducky_drum_zombie_walk_in_land_without_armor
        self.walk_image_list2_without_armor = self.setting.ducky_drum_zombie_walk_in_river_without_armor
        self.attack_image_list1 = self.setting.ducky_drum_zombie_attack_with_armor
        self.attack_image_list2 = self.setting.ducky_drum_zombie_attack_without_armor
        self.boom_image_list = self.setting.ducky_drum_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.ducky_drum_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在岸上
        self.is_in_land = True
        # 是否在河里
        self.is_in_river = False
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '鸭子铁桶'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_in_land:
            self.was_attacked_coord = (left + 65, top + 55)
            self.attack_coord = (left + 45, top + 60)
            self.was_frozen_coord = (left + 77, top + 110)
        elif self.is_in_river:
            self.was_attacked_coord = (left + 67, top + 90)
            self.attack_coord = (left + 50, top + 90)
            self.was_frozen_coord = (left + 80, top + 115)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 77
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制鸭子铁桶僵尸"""
        self._update_zombie_center_location()
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
            if self.index == len(self.boom_image_list) - 1:
                self.is_end_play = True
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            image = handle_index_error(self.shot_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
            if self.index == len(self.shot_image_list) - 1 and self.flying_head.is_end_play:
                self.is_end_play = True
        if self.is_in_river and not self.is_dead():
            if self.is_touch_plant:
                if self.is_lost_armor:
                    image = handle_index_error(self.attack_image_list2, self.index)
                    plot_image(self.surface, image, -5, self.height)
                else:
                    image = handle_index_error(self.attack_image_list1, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
            else:
                if self.is_lost_armor:
                    image = handle_index_error(self.walk_image_list2_without_armor, self.index)
                    plot_image(self.surface, image, -5, self.height)
                else:
                    image = handle_index_error(self.walk_image_list2_with_armor, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
                if not pause:
                    self._update_zombie_location()
        elif self.is_in_land and not self.was_called and not self.is_dead():
            if self.is_lost_armor:
                image = handle_index_error(self.walk_image_list1_without_armor, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
            else:
                image = handle_index_error(self.walk_image_list1_with_armor, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
            if not pause:
                self._update_zombie_location()
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.index < len(self.shot_image_list) - 1:
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_in_river and not self.is_dead():
                    if self.is_touch_plant:
                        if self.is_lost_armor:
                            self.index = (self.index + 1) % len(self.attack_image_list2)
                        else:
                            self.index = (self.index + 1) % len(self.attack_image_list1)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        if self.is_lost_armor:
                            self.index = (self.index + 1) % len(self.walk_image_list2_without_armor)
                        else:
                            self.index = (self.index + 1) % len(self.walk_image_list2_with_armor)
                elif self.is_in_land and not self.was_called and not self.is_dead():
                    if self.is_lost_armor:
                        self.index = (self.index + 1) % len(self.walk_image_list1_without_armor)
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list1_with_armor)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if not self.is_lost_armor and was_shoot:
            self.music.play_short_time_sound(self.setting.drum_zombie_was_hit)
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self.is_lost_armor = True
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class DuckyRoadBlockZombie(Sprite):
    """"创建鸭子路障僵尸"""
    def __init__(self, ai_game):
        """鸭子路障僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 640
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.index = 0
        self.zombie_index = 2  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.ducky_roadblock_zombie_static
        self.walk_image_list1_with_armor = self.setting.ducky_roadblock_zombie_walk_in_land_with_armor
        self.walk_image_list2_with_armor = self.setting.ducky_roadblock_zombie_walk_in_river_with_armor
        self.walk_image_list1_without_armor = self.setting.ducky_roadblock_zombie_walk_in_land_without_armor
        self.walk_image_list2_without_armor = self.setting.ducky_roadblock_zombie_walk_in_river_without_armor
        self.attack_image_list1 = self.setting.ducky_roadblock_zombie_attack_with_armor
        self.attack_image_list2 = self.setting.ducky_roadblock_zombie_attack_without_armor
        self.boom_image_list = self.setting.ducky_roadblock_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.ducky_roadblock_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在岸上
        self.is_in_land = True
        # 是否在河里
        self.is_in_river = False
        # 确定该僵尸防具已经掉落
        self.is_lost_armor = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '鸭子路障'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_in_land:
            self.was_attacked_coord = (left + 65, top + 55)
            self.attack_coord = (left + 45, top + 60)
            self.was_frozen_coord = (left + 77, top + 110)
        elif self.is_in_river:
            self.was_attacked_coord = (left + 67, top + 85)
            self.attack_coord = (left + 50, top + 85)
            self.was_frozen_coord = (left + 80, top + 110)
        # rect = pygame.Rect(50, 85, 20, 20)
        # pygame.draw.rect(self.surface, (255, 0, 0), rect)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 77
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制鸭子路障僵尸"""
        self._update_zombie_center_location()
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height)
            if self.index == len(self.boom_image_list) - 1:
                self.is_end_play = True
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            image = handle_index_error(self.shot_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
            if self.index == len(self.shot_image_list) - 1 and self.flying_head.is_end_play:
                self.is_end_play = True
        if self.is_in_river and not self.is_dead():
            if self.is_touch_plant:
                if self.is_lost_armor:
                    image = handle_index_error(self.attack_image_list2, self.index)
                    plot_image(self.surface, image, -5, self.height)
                else:
                    image = handle_index_error(self.attack_image_list1, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
            else:
                if self.is_lost_armor:
                    image = handle_index_error(self.walk_image_list2_without_armor, self.index)
                    plot_image(self.surface, image, -5, self.height)
                else:
                    image = handle_index_error(self.walk_image_list2_with_armor, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
                if not pause:
                    self._update_zombie_location()
        elif self.is_in_land and not self.was_called and not self.is_dead():
            if self.is_lost_armor:
                image = handle_index_error(self.walk_image_list1_without_armor, self.index)
                plot_image(self.surface, image, -5, self.height)
            else:
                image = handle_index_error(self.walk_image_list1_with_armor, self.index)
                plot_image(self.surface, image, -5, self.height)
            if not pause:
                self._update_zombie_location()
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.index < len(self.shot_image_list) - 1:
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_in_river and not self.is_dead():
                    if self.is_touch_plant:
                        if self.is_lost_armor:
                            self.index = (self.index + 1) % len(self.attack_image_list2)
                        else:
                            self.index = (self.index + 1) % len(self.attack_image_list1)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        if self.is_lost_armor:
                            self.index = (self.index + 1) % len(self.walk_image_list2_without_armor)
                        else:
                            self.index = (self.index + 1) % len(self.walk_image_list2_with_armor)
                elif self.is_in_land and not self.was_called and not self.is_dead():
                    if self.is_lost_armor:
                        self.index = (self.index + 1) % len(self.walk_image_list1_without_armor)
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list1_with_armor)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.roadblock_zombie_was_hit)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value
        if not self.is_lost_armor and was_shoot:
            self.music.play_short_time_sound(self.setting.roadblock_zombie_was_hit)
        if 0 < self.health <= self.health_limit and not self.is_lost_armor:
            self.is_lost_armor = True
            self.index = 0

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class DuckyGeneralZombie(Sprite):
    """"创建鸭子普通僵尸"""
    def __init__(self, ai_game):
        """鸭子普通僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self.height = (136, 130)
        self.flying_head = FlyingZombieHead(ai_game, self.width, self.height)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 270
        self.health_limit = 270  # 生命界限
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.speed = 0.3
        self.original_speed = 0.3
        self.index = 0
        self.zombie_index = 2  # 僵尸索引用于区分应该创建哪一个僵尸
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.was_frozen_coord = ()
        self.was_attacked_coord = ()
        self.attack_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.ducky_general_zombie_static
        self.walk_image_list1 = self.setting.ducky_general_zombie_walk_in_land
        self.walk_image_list2 = self.setting.ducky_general_zombie_walk_in_river
        self.attack_image_list = self.setting.ducky_general_zombie_attack
        self.boom_image_list = self.setting.ducky_general_zombie_boom  # 被炸成灰烬的僵尸
        self.shot_image_list = self.setting.ducky_general_zombie_was_shot_to_die  # 被射击而死的僵尸
        self.last_plot_time = time()
        self.last_attack_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否在岸上
        self.is_in_land = True
        # 是否在河里
        self.is_in_river = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '鸭子普通'
        self._update_zombie_center_location()

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        if self.is_in_land:
            self.was_attacked_coord = (left + 65, top + 55)
            self.attack_coord = (left + 45, top + 60)
            self.was_frozen_coord = (left + 77, top + 110)
        elif self.is_in_river:
            self.was_attacked_coord = (left + 67, top + 85)
            self.attack_coord = (left + 50, top + 85)
            self.was_frozen_coord = (left + 80, top + 110)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 77
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制鸭子普通僵尸"""
        self._update_zombie_center_location()
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -5, self.height)
            if self.index == len(self.boom_image_list) - 1:
                self.is_end_play = True
        elif self.was_shot_to_die:  # 如果被射死
            if not self.flying_head.is_end_play:
                self.flying_head.show_head(pause)
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            image = handle_index_error(self.shot_image_list, self.index)
            plot_image(self.surface, image, -5, self.height - 5)
            if self.index == len(self.shot_image_list) - 1 and self.flying_head.is_end_play:
                self.is_end_play = True
        if self.is_in_river and not self.is_dead():
            if self.is_touch_plant:
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -5, self.height)
            else:
                image = handle_index_error(self.walk_image_list2, self.index)
                plot_image(self.surface, image, -5, self.height)
                if not pause:
                    self._update_zombie_location()
        elif self.is_in_land and not self.was_called and not self.is_dead():
            image = handle_index_error(self.walk_image_list1, self.index)
            plot_image(self.surface, image, -5, self.height)
            if not pause:
                self._update_zombie_location()
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 5.7
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.index < len(self.shot_image_list) - 1:
                        self.index = (self.index + 1) % len(self.shot_image_list)
                elif self.is_in_river and not self.is_dead():
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        self.index = (self.index + 1) % len(self.walk_image_list2)
                elif self.is_in_land and not self.was_called and not self.is_dead():
                    self.index = (self.index + 1) % len(self.walk_image_list1)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.roadblock_zombie_was_hit)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class DancingZombie(Sprite):
    """"创建舞王僵尸"""
    def __init__(self, ai_game):
        """"舞王僵尸基本属性"""
        super().__init__()
        self.ai_game = ai_game
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (150, 160)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 1000
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 2
        self.original_speed = 0.8
        self.distance_limit = 550  # 舞王僵尸进入场内的距离限制
        self.call_interval_time = 10  # 召唤僵尸所间隔的时间
        self.call_waste_time = 1.8  # 召唤僵尸需要花费的时间
        self.image_move_height = (self.height + 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.center_coord = ()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = (self.setting.appear_locations[self.lattice_index][0],
                                self.setting.appear_locations[self.lattice_index][1])
        self.x = float(self.rect.x)
        self.original_location = self.x  # 舞王僵尸进入场内的起始位置
        self.static_image_list = self.setting.dancing_zombie_static
        self.enter_image_list = self.setting.dancing_zombie_enter_ground
        self.call_image_list = self.setting.dancing_zombie_called
        self.sway_image_list = self.setting.dancing_zombie_sway
        self.dancing_image_list = self.setting.dancing_zombie_dancing
        self.attack_image_list = self.setting.dancing_zombie_attack
        self.enter_image_list_without_head = self.setting.dancing_zombie_enter_ground_without_head
        self.call_image_list_without_head = self.setting.dancing_zombie_called_without_head
        self.sway_image_list_without_head = self.setting.dancing_zombie_sway_without_head
        self.dancing_image_list_without_head = self.setting.dancing_zombie_dancing_without_head
        self.attack_image_list_without_head = self.setting.dancing_zombie_attack_without_head
        self.boom_image_list = self.setting.dancing_zombie_boom
        self.body_fall_image_list = self.setting.dancing_zombie_body_fall  # 身体落下
        self.head_fall_image_list = self.setting.dancing_zombie_head_fall  # 头落下
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_call_time = 0  # 上一次召唤僵尸的时间
        self.last_wait_time = 0  # 最初到了召唤的的时候的时间
        self.last_exist_time = 0
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否能够被修改状态：
        self.is_can_be_change = True
        # 是否等待舞王僵尸召唤僵尸
        self.is_wait = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否播放进入场内的动画
        self.is_enter = True
        # 是否结束播放进入动画
        self.enter_is_end_play = False
        # 是否召唤僵尸
        self.is_call = False
        # 召唤动画播放结束
        self.call_is_end_play = False
        # 是否摇摆而死
        self.is_sway = False
        # 摇摆而死的动画播放完毕
        self.sway_is_end_play = False
        # 是否跳舞而死
        self.is_dance = False
        # 跳舞而死的动画播放完毕
        self.dance_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '舞王'
        self._update_zombie_center_location()

    def _call_four_zombie(self):
        """召唤四个僵尸，分别在上下左右"""
        if self.lattice_index == 0:
            # 本行
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] - 120, self.rect.bottom)
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] + 120, self.rect.bottom)
            # 下一行
            take_and_back_zombie(self.ai_game, self.lattice_index + 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index + 1][1])
        elif self.lattice_index == 1:
            # 上下
            take_and_back_zombie(self.ai_game, self.lattice_index - 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index - 1][1])
            take_and_back_zombie(self.ai_game, self.lattice_index + 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index + 1][1])
            # 左右
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] - 120, self.rect.bottom)
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] + 120, self.rect.bottom)
        elif self.lattice_index == 2:
            # 上下
            take_and_back_zombie(self.ai_game, self.lattice_index - 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index - 1][1])
            take_and_back_zombie(self.ai_game, self.lattice_index + 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index + 1][1])
            # 左右
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] - 120, self.rect.bottom)
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] + 120, self.rect.bottom)
        elif self.lattice_index == 3:
            # 上下
            take_and_back_zombie(self.ai_game, self.lattice_index - 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index - 1][1])
            take_and_back_zombie(self.ai_game, self.lattice_index + 1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index + 1][1])
            # 左右
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] - 120, self.rect.bottom)
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] + 120, self.rect.bottom)
        elif self.lattice_index == 4:
            # 上一行
            take_and_back_zombie(self.ai_game, self.lattice_index-1,
                                 self.center_coord[0], self.setting.appear_locations[self.lattice_index-1][1])
            # 本行
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] - 120, self.rect.bottom)
            take_and_back_zombie(self.ai_game, self.lattice_index, self.center_coord[0] + 120, self.rect.bottom)

    def _check_is_collide_plant(self):
        """检测是否碰撞到该行的植物"""
        for plant in self.ai_game.plants_lists[self.lattice_index]:
            if plant.can_be_destroy:
                plant_left = plant.was_attacked_coord[0]
                plant_right = plant.was_attacked_coord[1]
                if plant_left <= self.attack_coord[0] <= plant_right:
                    if self.is_call:
                        if self.is_touch_plant:
                            self.is_touch_plant = False
                            self.is_can_be_change = False
                            self .index = 0
                            break

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()
            if self.is_enter and self.original_location - self.x >= self.distance_limit:
                self.index = 0
                self.is_enter = False
                self.is_call = True
                self.is_invincible = True
                self.is_can_be_change = False
                self.speed = self.original_speed

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 50, top + 82)
        self.attack_coord = (left + 30, top + 82)
        self.was_frozen_coord = (left + 50, top + 137)
        self.center_coord = (left + 70, top + self.height)
        # rect = pygame.Rect(50, self.height, 20, 20)
        # pygame.draw.rect(self.surface, (255, 0, 0), rect)

    def _work_call_time(self):
        """计算舞王僵尸是否到了召唤僵尸的时候"""
        current_time = time()
        if (self.last_call_time != 0 and current_time - self.last_call_time >= self.call_interval_time
                and not self.is_call):
            self.index = 0
            self.is_call = True
            self.is_invincible = True
            self.is_attack = False
            self.is_dance = False
            self.is_sway = False
            self.is_touch_plant = False
            self.is_can_be_change = False

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 50
        self.rect.bottomleft = (self.x, y)
        self.original_location = self.x
        self.distance_limit = 100
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制舞王僵尸"""
        self._check_is_collide_plant()
        self.surface.fill((0, 255, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 255, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, 10, self.height + 2)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            if self.is_get_dead_location:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image, -5, self.height)
                self.screen.blit(self.surface1, self.rect1)

            if self.is_enter and not self.enter_is_end_play:
                image = handle_index_error(self.enter_image_list_without_head, self.index)
                plot_image(self.surface, image, -35, self.height + 10)
                if not pause:
                    self._update_zombie_location()
                if self.index == len(self.enter_image_list_without_head) - 1:
                    self.enter_is_end_play = True
                    self.is_enter = False
                    self.index = 0
            elif self.is_sway and not self.sway_is_end_play:
                image = handle_index_error(self.sway_image_list_without_head, self.index)
                plot_image(self.surface, image, -20, self.height + 5)
                if not pause:
                    self._update_zombie_location()
                if self.index == len(self.sway_image_list_without_head) - 1:
                    self.sway_is_end_play = True
                    self.is_sway = False
                    self.index = 0
            elif self.is_call and not self.call_is_end_play:
                image = handle_index_error(self.call_image_list_without_head, self.index)
                plot_image(self.surface, image, 0, self.height + 5)
                if self.index == len(self.call_image_list_without_head) - 1:
                    self.call_is_end_play = True
                    self.is_call = False
                    self.index = 0
            elif self.is_dance and not self.dance_is_end_play:
                image = handle_index_error(self.dancing_image_list_without_head, self.index)
                plot_image(self.surface, image, -5, self.height + 5)
                if self.index == len(self.dancing_image_list_without_head) - 1:
                    self.dance_is_end_play = True
                    self.is_dance = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, 0, self.height + 2)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif (not self.is_sway and not self.is_dance and not self.is_attack and not self.is_enter
                  and not self.is_call):
                image = handle_index_error(self.body_fall_image_list, self.index)
                plot_image(self.surface, image, -10, self.height + 3)
                if self.index == len(self.body_fall_image_list) - 1 and time() - self.last_exist_time >= 2.5:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif not self.is_dead() and not self.was_called:  # 正常行走状态
            self._work_call_time()
            if self.is_enter:  # 默认让舞王播放进入动画
                image = handle_index_error(self.enter_image_list, self.index)
                plot_image(self.surface, image, -45, self.height)
                if not pause:
                    self._update_zombie_location()
            elif self.is_touch_plant and not self.is_enter and not self.is_call:
                if not self.is_attack:
                    self.is_attack = True
                    self.is_sway = False
                    self.is_dance = False
                    self.is_call = False
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, 0, self.height + 2)
            elif not self.is_touch_plant and not self.is_enter:
                if self.is_call:
                    current_time = time()
                    image = handle_index_error(self.call_image_list, self.index)
                    plot_image(self.surface, image, 0, self.height + 2)
                    if self.index == len(self.call_image_list) - 1 and not self.is_wait:
                        self._call_four_zombie()
                        self.is_wait = True
                        self.last_wait_time = current_time
                    elif self.is_wait and current_time - self.last_wait_time >= self.call_waste_time:
                        self.last_call_time = current_time
                        self.index = 0
                        self.is_wait = False
                        self.is_call = False
                        self.is_invincible = False
                        self.is_can_be_change = True
                        num = randint(0, 1)
                        if num == 0:
                            self.is_sway = True
                            self.is_dance = False
                        else:
                            self.is_sway = False
                            self.is_dance = True
                else:
                    if self.is_attack:
                        self.is_attack = False
                    if self.is_dance and not self.is_sway:
                        image = handle_index_error(self.dancing_image_list, self.index)
                        plot_image(self.surface, image, -1, self.height + 5)
                        if self.index == len(self.dancing_image_list) - 1:
                            self.is_dance = False
                            self.is_sway = True
                    elif not self.is_dance and self.is_sway:
                        image = handle_index_error(self.sway_image_list, self.index)
                        plot_image(self.surface, image, -18, self.height + 5)
                        if not pause:
                            self._update_zombie_location()
                        if self.index == len(self.sway_image_list) - 1:
                            self.is_dance = True
                            self.is_sway = False
                    elif not self.is_dance and not self.is_sway:  # 如果没有动作就随机产生一个动作
                        num = randint(0, 1)
                        if num == 0:
                            self.is_sway = True
                            self.is_dance = False
                        else:
                            self.is_sway = False
                            self.is_dance = True
                        self.index = 0
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height + 5:
                    self.image_move_height -= 7.9
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)
        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.body_fall_image_list)
                    if self.is_enter and not self.enter_is_end_play:
                        self.index = (self.index + 1) % len(self.enter_image_list_without_head)
                    elif self.is_call and not self.call_is_end_play:
                        self.index = (self.index + 1) % len(self.call_image_list_without_head)
                    elif self.is_sway and not self.sway_is_end_play:
                        self.index = (self.index + 1) % len(self.sway_image_list_without_head)
                    elif self.is_dance and not self.dance_is_end_play:
                        self.index = (self.index + 1) % len(self.dancing_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif (not self.is_sway and not self.is_dance and not self.is_attack
                          and not self.is_call and not self.is_enter
                          and self.index < len(self.body_fall_image_list) - 1):
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif not self.is_dead() and not self.was_called:  # 正常行走状态
                    if self.is_enter:
                        self.index = (self.index + 1) % len(self.enter_image_list)
                    elif self.is_touch_plant and not self.is_enter and not self.is_enter:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    elif not self.is_touch_plant and not self.is_enter:
                        if self.is_call:
                            if self.index < len(self.call_image_list) - 1:
                                self.index = (self.index + 1) % len(self.call_image_list)
                        else:
                            if self.is_dance and not self.is_sway:
                                self.index = (self.index + 1) % len(self.dancing_image_list)
                            elif not self.is_dance and self.is_sway:
                                self.index = (self.index + 1) % len(self.sway_image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height + 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass


class BuckupDancerZombie(Sprite):
    """"创建后援僵尸"""
    def __init__(self, ai_game):
        """"后援僵尸基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.music = ai_game.music
        self.width, self. height = (136, 160)
        self.soil = ZombieAppearSoil(ai_game)
        self.health = 270
        self.hurt = 70
        self.hurt_interval = 0.15  # 伤害间隔时间
        self.index = 0
        self.head_index = 0
        self.zombie_index = 4  # 僵尸索引用于区分应该创建哪一个僵尸
        self.speed = 1
        self.original_speed = 1
        self.image_move_height = (self.height - 5) * 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((self.width, self.height))
        self.rect1 = self.surface1.get_rect()
        self.rect = self.surface.get_rect()
        self.attack_coord = ()
        self.was_attacked_coord = ()
        self.was_frozen_coord = ()
        self.lattice_index = randint(0, 4)
        self.rect.bottomleft = self.setting.appear_locations[self.lattice_index]
        self.static_image_list = self.setting.backup_dancer_zombie_static
        self.sway_image_list = self.setting.backup_dancer_zombie_sway
        self.dancing_image_list = self.setting.backup_dancer_zombie_dancing
        self.attack_image_list = self.setting.backup_dancer_zombie_attack
        self.sway_image_list_without_head = self.setting.backup_dancer_zombie_sway_without_head
        self.dancing_image_list_without_head = self.setting.backup_dancer_zombie_dancing_without_head
        self.attack_image_list_without_head = self.setting.backup_dancer_zombie_attack_without_head
        self.boom_image_list = self.setting.backup_dancer_zombie_boom
        self.body_fall_image_list = self.setting.backup_dancer_zombie_body_fall  # 身体落下
        self.head_fall_image_list = self.setting.backup_dancer_zombie_head_fall  # 头落下
        self.last_plot_time = 0
        self.last_attack_time = 0
        self.last_exist_time = 0
        self.x = float(self.rect.x)
        # 是否无敌
        self.is_invincible = False
        self.was_called = False
        # 是否接触植物
        self.is_touch_plant = False
        # 接触了植物是否处于攻击状态
        self.is_attack_plant = False
        # 是否摇摆而死
        self.is_sway = False
        # 摇摆而死的动画播放完毕
        self.sway_is_end_play = False
        # 是否跳舞而死
        self.is_dance = True
        # 跳舞而死的动画播放完毕
        self.dance_is_end_play = False
        # 是否攻击而死
        self.is_attack = False
        # 攻击而死的动画播放完毕
        self.attack_is_end_play = False
        # 被植物射击打死
        self.was_shot_to_die = False
        # 接触植物而死
        self.was_collided_to_die = False
        # 被炸成灰而死
        self.was_boom_to_die = False
        # 每一种死法的最后一帧
        self.is_end_play = False
        self.is_static = False
        self.can_be_controlled = True
        self.is_get_dead_location = False
        self.is_frozen_time = 0
        self.is_play_head_to_fly_sound = False
        self.name = '后援'
        self._update_zombie_center_location()

    def _get_current_location(self):
        """从当前僵尸死亡的位置获取坐标"""
        self.rect1.bottomleft = self.rect.bottomleft

    def _update_zombie_location(self):
        """更新僵尸的位置"""
        if self.attack_coord[0] > self.setting.zombie_move_limit:
            self.x -= self.speed
            self.rect.x = self.x
            self._update_zombie_center_location()

    def _update_zombie_center_location(self):
        """实时更新僵尸的中心位置"""
        left, top = self.rect.left, self.rect.top
        self.was_attacked_coord = (left + 50, top + 82)
        self.attack_coord = (left + 30, top + 82)
        self.was_frozen_coord = (left + 50, top + 135)

    def is_dead(self):
        """根据僵尸血量确认是否标记僵尸"""
        if self.health <= 0:
            return True
        return False

    def is_the_zombie_really_dead(self):
        """根据死亡方式的最后一帧播放完毕确认僵尸真正意义上的死亡"""
        if self.is_end_play:
            return True
        return False

    def reset_location(self, x, y):
        self.x = x - 50
        self.rect.bottomleft = (self.x, y)
        self.soil.set_surface_location((x, y))

    def show_zombie(self, pause, interval_time=0.1):
        """"在屏幕上绘制后援僵尸"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.was_boom_to_die:  # 被炸死的状态
            image = handle_index_error(self.boom_image_list, self.index)
            plot_image(self.surface, image, -10, self.height + 2)
        elif self.was_shot_to_die:  # 如果被射死
            if not self.is_play_head_to_fly_sound:
                self.music.play_short_time_sound(self.setting.zombie_head_fly)
                self.is_play_head_to_fly_sound = True
            if not self.is_get_dead_location:
                self._get_current_location()
                self.is_get_dead_location = True
                self.last_exist_time = time()
            if self.is_get_dead_location:
                self.surface1.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
                self.surface1.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
                image = handle_index_error(self.head_fall_image_list, self.head_index)
                plot_image(self.surface1, image, -5, self.height)
                self.screen.blit(self.surface1, self.rect1)

            if self.is_sway and not self.sway_is_end_play:
                image = handle_index_error(self.sway_image_list_without_head, self.index)
                plot_image(self.surface, image, -20, self.height - 5)
                if not pause:
                    self._update_zombie_location()
                if self.index == len(self.sway_image_list_without_head) - 1:
                    self.sway_is_end_play = True
                    self.is_sway = False
                    self.index = 0
            elif self.is_dance and not self.dance_is_end_play:
                image = handle_index_error(self.dancing_image_list_without_head, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.dancing_image_list_without_head) - 1:
                    self.dance_is_end_play = True
                    self.is_dance = False
                    self.index = 0
            elif self.is_attack and not self.attack_is_end_play:
                image = handle_index_error(self.attack_image_list_without_head, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
                if self.index == len(self.attack_image_list_without_head) - 1:
                    self.attack_is_end_play = True
                    self.is_attack = False
                    self.index = 0
            elif not self.is_sway and not self.is_dance and not self.is_attack:
                image = handle_index_error(self.body_fall_image_list, self.index)
                plot_image(self.surface, image, -30, self.height - 5)
                if self.index == len(self.body_fall_image_list) - 1 and time() - self.last_exist_time >= 2.5:
                    # 最后一帧播放结束且停留时间到达预期就设置播放完毕
                    self.is_end_play = True
        elif not self.is_dead() and not self.was_called:  # 正常行走状态
            if self.is_touch_plant:
                if not self.is_attack:
                    self.is_attack = True
                    self.is_sway = False
                    self.is_dance = False
                image = handle_index_error(self.attack_image_list, self.index)
                plot_image(self.surface, image, -5, self.height - 5)
            else:
                if self.is_attack:
                    self.is_attack = False
                if self.is_dance and not self.is_sway:
                    image = handle_index_error(self.dancing_image_list, self.index)
                    plot_image(self.surface, image, -5, self.height - 5)
                    if self.index == len(self.dancing_image_list) - 1:
                        self.is_dance = False
                        self.is_sway = True
                elif not self.is_dance and self.is_sway:
                    image = handle_index_error(self.sway_image_list, self.index)
                    plot_image(self.surface, image, -15, self.height - 5)
                    if not pause:
                        self._update_zombie_location()
                    if self.index == len(self.sway_image_list) - 1:
                        self.is_dance = True
                        self.is_sway = False
        elif self.was_called:
            image = handle_index_error(self.static_image_list, self.index)
            plot_image(self.surface, image, -5, self.image_move_height)
            if self.soil.is_play_one_frame:
                if self.image_move_height > self.height - 5:
                    self.image_move_height -= 7.9
        self._update_zombie_center_location()
        self.screen.blit(self.surface, self.rect)
        if self.was_called:
            self.soil.show_soil(pause)

        if not pause and not self.is_static:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.was_boom_to_die:  # 被炸成灰的图片
                    self.index = (self.index + 1) % len(self.boom_image_list)
                    if len(self.boom_image_list) - 1 == self.index:
                        self.is_end_play = True
                elif self.was_shot_to_die:  # 被射死的图片
                    if self.head_index < len(self.head_fall_image_list) - 1:
                        self.head_index = (self.head_index + 1) % len(self.body_fall_image_list)
                    if self.is_sway and not self.sway_is_end_play:
                        self.index = (self.index + 1) % len(self.sway_image_list_without_head)
                    elif self.is_dance and not self.dance_is_end_play:
                        self.index = (self.index + 1) % len(self.dancing_image_list_without_head)
                    elif self.is_attack and not self.attack_is_end_play:
                        self.index = (self.index + 1) % len(self.attack_image_list_without_head)
                    elif (not self.is_sway and not self.is_dance and not self.is_attack and
                          self.index < len(self.body_fall_image_list) - 1):
                        # 让索引只增加到最后一张图片之后就不再改变
                        self.index = (self.index + 1) % len(self.body_fall_image_list)
                elif not self.is_dead() and not self.was_called:  # 正常行走状态
                    if self.is_touch_plant:
                        self.index = (self.index + 1) % len(self.attack_image_list)
                        if self.index == 3 and current_time - self.last_attack_time >= self.hurt_interval:
                            self.music.play_short_time_sound(self.setting.zombie_eat)
                            self.last_attack_time = current_time
                            self.is_attack_plant = True
                    else:
                        if self.is_dance and not self.is_sway:
                            self.index = (self.index + 1) % len(self.dancing_image_list)
                        elif not self.is_dance and self.is_sway:
                            self.index = (self.index + 1) % len(self.sway_image_list)
                elif self.was_called:
                    if self.image_move_height <= self.height - 5 and self.soil.is_end_play:
                        self.was_called = False
                        self.is_invincible = False
                self.last_plot_time = current_time

    def update_collided_plant_health(self, plant):
        """更新碰撞到的植物生命"""
        if self.is_attack_plant and not self.is_static:
            plant.health -= self.hurt
            if plant.health <= 0:
                self.music.play_short_time_sound(self.setting.zombie_eat_finish)
            self.is_attack_plant = False

    def update_zombie_health(self, hurt_value, was_shoot=True):
        """计算僵尸受到的伤害"""
        self.health -= hurt_value

    def update_zombie_move_status(self):
        """根据死亡时机确定僵尸以何种形式倒下"""
        pass
