import pygame


class SunlightStat:
    """"这是一个阳光统计类"""
    def __init__(self, setting, surface):
        """"初始化阳光基本属性"""
        self.screen = surface
        self.setting = setting
        self.text_color = self.setting.fill_color
        self.font = pygame.font.SysFont('tahoma', int(self.setting.screen_height * 0.022))
        self.sunlight = self.setting.start_sunlight
        self.width, self.height = (self.setting.screen_width * 0.0613, self.setting.screen_height * 0.033)
        self.surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.sunlight_image = None
        self.sunlight_rect = None
        self.prep_sunlight_value()

    def prep_sunlight_value(self, sunlight=0):
        """每一次更新屏幕上的阳光值"""
        self.sunlight += sunlight
        sunlight_str = str(self.sunlight)
        self.sunlight_image = self.font.render(sunlight_str, True, self.text_color)
        self.sunlight_rect = self.sunlight_image.get_rect()
        x = self.width / 2 - self.sunlight_image.get_width() / 2
        y = self.height / 2 - self.sunlight_image.get_height() / 2
        self.sunlight_rect.topleft = (x, y)

    def plot_sunlight_value(self):
        """绘制实时阳光"""
        self.surface.fill((255, 255, 255))
        self.surface.set_colorkey((255, 255, 255))
        self.surface.blit(self.sunlight_image, self.sunlight_rect)
        self.screen.blit(self.surface, (11, 65))

