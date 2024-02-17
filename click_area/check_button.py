import pygame


class LeftEye:
    """眼睛往左看"""
    def __init__(self, setting, x, y):
        """左眼基本属性"""
        self.setting = setting
        self.width, self.height = (30, 30)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_left_eye()
        self.is_active = False

    def _load_left_eye(self):
        """加载左眼"""
        image = pygame.image.load(self.setting.left_eye)
        self.left_eye = pygame.transform.smoothscale(image, (self.width, self.height))
        self.left_eye_rect = self.left_eye.get_rect()
        self.left_eye_rect.topleft = (0, 0)

    def plot_small_button(self, pause):
        """根据游戏状态确定是否绘制按钮"""
        if not pause:
            self.surface.blit(self.left_eye, self.left_eye_rect)


class RightEye:
    """眼睛往右看"""
    def __init__(self, setting, x, y):
        """右眼基本属性"""
        self.setting = setting
        self.width, self.height = (30, 30)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_right_eye()
        self.is_active = False

    def _load_right_eye(self):
        """加载左眼"""
        image = pygame.image.load(self.setting.right_eye)
        self.right_eye = pygame.transform.smoothscale(image, (self.width, self.height))
        self.right_eye_rect = self.right_eye.get_rect()
        self.right_eye_rect.topleft = (0, 0)

    def plot_small_button(self, pause):
        """根据游戏状态确定是否绘制按钮"""
        if not pause:
            self.surface.blit(self.right_eye, self.right_eye_rect)


class StopButton:
    """视图停止按钮"""
    def __init__(self, setting, x, y):
        """按钮基本属性"""
        self.setting = setting
        self.width, self.height = (30, 30)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_stop_button()
        self.is_active = False

    def _load_stop_button(self):
        """加载左眼"""
        image = pygame.image.load(self.setting.stop_the_location)
        self.stop_button = pygame.transform.smoothscale(image, (self.width, self.height))
        self.stop_button_rect = self.stop_button.get_rect()
        self.stop_button_rect.topleft = (0, 0)

    def plot_small_button(self, pause):
        """根据游戏状态确定是否绘制按钮"""
        if not pause:
            self.surface.blit(self.stop_button, self.stop_button_rect)


class ResetButton:
    """眼睛往左看"""
    def __init__(self, setting, x, y):
        """左眼基本属性"""
        self.setting = setting
        self.width, self.height = (30, 30)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_reset_button()
        self.is_active = False

    def _load_reset_button(self):
        """加载左眼"""
        image = pygame.image.load(self.setting.reset_map_location)
        self.reset_button = pygame.transform.smoothscale(image, (self.width, self.height))
        self.reset_button_rect = self.reset_button.get_rect()
        self.reset_button_rect.topleft = (0, 0)

    def plot_small_button(self, pause):
        """根据游戏状态确定是否绘制按钮"""
        if not pause:
            self.surface.blit(self.reset_button, self.reset_button_rect)


class CheckButton:
    """创建视图按钮"""
    def __init__(self, ai_game, surface, rect):
        """按钮基本属性"""
        self.ai_game = ai_game
        self.screen = surface
        self.screen_rect = rect
        self.setting = ai_game.setting
        self.left_limit, self.right_limit = (0, -self.setting.screen_width * 0.6)
        self.inner_rect = ai_game.rect
        self.x = float(self.inner_rect.x)
        self.left_eye = LeftEye(self.setting, 835, 45)
        self.right_eye = RightEye(self.setting, 915, 45)
        self.stop_button = StopButton(self.setting, 875, 5)
        self.reset_button = ResetButton(self.setting, 875, 45)
        self.button_list = [self.stop_button, self.left_eye, self.reset_button, self.right_eye]
        self.button_status = [0, 0, 0, 0]
        self.is_to_left = True
        self.is_to_right = False
        self.is_to_center = False
        self.is_select_start = True
        self.is_select_end = False
        self.is_move = True
        self.is_arrive_location = False

    def check_which_button_is_clicked(self, mouse_pos):
        """检查哪一个按钮被点击"""
        rect_pos = self.screen_rect
        inner_mouse_pos = (mouse_pos[0] - rect_pos[0],
                           mouse_pos[1] - rect_pos[1])
        for index in range(0, len(self.button_list)):
            if self.button_list[index].rect.collidepoint(inner_mouse_pos):
                self.button_status[index] = 1
            else:
                self.button_status[index] = 0

    def initial_attribute(self):
        """初始化基本属性"""
        self.is_to_left = True
        self.is_to_right = False
        self.is_to_center = False
        self.is_select_start = True
        self.is_select_end = False
        self.is_move = True
        self.is_arrive_location = False

    def update_surface_location(self):
        """根据按钮状态更新游戏内部surface的位置"""
        if self.button_status[0] == 1:  # 点击了暂停按钮
            self.button_status[0:3] = [0, 0, 0, 0]
            self.x = float(self.inner_rect.topleft[0])
        elif self.button_status[1] == 1:  # 如果点击了左眼就向左边移动
            if self.x < self.left_limit:
                self.x += self.setting.inner_screen_speed
                self.inner_rect.x = self.x
            else:
                self.button_status[1] = 0
        elif self.button_status[2] == 1:  # 点击了还原按钮
            self.inner_rect.topleft = self.setting.inner_screen_coordinate
            self.x = float(self.inner_rect.topleft[0])
            self.button_status[2] = 0
        elif self.button_status[3] == 1:  # 如果点击了右眼就向右边移动
            if self.x > self.right_limit:
                self.x -= self.setting.inner_screen_speed
                self.inner_rect.x = self.x
            else:
                self.button_status[3] = 0

    def update_inner_surface_location(self):
        """更新内部屏幕位置，实现一次动画滚动"""
        if self.is_move and not self.ai_game.is_pause:
            if self.is_select_start and not self.is_select_end:  # 刚开始选择植物
                if self.is_to_left:
                    if self.x < self.left_limit:
                        self.x += 6
                        self.inner_rect.x = self.x
                    else:
                        self.is_to_left = False
                        self.is_to_right = True
                elif self.is_to_right:
                    if self.x > self.right_limit:
                        self.x -= 6
                        self.inner_rect.x = self.x
                    else:
                        self.is_to_right = False
                        self.is_to_center = True
                        self.is_select_start = False
                        self.is_move = False
            elif not self.is_select_start and self.is_select_end:  # 植物选择已经结束
                if self.is_to_center:
                    if self.x <= self.setting.inner_screen_coordinate[0]:
                        self.x += 6
                        self.inner_rect.x = self.x
                    else:
                        self.is_to_center = False
                        self.is_move = False
                        self.is_select_end = False
                        self.is_arrive_location = True

    def plot_check_button(self, pause):
        """在对应屏幕上绘制查看按钮"""
        self.left_eye.plot_small_button(pause)
        self.screen.blit(self.left_eye.surface, self.left_eye.rect)

        self.right_eye.plot_small_button(pause)
        self.screen.blit(self.right_eye.surface, self.right_eye.rect)

        self.reset_button.plot_small_button(pause)
        self.screen.blit(self.reset_button.surface, self.reset_button.rect)

        self.stop_button.plot_small_button(pause)
        self.screen.blit(self.stop_button.surface, self.stop_button.rect)
