import pygame


class EnterView:
    """进入游戏的界面"""
    def __init__(self, ai_game):
        """视图基本属性"""
        self.screen = ai_game.main_screen
        self.setting = ai_game.setting
        self.width, self.height = (self.setting.screen_width*0.4, self.setting.screen_height*0.1)
        self.text_color1 = (246, 255, 37)  # 未点击的颜色
        self.text_color2 = (75, 240, 0)  # 点击后的颜色
        self.font = pygame.font.SysFont('tahoma', int(self.setting.screen_height*0.0505))
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.setting.screen_width*0.307, self.setting.screen_height*0.886)
        self._create_inner_surface()
        self._create_font_image()
        self._load_wait_background_image()
        self._load_dirt_image()
        self.is_light = False

    def _create_font_image(self):
        """创建不同的字体颜色"""
        string = 'start game'
        self.font1 = self.font.render(string, True, self.text_color1)
        self.font2 = self.font.render(string, True, self.text_color2)
        self.font_rect = self.font2.get_rect()
        x = self.inner_surface.get_width() / 2 - self.font1.get_width() / 2
        y = self.inner_surface.get_height() / 2 - self.font1.get_height() / 2
        self.font_rect.topleft = (x, y)

    def _create_inner_surface(self):
        """创建容纳字体的surface"""
        width, height =(self.setting.screen_width * 0.156, self.setting.screen_height * 0.055)
        self.inner_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.inner_rect = self.inner_surface.get_rect()
        self.inner_rect.topleft = \
            (self.width / 2 - width / 2 - self.setting.screen_width*0.0101, self.setting.screen_height*0.015)

    def _load_wait_background_image(self):
        """等待背景图片"""
        image = pygame.image.load(self.setting.wait_background)
        self.wait = pygame.transform.scale(image, (self.setting.screen_width, self.setting.screen_height))

    def _load_dirt_image(self):
        """加载土地图片"""
        image = pygame.image.load(self.setting.soil)
        self.dirt = pygame.transform.scale(image, (self.width, self.height))
        self.surface.blit(self.dirt, (0, 0))

    def check_is_pass_start_game(self, mouse_pos):
        """根据鼠标位置判断是否进入游戏"""
        inner_mouse_pos = [(mouse_pos[0] - self.rect.x),
                           (mouse_pos[1] - self.rect.y)]
        if self.inner_rect.collidepoint(inner_mouse_pos):
            return True
        return False

    def check_is_enter_game(self, mouse_pos):
        """检测鼠标是否点击目标区域"""
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def plot_wait_background(self):
        """绘制等待背景"""
        self.screen.blit(self.wait, (0, 0))
        self.inner_surface.fill(self.setting.fill_color)
        self.inner_surface.set_colorkey(self.setting.fill_color)
        if not self.is_light:
            self.inner_surface.blit(self.font1, self.font_rect)
        else:
            self.inner_surface.blit(self.font2, self.font_rect)
        self.surface.blit(self.inner_surface, self.inner_rect)
        self.screen.blit(self.surface, self.rect)
