import pygame


class OptionFont:
    """选项字体"""
    def __init__(self, setting):
        """字体基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.172, self.setting.screen_height * 0.269)
        self.text_color = (108, 108, 145)
        self.font_size = int(self.setting.screen_height * 0.0421)
        self.font = pygame.font.SysFont('tahoma', self.font_size)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface. get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.091, self.setting.screen_height * 0.219)
        self.font_list = []
        self.font_rect_list = []
        self._create_option_font()
        self._arrange_font()

    def _create_option_font(self):
        """创建各种选项字体"""
        str1 = 'Music'
        str2 = 'Sound'
        str3 = '3D Speed Plus'
        str4 = 'Whole Screen'
        self.font1 = self.font.render(str1, True, self.text_color)
        self.font2 = self.font.render(str2, True, self.text_color)
        self.font3 = self.font.render(str3, True, self.text_color)
        self.font4 = self.font.render(str4, True, self.text_color)
        self.rect1 = self.font1.get_rect()
        self.rect2 = self.font2.get_rect()
        self.rect3 = self.font3.get_rect()
        self.rect4 = self.font4.get_rect()
        self.font_list = [self.font1, self.font2, self.font3, self.font4]
        self.font_rect_list = [self.rect1, self.rect2, self.rect3, self.rect4]

    def _arrange_font(self):
        """将字体整齐排列"""
        x, y = (0, 0)
        for font, rect in zip(self.font_list, self.font_rect_list):
            rect.topleft = (x, y)
            self.surface.blit(font, rect)
            y += self.font_size + self.setting.screen_height * 0.0168


class MainButton:
    """确定按钮"""
    def __init__(self, setting):
        """创建确定按钮基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.384, self.setting.screen_height * 0.152)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width * 0.0404, self.setting.screen_height * 0.673)
        self._load_sure_button_image()
        self.is_press = False

    def _load_sure_button_image(self):
        """加载并设置确定按钮"""
        # 主菜单按钮
        image1 = pygame.image.load(self.setting.main_menu_back)
        self.main_button = pygame.transform.scale(image1, (self.width, self.height * 2))
        self.main_button_rect = self.main_button.get_rect()
        # 返回游戏按钮
        image2 = pygame.image.load(self.setting.game_view_back)
        self.game_view_button = pygame.transform.scale(image2, (self.width, self.height * 2))
        self.game_view_button_rect = self.game_view_button.get_rect()

    def plot_sure_button(self, is_start_game):
        """在操作台绘制确定按钮"""
        if not is_start_game:  # 游戏还没有开始,停留在主页
            if not self.is_press:
                self.main_button_rect.topleft = (0, 0)
            else:
                self.main_button_rect.bottomleft = (0, self.height)
            self.surface.blit(self.main_button, self.main_button_rect)
        else:  # 游戏已经开始
            if not self.is_press:
                self.game_view_button_rect.topleft = (0, 0)
            else:
                self.game_view_button_rect.bottomleft = (0, self.height)
            self.surface.blit(self.game_view_button, self.game_view_button_rect)


class SmallButton:
    """小按钮"""
    def __init__(self, setting, x, y):
        """小按钮基本属性"""
        self.setting = setting
        self.width, self.height = (160, 40)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.x = x / 2 - self.width / 2
        self.rect.topleft = (self.x, y)
        self._load_small_button()

    def _load_small_button(self):
        """加载小按钮"""
        # 制作者名单
        image1 = pygame.image.load(self.setting.maker_list_button)
        self.maker_button = pygame.transform.scale(image1, (self.width, self.height))
        self.maker_button_rect = self.maker_button.get_rect()
        # 主菜单按钮
        image2 = pygame.image.load(self.setting.goto_main_menu)
        self.main_menu_button = pygame.transform.scale(image2, (self.width, self.height))
        self.main_menu_button_rect = self.main_menu_button.get_rect()

    def plot_small_button(self, is_start_game):
        """根据游戏状态绘制不同的按钮"""
        if not is_start_game:  # 停留在主页，游戏未开始
            self.surface.blit(self.maker_button, self.maker_button_rect)
        else:  # 游戏已经开始
            self.surface.blit(self.main_menu_button, self.main_menu_button_rect)


