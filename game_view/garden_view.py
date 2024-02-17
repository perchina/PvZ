import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group


class Area(Sprite):
    """创建可以被检测到的区域"""
    def __init__(self):
        super().__init__()
        self.width, self.height = (80, 60)
        self._create_area()

    def _create_area(self):
        """创建可被检测到的矩形区域"""
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        # self.surface.fill((255, 255, 255))

    def reset_area_location(self, x, y):
        self.rect.topleft = (x, y)


class Container(Sprite):
    """花园中的工具容器"""
    def __init__(self, setting):
        super().__init__()
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_container_image()

    def _load_container_image(self):
        """加载容器图片"""
        image = pygame.image.load(self.setting.tool_container)
        self.container = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.container.get_rect()

    def reset_container_location(self, x, y):
        self.rect.topleft = (x, y)


class Kettle:
    """创建水壶"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_kettle_image()

    def _load_kettle_image(self):
        """水壶图片"""
        image = pygame.image.load(self.setting.kettle)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class TreeFood:
    """创建肥料"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_tree_food_image()

    def _load_tree_food_image(self):
        """肥料图片"""
        image = pygame.image.load(self.setting.tree_food)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class BugSpray:
    """创建水壶"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_bug_spray_image()

    def _load_bug_spray_image(self):
        """杀虫剂图片"""
        image = pygame.image.load(self.setting.bug_spray)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class Phonograph:
    """创建音乐播放器"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_phonograph_image()

    def _load_phonograph_image(self):
        """播放器图片"""
        image = pygame.image.load(self.setting.phonograph)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class Glove:
    """创建水壶"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_glove_image()

    def _load_glove_image(self):
        """手套图片"""
        image = pygame.image.load(self.setting.glove)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class ZenMoney:
    """创建水壶"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_zen_money_image()

    def _load_zen_money_image(self):
        """兑换器图片"""
        image = pygame.image.load(self.setting.zen_money)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class ZenWheelBarrow:
    """创建水壶"""
    def __init__(self, setting):
        """基本属性设置"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.066, self.setting.screen_width * 0.066)
        self._load_zen_wheel_barrow_image()

    def _load_zen_wheel_barrow_image(self):
        """小推车图片"""
        image = pygame.image.load(self.setting.zen_wheel_barrow)
        self.shape = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.shape.get_rect()

    def set_location(self, sprite):
        """从传过来的精灵获取位置"""
        self.rect.center = sprite.rect.center

    def reset_location(self, x, y):
        """重新设置其位置"""
        # 保证鼠标点位于图像正中央
        x += self.width / 2
        y += self.height / 2
        self.rect.center = (x, y)


class MainMenu:
    """菜单按钮"""
    def __init__(self, setting):
        """菜单基本属性"""
        self.setting = setting
        self.text_color = (0, 216, 0)
        self.width, self.height = (self.setting.screen_width * 0.091, self.setting.screen_height * 0.0505)
        self.font = pygame.font.SysFont('tahoma', int(self.setting.screen_height * 0.037))
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.879, 0)
        self._load_main_menu_image()

    def _load_main_menu_image(self):
        """加载主菜单图片"""
        image = pygame.image.load(self.setting.menu)
        self.main_menu = pygame.transform.scale(image, (self.width, self.height))
        self.surface.blit(self.main_menu, (0, 0))


class GardenStore:
    """花园中的商店"""
    def __init__(self, setting):
        """初始化商店属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.101, self.setting.screen_height * 0.101)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.899, self.setting.screen_height * 0.059)
        self._load_store_image()

    def _load_store_image(self):
        """加载并设置商店图片"""
        image1 = pygame.image.load(self.setting.garden_store_dark)
        image2 = pygame.image.load(self.setting.garden_store_light)
        self.store_dark = pygame.transform.scale(image1, (self.width, self.height))
        self.store_light = pygame.transform.scale(image2, (self.width, self.height))

    def plot_store(self, status):
        """根据状态绘制对应的图片"""
        if status:
            self.surface.blit(self.store_light, (0, 0))
        else:
            self.surface.blit(self.store_dark, (0, 0))


