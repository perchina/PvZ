import pygame
from time import time
from click_area.check_button import CheckButton
from game_stat.sunlight_stat import SunlightStat


class PCard:
    """植物卡片类"""
    def __init__(self, attribute, choose_frame):
        self.attr = attribute  # 外面传过来的是一个列表， 分别是卡片亮色， 漆黑色， 索引， 阳光耗费， 冷却时间
        self.choose_frame = choose_frame  # 选择框
        self.surface = pygame.Surface((51, 66))
        self.rect = self.surface.get_rect()
        self.list_index = 0  # 存在于列表中的索引
        self.last_rest_time = time()
        self._load_light_and_dark_card()
        self.sunlight_is_enough = False
        self.is_rest_time = False
        self.is_select_the_card = False

    def _load_light_and_dark_card(self):
        """加载高亮和漆黑的卡片"""
        self.light_card = self._load_and_set_image(self.attr[0])
        self.dark_card = self._load_and_set_image(self.attr[1])
        self.card_index = self.attr[2]
        self.sunlight_cost = self.attr[3]
        self.rest_time = self.attr[4]
        self.choose_frame = self._load_and_set_image(self.choose_frame)

    def _load_and_set_image(self, path, width=51, height=66, smooth=False):
        """加载图片并设置图片大小"""
        image = pygame.image.load(path)
        if not smooth:
            return pygame.transform.scale(image, (width, height))
        else:
            return pygame.transform.smoothscale(image, (width, height))

    def _check_card_status(self, sunlight_value):
        """根据卡片本身状态确定是否能够被点击"""
        current_time = time()
        if sunlight_value >= self.sunlight_cost:
            self.sunlight_is_enough = True
            if self.is_rest_time:
                if current_time - self.last_rest_time >= self.rest_time:
                    print(current_time)
                    self.is_rest_time = False
                    self.last_rest_time = current_time

    def set_location(self, x, y):
        """设置surface位置"""
        self.rect.topleft = (x, y)

    def blit_card(self, sunlight_value):
        self._check_card_status(sunlight_value)
        self.surface.fill((0, 225, 0))
        self.surface.set_colorkey((0, 225, 0))
        if self.sunlight_is_enough and not self.is_rest_time:  # 阳光充足并且没有进入休息时间
            self.surface.blit(self.light_card, (0, 0))
        elif not self.sunlight_is_enough or self.is_rest_time:
            self.surface.blit(self.dark_card, (0, 0))
        if self.is_select_the_card:
            self.surface.blit(self.choose_frame, (0, 0))


