import pygame
from time import time
from pygame.sprite import Sprite


# ××××××××××××××××××××××××××××××××××××××下面是所有子弹特效类××××××××××××××××××××××××××××××××××××××××××××××
class PeaBreak:
    """豌豆破裂"""
    def __init__(self, ai_game, *surface_size):
        """"寒冰基本属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = surface_size
        self.index = 0
        self.pea_break_time = 0
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.broken_pea_bullet
        self.last_plot_time = time()
        self.is_end_play = False

    def set_surface_location(self, coord, *extra):
        """从死亡的僵尸那里获取坐标"""
        self.rect.center = coord

    def show_break_pea(self, pause):
        """"在屏幕上绘制破裂的豌豆"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色

        image = self.image_list[self.index]
        rect = image.get_rect()
        rect.bottomleft = (0, self.height)
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)

        if not pause:
            current_time = time()
            self.index = (self.index + 1) % len(self.image_list)
            if current_time - self.pea_break_time >= 0.1:  # 破裂豌豆出现时间
                self.is_end_play = True


class BurningFire:
    """燃烧的火焰"""
    def __init__(self, ai_game, *surface_size):
        """"火焰基本属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = surface_size
        self.index = 0
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.burning_fire
        self.last_plot_time = time()
        self.is_end_play = False

    def set_surface_location(self, coord, *extra):
        """从死亡的僵尸哪里获取坐标"""
        self.rect.center = coord

    def show_fire(self, pause, interval_time=0.03):
        """"在屏幕上绘制燃烧的火焰"""
        self.surface.fill((245, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((245, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色

        image = self.image_list[self.index]
        rect = image.get_rect()
        rect.bottomleft = (0, self.height)
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)

        if not pause:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.index < len(self.image_list) - 1:
                    self.index = (self.index + 1) % len(self.image_list)
                else:
                    self.is_end_play = True
                self.last_plot_time = current_time


class Ice:
    """寒冰"""
    def __init__(self, ai_game, *surface_size):
        """"寒冰基本属性"""
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.width, self.height = surface_size
        self.index = 0
        self.ice_time = 1.5
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.image_list = self.setting.ice
        self.last_plot_time = time()
        self.ice_apper_time = 0
        self.is_end_play = False

    def set_surface_location(self, coord):
        """从死亡的僵尸哪里获取坐标"""
        self.rect.center = coord

    def show_ice(self, pause):
        """"在屏幕上绘制寒冰"""
        self.surface.fill((0, 0, 125))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 125))  # 用于将操作台内指定的RGB颜色设置为透明色

        image = self.image_list[self.index]
        rect = image.get_rect()
        rect.bottomleft = (0, self.height)
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)

        if not pause:  # 僵尸只有在非暂停状态时才更新动作
            current_time = time()
            if current_time - self.ice_apper_time >= self.ice_time:
                self.is_end_play = True


