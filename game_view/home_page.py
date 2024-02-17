import pygame


class HomePage:
    """游戏主页面"""
    def __init__(self, ai_game):
        """建立主页面"""
        self.music = ai_game.music
        self.screen = ai_game.main_screen
        self.setting = ai_game.setting
        self._load_home_page_image()
        self._load_mode_1_image()
        self._load_mode_2_image()
        self._load_mode_3_image()
        self._load_mode_4_image()
        self._load_option_image()
        self._load_help_image()
        self._load_quit_image()
        self._load_garden_image()
        self._load_almanac_image()
        self._load_store_image()
        self._load_user_image()
        self._load_save_files_image()
        self._load_sunflower_gold_trophy()
        self.model_rect_lists = [self.mode1_rect, self.mode2_rect, self.mode3_rect, self.mode4_rect]
        self.model_index = -1
        self.character_lists = [self.surface5, self.surface6, self.surface7]
        self.character_index = -1
        self.light_images = [self.garden_light, self.almanac_light, self.store_light, self.save_light]
        self.dark_images = [self.garden_dark, self.almanac_dark, self.store_dark, self.save_dark]
        self.view_rect_lists = [self.garden_rect, self.almanac_rect, self.store_rect, self.save_rect]
        self.view_surface_lists = [self.surface8, self.surface9, self.surface10, self.surface12]
        self.view_index = -1
        self.last_index_value = -1  # 上一次的索引值
        self.mouse_is_stay = False  # 默认鼠标没有一直停留在一片区域

    def _load_home_page_image(self):
        """加载并设置游戏主页"""
        image = pygame.image.load(self.setting.home_page)
        self.home_page = pygame.transform.smoothscale(image, (self.setting.screen_width, self.setting.screen_height))

    def _load_mode_1_image(self):
        """加载模式1"""
        width, height = (self.setting.screen_width*0.41, self.setting.screen_height*0.2)
        image1 = pygame.image.load(self.setting.mode_1)
        self.surface1 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mode1 = pygame.transform.scale(image1, (width, height*2))
        self.mode1_rect = self.mode1.get_rect()
        self.rect1 = self.surface1.get_rect()
        self.rect1.topleft = (self.setting.screen_width*0.51, self.setting.screen_height*0.1)
        self.mode1_rect.topleft = (0, 0)
        # self.surface1.fill((255, 255, 255))

    def _load_mode_2_image(self):
        """加载模式2"""
        width, height = (self.setting.screen_width*0.39, self.setting.screen_height*0.2)
        image = pygame.image.load(self.setting.mode_2)
        self.surface2 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mode2 = pygame.transform.scale(image, (width, height*2))
        self.mode2_rect = self.mode2.get_rect()
        self.rect2 = self.surface2.get_rect()
        self.rect2.topleft = (self.setting.screen_width*0.51, self.setting.screen_height*0.26)
        self.mode2_rect.topleft = (0, 0)
        # self.surface2.fill((255, 255, 255))

    def _load_mode_3_image(self):
        """加载模式3"""
        width, height = (self.setting.screen_width*0.35, self.setting.screen_height*0.2)
        image = pygame.image.load(self.setting.mode_3)
        self.surface3 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mode3 = pygame.transform.scale(image, (width, height*2))
        self.mode3_rect = self.mode3.get_rect()
        self.rect3 = self.surface3.get_rect()
        self.rect3.topleft = (self.setting.screen_width*0.52, self.setting.screen_height*0.4)
        self.mode3_rect.topleft = (0, 0)
        # self.surface3.fill((255, 255, 255))

    def _load_mode_4_image(self):
        """加载模式4"""
        width, height = (self.setting.screen_width*0.32, self.setting.screen_height*0.2)
        image = pygame.image.load(self.setting.mode_4)
        self.surface4 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mode4 = pygame.transform.scale(image, (width, height*2))
        self.mode4_rect = self.mode4.get_rect()
        self.rect4 = self.surface4.get_rect()
        self.rect4.topleft = (self.setting.screen_width*0.525, self.setting.screen_height*0.54)
        self.mode4_rect.topleft = (0, 0)
        # self.surface4.fill((255, 255, 255))

    def _load_option_image(self):
        """创建选项区域"""
        width, height = (self.setting.screen_width*0.105, self.setting.screen_height*0.047)
        image = pygame.image.load(self.setting.option_light)
        self.surface5 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.option = pygame.transform.scale(image, (width, height))
        self.rect5 = self.surface5.get_rect()
        self.option_rect = self.option.get_rect()
        self.rect5.topleft = (self.setting.screen_width*0.707, self.setting.screen_height*0.819)
        self.option_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_help_image(self):
        """创建帮助区域"""
        width, height = (self.setting.screen_width * 0.06, self.setting.screen_height * 0.038)
        image = pygame.image.load(self.setting.help_light)
        self.surface6 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.help = pygame.transform.scale(image, (width, height))
        self.rect6 = self.surface6.get_rect()
        self.help_rect = self.help.get_rect()
        self.rect6.topleft = (self.setting.screen_width * 0.81, self.setting.screen_height * 0.88)
        self.help_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_quit_image(self):
        """创建退出区域"""
        width, height = (self.setting.screen_width * 0.0587, self.setting.screen_height * 0.04)
        image = pygame.image.load(self.setting.quit_light)
        self.surface7 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.quit = pygame.transform.scale(image, (width, height))
        self.rect7 = self.surface7.get_rect()
        self.quit_rect = self.quit.get_rect()
        self.rect7.topleft = (self.setting.screen_width * 0.901, self.setting.screen_height * 0.862)
        self.quit_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_garden_image(self):
        """创建花园区域"""
        width, height = (self.setting.screen_width * 0.233, self.setting.screen_height * 0.311)
        image1 = pygame.image.load(self.setting.garden_dark)
        image2 = pygame.image.load(self.setting.garden_light)
        self.surface8 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.garden_dark = pygame.transform.scale(image1, (width, height))
        self.garden_light = pygame.transform.scale(image2, (width, height))
        self.rect8 = self.surface8.get_rect()
        self.garden_rect = self.garden_dark.get_rect()
        self.rect8.topleft = (self.setting.screen_width * 0.207, self.setting.screen_height * 0.622)
        self.garden_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_almanac_image(self):
        """创建图鉴区域"""
        width, height = (self.setting.screen_width * 0.1, self.setting.screen_height * 0.167)
        image1 = pygame.image.load(self.setting.almanac_dark)
        image2 = pygame.image.load(self.setting.almanac_light)
        self.surface9 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.almanac_dark = pygame.transform.scale(image1, (width, height))
        self.almanac_light = pygame.transform.scale(image2, (width, height))
        self.rect9 = self.surface9.get_rect()
        self.almanac_rect = self.almanac_dark.get_rect()
        self.rect9.topleft = (self.setting.screen_width * 0.407, self.setting.screen_height * 0.711)
        self.almanac_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_store_image(self):
        """创建商店区域"""
        width, height = (self.setting.screen_width * 0.147, self.setting.screen_height * 0.156)
        image1 = pygame.image.load(self.setting.store_dark)
        image2 = pygame.image.load(self.setting.store_light)
        self.surface10 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.store_dark = pygame.transform.scale(image1, (width, height))
        self.store_light = pygame.transform.scale(image2, (width, height))
        self.rect10 = self.surface10.get_rect()
        self.store_rect = self.store_dark.get_rect()
        self.rect10.topleft = (self.setting.screen_width * 0.501, self.setting.screen_height * 0.79)
        self.store_rect.topleft = (0, 0)
        # self.surface5.fill((255, 255, 255))

    def _load_user_image(self):
        """创建用户区域"""
        width, height = (self.setting.screen_width * 0.333, self.setting.screen_height * 0.256)
        image = pygame.image.load(self.setting.register_board)
        self.surface11 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.user = pygame.transform.scale(image, (width, height))
        self.rect11 = self.surface11.get_rect()
        self.user_rect = self.user.get_rect()
        self.rect11.topleft = (self.setting.screen_width * 0.027, 0)
        self.user_rect.topleft = (0, 0)
        # self.surface11.fill((255, 255, 255))

    def _load_save_files_image(self):
        """创建存档区域"""
        width, height = (self.setting.screen_width * 0.333, self.setting.screen_height * 0.133)
        image1 = pygame.image.load(self.setting.save_board_dark)
        image2 = pygame.image.load(self.setting.save_board_light)
        self.surface12 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.save_dark = pygame.transform.scale(image1, (width, height))
        self.save_light = pygame.transform.scale(image2, (width, height))
        self.rect12 = self.surface12.get_rect()
        self.save_rect = self.save_dark.get_rect()
        self.rect12.topleft = (self.setting.screen_width * 0.03, self.setting.screen_height * 0.233)
        self.save_rect.topleft = (0, 0)
        # self.surface12.fill((255, 255, 255))

    def _load_sunflower_gold_trophy(self):
        """加载太阳花杯"""
        width, height = (self.setting.screen_width * 0.162, self.setting.screen_height * 0.455)
        image = pygame.image.load(self.setting.sunflower_trophy)
        self.surface13 = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect13 = self.surface13.get_rect()
        self.rect13.topleft = (self.setting.screen_width * 0.015, self.setting.screen_height * 0.505)
        self.sunflower_trophy = pygame.transform.scale(image, (width*2, height))
        self.surface13.blit(self.sunflower_trophy, (0, 0))

    def _change_model_brightness(self, index):
        """实时更新模式区域颜色"""
        self.model_index = index - 1
        self.model_rect_lists[self.model_index].bottomleft = (0, self.setting.screen_height*0.2)
        for model_rect in self.model_rect_lists:
            if model_rect != self.model_rect_lists[self.model_index]:
                model_rect.topleft = (0, 0)

    def _change_character_brightness(self, index):
        """对鼠标经过的字符区域高亮显示"""
        if index == 5:
            self.character_index = 0
            self.surface5.blit(self.option, self.option_rect)
            self.surface6.fill((0, 0, 0))
            self.surface6.set_colorkey((0, 0, 0))
            self.surface7.fill((0, 0, 0))
            self.surface7.set_colorkey((0, 0, 0))
        elif index == 6:
            self.character_index = 1
            self.surface5.fill((0, 0, 0))
            self.surface5.set_colorkey((0, 0, 0))
            self.surface6.blit(self.help, self.help_rect)
            self.surface7.fill((0, 0, 0))
            self.surface7.set_colorkey((0, 0, 0))
        elif index == 7:
            self.character_index = 2
            self.surface5.fill((0, 0, 0))
            self.surface5.set_colorkey((0, 0, 0))
            self.surface6.fill((0, 0, 0))
            self.surface6.set_colorkey((0, 0, 0))
            self.surface7.blit(self.quit, self.quit_rect)

    def _change_view_brightness(self, index):
        """对视图模式的亮度进行切换"""
        if index == 8:
            self.view_index = 0
        elif index == 9:
            self.view_index = 1
        elif index == 10:
            self.view_index = 2
        elif index == 12:
            self.view_index = 3
        for dark_image, light_image, view_surface, view_rect in zip(self.dark_images,
                            self.light_images, self.view_surface_lists, self.view_rect_lists):
            if view_rect == self.view_rect_lists[self.view_index]:
                view_surface.blit(light_image, view_rect)
                continue
            view_surface.blit(dark_image, view_rect)

    def plot_home_page(self, index=-1):
        """在屏幕上绘制主页"""
        self.screen.blit(self.home_page, (0, 0))
        # 根据鼠标位置绘制在相应的surface上做出响应
        if index > 0:  # 点亮鼠标停留位置
            if self.last_index_value != index:  # 如果鼠标上次的停留值跟这一次不一样，就播放音乐
                self.music.play_short_time_sound(self.setting.mouse_pass)
                self.last_index_value = index  # 播放后记录本次的值
            if index <= 4:
                self._change_model_brightness(index)
            elif index <= 7:
                self._change_character_brightness(index)
            else:
                self._change_view_brightness(index)
        else:  # 复原黑色状态
            if self.model_index >= 0:
                self.model_rect_lists[self.model_index].topleft = (0, 0)

            if self.character_index >= 0:
                self.character_lists[self.character_index].fill(self.setting.fill_color)
                self.character_lists[self.character_index].set_colorkey(self.setting.fill_color)

            if self.view_index >= 0:
                self.view_surface_lists[self.view_index].blit(self.light_images[self.view_index],
                                                              self.view_rect_lists[self.view_index])
                self.view_index = -1
        # 默认第一次就将可以点击的位置显示出来
        if self.view_index < 0:
            for dark_image, view_rect, surface in zip(self.dark_images, self.view_rect_lists, self.view_surface_lists):
                surface.blit(dark_image, view_rect)
        # self.surface1.blit(self.mode1_shadow, (0, -5))
        self.surface1.blit(self.mode1, self.mode1_rect)
        self.surface2.blit(self.mode2, self.mode2_rect)
        self.surface3.blit(self.mode3, self.mode3_rect)
        self.surface4.blit(self.mode4, self.mode4_rect)
        self.surface11.blit(self.user, self.user_rect)

        # 将对应的surface绘制到屏幕上
        self.screen.blit(self.surface1, self.rect1)
        self.screen.blit(self.surface2, self.rect2)
        self.screen.blit(self.surface3, self.rect3)
        self.screen.blit(self.surface4, self.rect4)
        self.screen.blit(self.surface5, self.rect5)
        self.screen.blit(self.surface6, self.rect6)
        self.screen.blit(self.surface7, self.rect7)
        self.screen.blit(self.surface8, self.rect8)
        self.screen.blit(self.surface9, self.rect9)
        self.screen.blit(self.surface10, self.rect10)
        self.screen.blit(self.surface11, self.rect11)
        self.screen.blit(self.surface12, self.rect12)
        self.screen.blit(self.surface13, self.rect13)