class NextSign:
    """创建下一个花园的点击标志"""
    def __init__(self, setting):
        """标志基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.0505, self.setting.screen_height * 0.0842)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.49, self.setting.screen_height * 0.0117)
        self._load_next_sign_image()

    def _load_next_sign_image(self):
        """加载并设置标志"""
        image = pygame.image.load(self.setting.next_garden)
        self.sign = pygame.transform.scale(image, (self.width, self.height))
        self.surface.blit(self.sign, (0, 0))


class GardenView:
    """创建花园视图"""
    def __init__(self, ai_game):
        """初始化花园基本属性"""
        self.screen = ai_game.main_screen
        self.setting = ai_game.setting
        self.garden_index = 0
        self.areas = Group()
        self.containers = Group()
        self.tools = [Kettle(self.setting),
                      TreeFood(self.setting),
                      BugSpray(self.setting),
                      Phonograph(self.setting),
                      Glove(self.setting),
                      ZenMoney(self.setting),
                      ZenWheelBarrow(self.setting)]
        self.main_menu = MainMenu(self.setting)
        self.store = GardenStore(self.setting)
        self.next_sign = NextSign(self.setting)
        self._create_click_areas()
        self._create_tool_container()
        self.create_and_show_tools()
        self.is_enter = False
        self.is_light = False

    def _load_garden_background(self, index):
        """加载花园背景"""
        image = pygame.image.load(self.setting.garden_list[index])
        self.garden = pygame.transform.scale(image, (self.setting.screen_width, self.setting.screen_height))
        self.garden_rect = self.garden.get_rect()
        self.garden_rect.topleft = (0, 0)

    def _create_tool_container(self):
        """在屏幕上创建5个工具容纳区"""
        x, y = (self.setting.screen_width * 0.02, 0)
        for _ in range(7):
            new_container = Container(self.setting)
            new_container.reset_container_location(x, y)
            self.containers.add(new_container)
            x += self.setting.screen_width * 0.066

    def _create_click_areas(self):
        """在屏幕上创建32个可点击的区域"""
        x, y = (95, 115)
        for _ in range(8):
            new_area = Area()
            new_area.reset_area_location(x, y)
            self.areas.add(new_area)
            x += 103
        x, y = (85, 213)
        for _ in range(8):
            new_area = Area()
            new_area.reset_area_location(x, y)
            self.areas.add(new_area)
            x += 107
        x, y = (55, 307)
        for _ in range(8):
            new_area = Area()
            new_area.reset_area_location(x, y)
            self.areas.add(new_area)
            x += 115
        x, y = (45, 410)
        for _ in range(4):
            new_area = Area()
            new_area.reset_area_location(x, y)
            self.areas.add(new_area)
            x += 115
        x, y = (532, 410)
        for _ in range(4):
            new_area = Area()
            new_area.reset_area_location(x, y)
            self.areas.add(new_area)
            x += 113

    def check_is_click_main_menu(self, mouse_pos):
        """检查是否点击了主菜单"""
        if self.main_menu.rect.collidepoint(mouse_pos):
            return True
        return False

    def check_is_click_sign(self, mouse_pos):
        """检查是否点击标志"""
        if self.next_sign.rect.collidepoint(mouse_pos):
            return True
        return False

    def check_is_click_or_pass_store(self, mouse_pos):
        """检查是否点击了商店"""
        if self.store.rect.collidepoint(mouse_pos):
            self.is_light = True
            return True
        else:
            self.is_light = False
            return False

    def create_and_show_tools(self):
        """从列表中依次写入到指定的区域中"""
        for container, tool in zip(self.containers, self.tools):
            tool.set_location(container)
            self.screen.blit(tool.shape, tool.rect)

    def plot_garden_view(self):
        """在屏幕上绘制元素"""
        self._load_garden_background(self.garden_index)
        self.screen.blit(self.garden, self.garden_rect)
        self.screen.blit(self.next_sign.surface, self.next_sign.rect)
        for area in self.areas.sprites():
            self.screen.blit(area.surface, area.rect)
        for container in self.containers.sprites():
            self.screen.blit(container.container, container.rect)
        self.create_and_show_tools()
        self.screen.blit(self.main_menu.surface, self.main_menu.rect)
        self.store.plot_store(self.is_light)
        self.screen.blit(self.store.surface, self.store.rect)

    def update_next_garden(self):
        """检查是否点击了下一个花园"""
        self.garden_index = (self.garden_index+1) % len(self.setting.garden_list)