class CheckBox:
    """复选框"""
    def __init__(self, setting, x, y):
        """复选框基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.0303, self.setting.screen_width * 0.0303)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_check_box_image()
        self.is_select = False

    def _load_check_box_image(self):
        """复选框的不同状态"""
        image1 = pygame.image.load(self.setting.option_checkbox0)
        image2 = pygame.image.load(self.setting.option_checkbox1)
        self.select = pygame.transform.smoothscale(image1, (self.width, self.height))
        self.selected = pygame.transform.smoothscale(image2, (self.width, self.height))

    def plot_check_box(self):
        """绘制复选框"""
        self.surface.fill(self.setting.fill_color)
        self.surface.set_colorkey(self.setting.fill_color)
        if not self.is_select:
            self.surface.blit(self.select, (0, 0))
        else:
            self.surface.blit(self.selected, (0, 0))


class ProgressBar:
    """进度条"""
    def __init__(self, setting):
        """进度条基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.152, self.setting.screen_height * 0.0842)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._load_progress_bar_image()

    def _load_progress_bar_image(self):
        """加载进度条"""
        image1 = pygame.image.load(self.setting.option_sliderslot)
        image2 = pygame.image.load(self.setting.option_sliderslot)
        self.progress1 = pygame.transform.scale(image1, (self.width, self.setting.screen_height * 0.0168))
        self.progress2 = pygame.transform.scale(image2, (self.width, self.setting.screen_height * 0.0168))
        self.surface.blit(self.progress1, (0, 0))
        self.surface.blit(self.progress2, (0, self.height - self.setting.screen_height * 0.0168))


class Slider:
    """滑块类"""
    def __init__(self, setting, x, y):
        """滑块基本属性"""
        self.setting = setting
        self.width, self.height = (self.setting.screen_width * 0.162, self.setting.screen_height * 0.0505)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self._load_slider_image()

    def _load_slider_image(self):
        """滑块图片"""
        image = pygame.image.load(self.setting.option_sliderknob2)
        self.slider = pygame.transform.scale(image, (self.setting.screen_width * 0.0202, self.height))
        self.slider_rect = self.slider.get_rect()
        self.slider_rect.topleft = (self.setting.screen_width * 0.1414, 0)
        self.surface.blit(self.slider, self.slider_rect)

    def clear_image_in_surface(self):
        """清空surface内部的所有图像"""
        self.surface.fill(self.setting.fill_color)
        self.surface.set_colorkey(self.setting.fill_color)

    def reset_slider_rect(self, x):
        """根据获取到的x重新设置滑块的位置"""
        self.clear_image_in_surface()
        self.slider_rect.topleft = (x, 0)
        self.surface.blit(self.slider, self.slider_rect)