# ××××××××××××××××××××××××××××××××××××××下面是所有子弹类××××××××××××××××××××××××××××××××××××××××××××××
class Pea(Sprite):
    """豌豆"""
    def __init__(self, ai_game):
        """初始化基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.path = self.setting.pea_gif
        self.width, self.height = (30, 30)
        self.pea_break = PeaBreak(ai_game, 40, 40)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.hurt = 20
        self.speed = 7
        self.index = 0
        self.image_list = self.setting.pea_bullet
        self.last_plot_time = time()
        self.is_hit = False
        self.is_end_play = False

    def _update_location(self, pause):
        """实时更新子弹位置"""
        if not pause:
            x = float(self.rect.x)
            x += self.speed
            self.rect.x = x

    def check_is_surpass_distance(self):
        """检查子弹是否超过设定的距离"""
        if self.rect.x >= self.setting.pea_max_distance:
            return True
        return False

    def _update_image(self, pause, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        image = self.image_list[self.index]
        self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        rect = image.get_rect()
        rect.topleft = (0, 0)
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)
        if not pause:
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time

    def draw_bullet(self, pause):
        """更新并绘制子弹"""
        if not self.is_hit:
            self._update_image(pause)
            self._update_location(pause)
        else:
            if not self.pea_break.is_end_play:
                self.pea_break.show_break_pea(pause)
            else:
                self.is_end_play = True

    def reset_location(self, plant, x=20, y=20):
        """根据检索到的植物位置设置其子弹相应的位置"""
        if x == 20 and y == 20:  # 没有新的x,y坐标传过来的情况, 默认从植物的右边顶部计算发射位置
            set_x, set_y = plant.attack_coord
        else:
            set_x = plant.attack_coord[0]
            set_y = y
        self.rect.midleft = (set_x, set_y)


class IcePea(Sprite):
    """寒冰豌豆"""
    def __init__(self, ai_game):
        """初始化基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.path = self.setting.ice_pea_gif
        self.width, self.height = (30, 30)
        self.ice = Ice(ai_game, 60, 40)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.hurt = 20
        self.speed = 7
        self.index = 0
        self.image_list = self.setting.ice_pea_bullet
        self.last_plot_time = time()
        self.is_hit = False
        self.is_end_play = False

    def _update_location(self, pause):
        """实时更新子弹位置"""
        if not pause:
            x = float(self.rect.x)
            x += self.speed
            self.rect.x = x

    def check_is_surpass_distance(self):
        """检查子弹是否超过设定的距离"""
        if self.rect.x >= self.setting.pea_max_distance:
            return True
        return False

    def _update_image(self, pause, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        image = self.image_list[self.index]
        self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        rect = image.get_rect()
        rect.topleft = (0, 0)
        self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)
        if not pause:
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                self.index = (self.index + 1) % len(self.image_list)  # 每一次绘制图片之后都会索引都会往下一个，这是一个很好的设计思路
                self.last_plot_time = current_time

    def draw_bullet(self, pause):
        """更新并绘制子弹"""
        if not self.is_hit:
            self._update_image(pause)
            self._update_location(pause)
        else:
            if not self.ice.is_end_play:
                self.ice.show_ice(pause)
            else:
                self.is_end_play = True

    def reset_location(self, plant, x=20, y=20):
        """根据检索到的植物位置设置其子弹相应的位置"""
        if x == 20 and y == 20:  # 没有新的x,y坐标传过来的情况, 默认从植物的右边顶部计算发射位置
            set_x, set_y = plant.attack_coord
        else:
            set_x = plant.attack_coord[0]
            set_y = y
        self.rect.midleft = (set_x, set_y)


class FirePea(Sprite):
    """火焰豌豆"""
    def __init__(self, ai_game):
        """初始化基本属性"""
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.surface
        self.path = self.setting.fire_pea_gif
        self.width, self.height = (85, 50)
        self.burn_fire = BurningFire(ai_game, 60, 20)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.hurt = 40
        self.speed = 10
        self.index = 0
        self.level = 1
        self.image_list1 = self.setting.fire_pea_bullet1
        self.image_list2 = self.setting.fire_pea_bullet2
        self.last_plot_time = time()
        self.is_hit = False
        self.is_end_play = False

    def _update_location(self, pause):
        """实时更新子弹位置"""
        if not pause:
            x = float(self.rect.x)
            x += self.speed
            self.rect.x = x

    def check_is_surpass_distance(self):
        """检查子弹是否超过设定的距离"""
        if self.rect.x >= self.setting.pea_max_distance:
            return True
        return False

    def _update_image(self, pause, interval_time=0.05):
        """从列表中按照正常顺序读取一帧"""
        self.surface.fill((0, 0, 0))  # 该语句不可少，用于每次移除上一帧的图像
        self.surface.set_colorkey((0, 0, 0))  # 用于将操作台内指定的RGB颜色设置为透明色
        if self.level == 1:
            image = self.image_list1[self.index]
            rect = image.get_rect()
            rect.topleft = (0, 5)
            self.surface.blit(image, rect)
        if self.level == 2:
            image = self.image_list2[self.index]
            rect = image.get_rect()
            rect.topleft = (0, 0)
            self.surface.blit(image, rect)
        self.screen.blit(self.surface, self.rect)
        if not pause:
            current_time = time()
            if current_time - self.last_plot_time >= interval_time:
                if self.level == 1:
                    self.index = (self.index + 1) % len(self.image_list1)
                elif self.level == 2:
                    self.index = (self.index + 1) % len(self.image_list2)
                self.last_plot_time = current_time

    def draw_bullet(self, pause):
        """更新并绘制子弹"""
        if not self.is_hit:
            self._update_image(pause)
            self._update_location(pause)
        else:
            if not self.burn_fire.is_end_play:
                self.burn_fire.show_fire(pause)
            else:
                self.is_end_play = True

    def reset_location(self, plant, x=20, y=20):
        """根据检索到的植物位置设置其子弹相应的位置"""
        if x == 20 and y == 20:  # 没有新的x,y坐标传过来的情况, 默认从植物的右边顶部计算发射位置
            set_x, set_y = plant.attack_coord
        else:
            set_x = plant.attack_coord[0]
            set_y = y
        self.rect.midleft = (set_x, set_y)
