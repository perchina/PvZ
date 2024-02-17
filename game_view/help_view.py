import pygame


class HelpView:
    """创建一个帮助视图"""
    def __init__(self, ai_game):
        """初始化视图属性"""
        self.screen = ai_game.main_screen
        self.rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self._load_help_background_image()
        self._create_surface()
        self._load_button()
        self._load_help_content()
        self.is_enter = False
        self.is_light = False

    def _create_surface(self):
        """创建一个按钮区域"""
        size = (self.setting.screen_width*0.133, self.setting.screen_height*0.067)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        x = self.setting.screen_width / 2 - self.setting.screen_width*0.133 / 2
        y = self.setting.screen_height*0.889
        self.surface_rect.topleft = (x, y)

    def _load_button(self):
        """设置具体的按钮样式"""
        size = (self.setting.screen_width*0.133, self.setting.screen_height*0.067)
        image1 = pygame.image.load(self.setting.seed_button_light)
        image2 = pygame.image.load(self.setting.seed_button_dark)
        self.button_light = pygame.transform.scale(image1, size)
        self.button_dark = pygame.transform.scale(image2, size)
        self.button_rect = self.button_dark.get_rect()
        self.button_rect.topleft = (0, 0)

    def _load_help_background_image(self):
        """加载背景图"""
        size = (self.setting.screen_width*1.333, self.setting.screen_height*1.333)
        image = pygame.image.load(self.setting.help_background)
        self.background = pygame.transform.scale(image, size)
        self.bg_rect = self.background.get_rect()
        self.bg_rect.center = self.rect.center

    def _load_help_content(self):
        """加载内容"""
        size = (self.setting.screen_width*0.667, self.setting.screen_height*0.667)
        image = pygame.image.load(self.setting.help_content)
        self.content = pygame.transform.scale(image, size)
        self.content_rect = self.content.get_rect()
        x = self.setting.screen_width / 2 - self.setting.screen_width*0.667 / 2
        y = self.setting.screen_height*0.111
        self.content_rect.topleft = (x, y)

    def check_is_click_main_menu(self, mouse_pos):
        """检查鼠标是否点击"""
        if self.surface_rect.collidepoint(mouse_pos):
            self.is_light = True
            return True
        else:
            self.is_light = False
            return False

    def plot_help_view(self):
        """在屏幕上绘制帮助视图"""
        if not self.is_light:
            self.surface.blit(self.button_dark, self.button_rect)
        else:
            self.surface.blit(self.button_light, self.button_rect)
        self.screen.blit(self.background, self.bg_rect)
        self.screen.blit(self.content, self.content_rect)
        self.screen.blit(self.surface, self.surface_rect)