class OptionView:
    """设置视图"""
    def __init__(self, ai_game):
        """设置面板基本属性"""
        self.ai_game = ai_game
        self.screen = ai_game.main_screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.music = ai_game.music  # 主程序的音乐模块
        self.width, self.height = (self.setting.screen_width * 0.455, self.setting.screen_height * 0.842)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.center = self.screen_rect.center
        self._load_set_board_image()

        self.main_button = MainButton(self.setting)
        self.small_button = SmallButton(self.setting, self.width, 330)
        self.option = OptionFont(self.setting)
        self.check_box1 = CheckBox(self.setting, self.setting.screen_width * 0.323, self.setting.screen_height * 0.345)
        self.check_box2 = CheckBox(self.setting, self.setting.screen_width * 0.323, self.setting.screen_height * 0.404)
        self.slider1 = Slider(self.setting, self.setting.screen_width * 0.212, self.setting.screen_height * 0.219)
        self.slider2 = Slider(self.setting, self.setting.screen_width * 0.212, self.setting.screen_height * 0.286)
        self.progress = ProgressBar(self.setting)
        self.is_enter = False
        self.is_start_game = False

    def _load_set_board_image(self):
        """加载面板图片"""
        image = pygame.image.load(self.setting.set_board)
        self.board = pygame.transform.smoothscale(image, (self.width, self.height))

    def _check_game_status(self):
        """检查游戏状态"""
        if self.ai_game.is_start_select or self.ai_game.is_start_game:
            self.is_start_game = True
        else:
            self.is_start_game = False

    def _check_is_click_check_box1(self, mouse_pos):
        """检测是否点击了复选框"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.check_box1.rect.collidepoint(mouse_pos):
            return True
        return False

    def _check_is_click_check_box2(self, mouse_pos):
        """检测是否点击了复选框"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.check_box2.rect.collidepoint(mouse_pos):
            return True
        return False

    def check_is_click_main_button(self, mouse_pos):
        """检测是否点击到了主按钮"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.main_button.rect.collidepoint(mouse_pos):
            return True
        return False

    def _check_is_click_small_button(self, mouse_pos):
        """检测是否点击到了小的按钮"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.small_button.rect.collidepoint(mouse_pos):
            return True
        return False

    def _check_is_click_slider1(self, mouse_pos):
        """检测是否点击了内部滑块"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.slider1.rect.collidepoint(mouse_pos):
            if ((mouse_pos[0] >= self.slider1.rect.x) and
                    (mouse_pos[0] <= self.setting.screen_width * 0.354)):
                x = mouse_pos[0] - self.slider1.rect.x
                self.slider1.reset_slider_rect(x)
                scale = round(x / (self.setting.screen_width * 0.141), 2)
                self.music.adjust_music_high_or_low(scale)
                return True
        return False

    def _check_is_click_slider2(self, mouse_pos):
        """检测是否点击了内部滑块"""
        mouse_pos = self._get_real_mouse_pos(mouse_pos)
        if self.slider2.rect.collidepoint(mouse_pos):
            if ((mouse_pos[0] >= self.slider2.rect.x) and
                    (mouse_pos[0] <= self.setting.screen_width * 0.354)):
                x = mouse_pos[0] - self.slider2.rect.x
                self.slider2.reset_slider_rect(x)
                scale = round(x / (self.setting.screen_width * 0.141), 2)
                self.music.sound_scale = scale
                return True
        return False

    def _get_real_mouse_pos(self, mouse_pos):
        """得到真实的坐标"""
        inner_pos = self.rect
        mouse_pos = (mouse_pos[0] - inner_pos[0],
                     mouse_pos[1] - inner_pos[1])
        return mouse_pos

    def check_mouse_click_event(self, mouse_pos):
        """鼠标按下事件"""
        if self.check_is_click_main_button(mouse_pos):  # 点击主按钮
            self.main_button.is_press = True  # 将确定按钮设置为按下状态
        elif self._check_is_click_small_button(mouse_pos):
            if not self.is_start_game:
                pass
            else:
                self.is_enter = False
                self.ai_game.is_enter = True
                self.ai_game.is_in_home_page = True
                self.ai_game.is_start_select = False
                self.ai_game.is_start_game = False
                self.ai_game.music_start_time = 0
                self.ai_game.plant_cards.check_button.initial_attribute()
                self.ai_game.rect.topleft = self.setting.inner_screen_coordinate
        elif self._check_is_click_check_box1(mouse_pos):  # 点击了复选框1
            self.check_box1.is_select = not self.check_box1.is_select
            self.music.play_short_time_sound(self.setting.button_click)
        elif self._check_is_click_check_box2(mouse_pos):  # 点击了复选框2
            self.check_box2.is_select = not self.check_box2.is_select
            self.music.play_short_time_sound(self.setting.button_click)
        elif self._check_is_click_slider1(mouse_pos):   # 点击了滑块1
            pass
        elif self._check_is_click_slider2(mouse_pos):  # 点击了滑块2
            pass

    def check_mouse_choose_event(self, mouse_pos):
        """检测鼠标松开事件"""
        if self.check_is_click_main_button(mouse_pos):  # 松开主按钮
            if not self.is_start_game:
                self.is_enter = False
                self.main_button.is_press = False  # 将确定按钮设置为按下状态
                self.ai_game.is_draw_in_home_page = False
            else:
                self.is_enter = False
                self.main_button.is_press = False
                self.ai_game.is_pause = False
            self.music.play_short_time_sound(self.setting.button_click)
            self.music.unpause_play_music()

    def plot_set_board(self):
        """在主屏幕上绘制设置面板"""
        self._check_game_status()
        # 绘制面板
        self.surface.blit(self.board, (0, 0))
        # 绘制小按钮
        self.small_button.plot_small_button(self.is_start_game)
        self.surface.blit(self.small_button.surface, self.small_button.rect)
        # 绘制大按钮
        self.main_button.plot_sure_button(self.is_start_game)
        self.surface.blit(self.main_button.surface, self.main_button.rect)
        # 绘制文字
        self.surface.blit(self.option.surface, self.option.rect)
        # 绘制进度条
        self.surface.blit(self.progress.surface,
                          (self.setting.screen_width * 0.212, self.setting.screen_height * 0.236))
        # 绘制滑块
        self.surface.blit(self.slider1.surface, self.slider1.rect)
        self.surface.blit(self.slider2.surface, self.slider2.rect)
        # 绘制复选框
        self.check_box1.plot_check_box()
        self.check_box2.plot_check_box()
        self.surface.blit(self.check_box1.surface, self.check_box1.rect)
        self.surface.blit(self.check_box2.surface, self.check_box2.rect)
        # 将整个surface绘制到主屏幕
        self.screen.blit(self.surface, self.rect)
