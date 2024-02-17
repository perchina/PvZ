import time

import pygame


class PlantCard:
    """每一张植物卡片"""
    def __init__(self, surface, image_path, width, height):
        """每一张植物卡片"""
        self.screen = surface
        self.image = image_path
        self.width, self.height = (width, height)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.index = 0
        self._load_plant_card()
        self.is_click = False

    def check_is_click(self, mouse_pos):
        """检查鼠标是否点击该卡片"""
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def _load_plant_card(self):
        """加载植物卡片"""
        image = pygame.image.load(self.image)
        self.card = pygame.transform.scale(image, (self.width, self.height*2))
        self.card_rect = self.card.get_rect()

    def reset_location(self, x, y):
        """重新设置位置"""
        self.rect.topleft = (x, y)

    def plot_card(self):
        """绘制卡片"""
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        if not self.is_click:
            self.card_rect.topleft = (0, 0)
        else:
            self.card_rect.bottomleft = (0, self.height)
        self.surface.blit(self.card, self.card_rect)
        self.screen.blit(self.surface, self.rect)


class ImitatorCard:
    """模仿者卡片"""
    def __init__(self, surface, setting, width, height):
        """模仿者基本属性"""
        self.screen = surface
        self.setting = setting
        self.width, self.height = (width, height)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (690, 350)
        self.index = 0
        self._load_plant_card()
        self.is_click = False

    def check_is_click(self, mouse_pos):
        """检查鼠标是否点击该卡片"""
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def _load_plant_card(self):
        """加载植物卡片"""
        image1 = pygame.image.load(self.setting.imitator_color)
        image2 = pygame.image.load(self.setting.imitator_black)
        self.card1 = pygame.transform.scale(image1, (self.width, self.height))
        self.card2 = pygame.transform.scale(image2, (self.width, self.height))

    def plot_card(self):
        """绘制模仿者卡片"""
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        if not self.is_click:
            self.surface.blit(self.card1, (0, 0))
        else:
            self.surface.blit(self.card2, (0, 0))
        self.screen.blit(self.surface, self.rect)


class PlantsSelectBoard:
    """植物选择页面"""
    def __init__(self, ai_game):
        """创建植物选择面板"""
        self.screen = ai_game.main_screen
        self.plant_cards = ai_game.plant_cards
        self.setting = ai_game.setting
        self.width, self.height = (1000, 500)
        self.card_width, self.card_height = (100, 60)
        self.surface = pygame.Surface((self.width, self.height))
        self.surface1 = pygame.Surface((120, 40))
        self.rect = self.surface.get_rect()
        self.rect1 = self.surface1.get_rect()
        self.board_move_limit = self.setting.screen_height - self.height + 10
        self.y = float(self.rect.y)
        self.cards = []
        self.index = -1
        self.last_up_time = 0
        self._create_plant_card_list()
        self.reset_initial_location()
        self._load_plant_select_board()
        self._load_start_game_button()
        self.is_arrive_location = False
        self.is_can_click = False
        self.is_up = True
        self.is_down = False
        self.is_enter = False

    def _create_imitator_card(self):
        """创建模仿者卡片"""
        imitator = ImitatorCard(self.surface, self.setting, 120, 160)
        imitator.index = 40
        self.cards.append(imitator)

    def _create_plant_card_list(self):
        """创建植物卡片选择列表"""
        index = 0
        x_interval, y_interval = (self.card_width, self.card_height)
        x_start, y_start = (25, 35)
        x, y = (x_start, y_start)
        rows = 0
        for image_path in self.setting.plant_select_list:
            card = PlantCard(self.surface, image_path, self.card_width, self.card_height)
            card.reset_location(x, y)
            card.index = index
            self.cards.append(card)
            x += x_interval + 10
            rows += 1
            index += 1
            if rows == 6:
                x = x_start
                y += y_interval + 5
                rows = 0
        self._create_imitator_card()

    def _load_plant_select_board(self):
        """加载植物选择面板"""
        image = pygame.image.load(self.setting.plant_select_board_png)
        self.plant_board = pygame.transform.scale(image, (700, self.height))

    def _load_start_game_button(self):
        """加载开始按钮"""
        image = pygame.image.load(self.setting.start_game_button)
        self.start_button = pygame.transform.scale(image, (120, 80))
        self.rect1.topleft = (870, 450)

    def _update_board_location(self):
        """更新面板位置"""
        if self.plant_cards.is_move:
            current_time = time.time()
            if self.is_up:
                if self.rect.top >= self.board_move_limit:
                    if current_time - self.last_up_time >= 0.05:
                        self.y -= 100
                        self.rect.y = self.y
                        self.last_up_time = current_time
                else:
                    self.is_up = False
                    self.is_arrive_location = True
                    self.plant_cards.is_move = False
            elif self.is_down:
                if self.rect.top <= self.setting.screen_height:
                    if current_time - self.last_up_time >= 0.05:
                        self.y += 100
                        self.rect.y = self.y
                        self.last_up_time = current_time
                else:
                    self.is_enter = False
                    self.is_down = False
                    self.is_arrive_location = True
                    self.plant_cards.is_move = False

    def _blit_start_button(self):
        """绘制开始按钮"""
        self.surface1.fill((0, 7, 0))
        self.surface1.set_colorkey((0, 7, 0))
        if not self.is_can_click:
            self.surface1.blit(self.start_button, (0, -40))
        else:
            self.surface1.blit(self.start_button, (0, -1))
        self.surface.blit(self.surface1, self.rect1)

    def check_click(self, mouse_pos):
        """检查点击事件"""
        inner_coord = self.rect
        inner_mouse_pos = (mouse_pos[0] - inner_coord[0],
                           mouse_pos[1] - inner_coord[1])
        for card in self.cards:
            if not card.is_click:
                if card.check_is_click(inner_mouse_pos):
                    card.is_click = True
                    self.index = card.index
                    return True
        return False

    def check_is_click_start_button(self, mouse_pos):
        """检测鼠标是否点击或者经过开始按钮"""
        if len(self.plant_cards.show_plant_cards) == 10:
            self.is_can_click = True
            inner_coord = self.rect
            inner_mouse_pos = (mouse_pos[0] - inner_coord[0],
                               mouse_pos[1] - inner_coord[1])
            if self.rect1.collidepoint(inner_mouse_pos):
                return True
            else:
                return False
        else:
            self.is_can_click = False

    def recover_card_status(self, index):
        """根据索引恢复原来卡片的状态"""
        self.cards[index].is_click = False

    def reset_initial_location(self):
        """重设初始位置"""
        self.rect.top = self.screen.get_height()
        self.rect.left = 10
        self.y = float(self.rect.y)

    def show_plant_cards(self):
        """展示所有的植物卡片"""
        self.surface.fill((0, 7, 0))
        self.surface.set_colorkey((0, 7, 0))
        self.surface.blit(self.plant_board, (0, 0))
        if not self.is_arrive_location:
            self._update_board_location()
        for card in self.cards:
            card.plot_card()
        self._blit_start_button()
        self.screen.blit(self.surface, self.rect)