class PlantCards:
    """这是一个规范植物卡片在屏幕上显示位置的类"""
    def __init__(self, ai_game):
        """"植物卡片基本属性"""
        self.ai_game = ai_game
        self.screen = ai_game.main_screen
        self.setting = ai_game.setting
        self.card_width, self.card_height = (51, 66)
        self.plant_mode_list = []  # 所有的植物模型列表
        self.plant_cards = []   # 所有的植物卡片储存列表
        self.show_plant_cards = []   # 供展示和点击的植物卡片列表，长度最大为10
        self.card_length_limit = 10
        self.list_index = -1
        self.card_index = -1
        self.surface = pygame.Surface((1080, 90))
        self.rect = self.surface.get_rect()
        self.check_button = CheckButton(ai_game, self.surface, self.rect)
        self.sunlight_stat = SunlightStat(self.setting, self.surface)
        self.reset_initial_location()
        self.y = float(self.rect.y)
        self._load_sun_and_card_container()
        self._set_shovel_size_and_location()
        self._load_plant_modes()
        self._load_plant_cards()
        self._load_main_menu()
        self.is_move = False
        self.is_start_game = True
        self.shovel_active = False
        self.is_select_plant = False

    def _load_sun_and_card_container(self):
        """加载阳光和卡片容器"""
        self.sun_bank = self._load_and_set_image(self.setting.sun_bank, 88, 88, True)
        self.container = self._load_and_set_image(self.setting.container, 720, 80, True)

    def _load_main_menu(self):
        """加载主菜单"""
        image = pygame.image.load(self.setting.menu)
        self.menu = pygame.transform.scale(image, (94, 26))
        self.menu_rect = self.menu.get_rect()
        self.menu_rect.topleft = (976, 0)

    def _load_plant_modes(self):
        """将所有的植物模型加载到指定列表中"""
        for mode in self.setting.select_plant_list:
            image = mode[0]
            pygame_image = self._load_and_set_image(image, mode[1][0], mode[1][1], False)
            if mode[2] != 0:
                pygame_image = pygame.transform.rotate(pygame_image, mode[2])
            self.plant_mode_list.append(pygame_image)

    def _load_plant_cards(self):
        """加载所有的植物卡片到指定列表中"""
        for card in self.setting.card_list:
            new_card = PCard(card, self.setting.choose_frame)
            self.plant_cards.append(new_card)

    def _load_and_set_image(self, path, width=51, height=66, smooth=True):
        """"加载每一张图片然后设置其大小"""
        image = pygame.image.load(path)
        if smooth:
            return pygame.transform.smoothscale(image, (width, height))
        else:
            return pygame.transform.scale(image, (width, height))

    def _set_shovel_size_and_location(self):
        """"设置铲子属性"""
        image1 = pygame.image.load(self.setting.shovel)
        image2 = pygame.image.load(self.setting.shovel_bank)
        self.shovel_original_coordinate = (723, 0)
        self.surface1 = pygame.Surface((72, 66))
        self.rect1 = self.surface1.get_rect()
        self.rect1.topleft = self.shovel_original_coordinate
        self.shovel = pygame.transform.smoothscale(image1, (72, 66))
        self.shovel_bank = pygame.transform.smoothscale(image2, (72, 66))
        self.shovel_rect = self.shovel.get_rect()

    def _update_location(self):
        """更新容器位置"""
        if self.is_move:
            if self.rect.y < 0:
                self.y += 10
                self.rect.y = self.y

    def _check_screen_move_status(self):
        """检查屏幕的状态并设置相应移动属性"""
        if not self.check_button.is_select_start and not self.check_button.is_move:  # 进入到游戏局内同时正要选择植物
            self.is_move = True

    def add_card_to_list(self, index):
        """将特定的卡片加入待展示的列表中"""
        list_len = len(self.show_plant_cards)
        self.plant_cards[index].list_index = list_len
        self.show_plant_cards.append(self.plant_cards[index])

    def check_is_can_click_plant_card(self, mouse_pos):
        """检测是否能够点击植物卡片"""
        count_select_card = 0
        count_cancel_select_card = 0
        for card in self.show_plant_cards:
            if card.rect.collidepoint(mouse_pos):
                if card.sunlight_is_enough and not card.is_rest_time:
                    if not card.is_select_the_card:
                        self.is_select_plant = True
                        card.is_select_the_card = True
                        self.card_index = card.card_index
                        self.list_index = card.list_index
                        count_select_card += 1
                    else:
                        self.is_select_plant = False
                        card.is_select_the_card = False
                        self.card_index = -1
                        count_cancel_select_card += 1
            else:
                card.is_select_the_card = False
        if count_select_card > 0:
            return 1
        elif count_cancel_select_card > 0:
            return 2
        else:
            self.is_select_plant = False
            self.show_plant_cards[self.list_index].is_select_the_card = False
            self.card_index = -1
            return False

    def check_is_remove_card(self, mouse_pos):
        """检查卡片是否被返回"""
        for index in range(0, len(self.show_plant_cards)):
            if self.show_plant_cards[index].rect.collidepoint(mouse_pos):
                self.card_index = self.show_plant_cards[index].card_index
                self.show_plant_cards.pop(index)
                return True
        return False

    def check_is_click_main_menu(self, mouse_pos):
        """检查是否点击主菜单"""
        inner_coord = self.rect
        inner_mouse_pos = (mouse_pos[0] - inner_coord[0],
                           mouse_pos[1] - inner_coord[1])
        if self.menu_rect.collidepoint(inner_mouse_pos):
            return True
        return False

    def check_is_click_shovel(self, mouse_pos):
        """检查是否点击铲子"""
        inner_coord = self.rect
        inner_mouse_pos = (mouse_pos[0] - inner_coord[0],
                           mouse_pos[1] - inner_coord[1])
        if self.rect1.collidepoint(inner_mouse_pos):
            return True
        return False

    def reset_initial_location(self):
        """初始化卡片位置"""
        self.rect.bottomleft = (0, 0)

    def _blit_plant_card(self):
        """绘制待展示的植物卡片"""
        x, y = (97, 7)
        for card in self.show_plant_cards:
            card.blit_card(self.sunlight_stat.sunlight)
            card.set_location(x, y)
            self.screen.blit(card.surface, card.rect)
            x += card.surface.get_width() + 11.5

    def _blit_plant_mode(self):
        """根据植物索引和鼠标位置在屏幕上响应的位置绘制植物模型"""
        if self.is_select_plant and self.card_index != -1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] >= 80:
                mode_rect = self.plant_mode_list[self.card_index].get_rect()
                mode_rect.center = mouse_pos
                self.screen.blit(self.plant_mode_list[self.card_index], mode_rect)

    def _blit_shovel(self):
        """绘制铲子"""
        if self.is_start_game:
            self.surface1.fill((0, 0, 0))
            self.surface1.set_colorkey((0, 0, 0))
            self.surface1.blit(self.shovel_bank, (0, 0))
            if self.shovel_active:
                mouse = pygame.mouse.get_pos()
                self.shovel_rect.bottomleft = mouse
                self.surface.blit(self.surface1, self.rect1)
                self.screen.blit(self.surface, self.rect)
                self.screen.blit(self.shovel, self.shovel_rect)
            else:
                self.surface1.blit(self.shovel, (0, 0))
                self.surface.blit(self.surface1, self.rect1)
                self.screen.blit(self.surface, self.rect)

    def _blit_card_container_and_sunbank(self):
        """绘制阳光银行和卡片容器"""
        self.surface.blit(self.container, (0, 0))
        self.surface.blit(self.sun_bank, (0, 0))

    def _blit_check_button(self, pause):
        self.check_button.plot_check_button(pause)

    def _blit_menu_button(self):
        """绘制主菜单"""
        if not self.ai_game.is_pause:
            self.surface.blit(self.menu, self.menu_rect)

    def blit_all(self, pause):
        """绘制植物卡片，阳光，铲子， 和视图, 开始按钮"""
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        self.check_button.update_surface_location()
        self.check_button.update_inner_surface_location()
        self._check_screen_move_status()
        self._update_location()
        self._blit_card_container_and_sunbank()
        self.sunlight_stat.plot_sunlight_value()
        self._blit_check_button(pause)
        self._blit_menu_button()
        self._blit_shovel()
        self._blit_plant_card()
        self._blit_plant_mode()
