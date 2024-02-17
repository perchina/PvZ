import sys

import pygame.sprite

from collision_area.home_line import HomeLine

from game_view.home_page import HomePage
from game_view.help_view import HelpView
from game_view.garden_view import GardenView
from game_view.almanac_view import AlmanacView
from game_view.option_view import OptionView
from game_view.enter_view import EnterView

from pygame.sprite import Group
from plants.plants import *
from plants.bullets import Pea, IcePea, FirePea

from radio_video.radio import Radio

from settings.setting import Setting
from show_elements.plant_cards import PlantCards
from show_elements.map import Background
from show_elements.plants_select_board import PlantsSelectBoard

from zombies.zombies import *
from zombies.appear_zombies import StaticZombies


class PVZ:
    """游戏运行的主类"""
    def __init__(self):
        """初始化基本属性"""
        pygame.init()
        self.setting = Setting()
        # 创建帧速
        self.clock = pygame.time.Clock()
        self.main_screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        self.surface = (
            pygame.Surface((self.setting.inner_screen_width, self.setting.inner_screen_height), pygame.SRCALPHA))
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.setting.inner_screen_coordinate
        pygame.display.set_caption(self.setting.game_title)

        self.music = Radio(self)
        self.enter = EnterView(self)
        self._prep_home_page()

        self.music_start_time = 0
        self.is_in_home_page = True
        self.home_index = -1

        self.is_enter = False
        self.is_draw_in_home_page = False

        self.is_start_select = False
        self.is_start_game = False

    def _add_plant_in_area(self, index, lattice):
        """根据索引和矩形区域创建相应的类然后设置其位置"""
        if index >= 0:
            new_plant = self.plant_list.pop(index)  # 注意不添加索引默认将最后一个元素弹出
            if index == 0:
                self.plant_list.insert(index, PeaShooter(self))             # 豌豆射手
            elif index == 1:
                self.plant_list.insert(index, SunFlower(self))              # 向日葵
            elif index == 2:
                self.plant_list.insert(index, Cherry(self))                  # 樱桃炸弹
            elif index == 3:
                self.plant_list.insert(index, WallNut(self))                 # 坚果
            elif index == 4:
                pass                                                        # 土豆地雷
            elif index == 5:
                self.plant_list.insert(index, IceShooter(self))             # 寒冰射手
            elif index == 6:
                self.plant_list.insert(index, ManEatingFlower(self))        # 食人花
            elif index == 7:
                pass                                                        # 双发射手
            elif index == 8:
                pass                                                        # 小喷菇
            elif index == 9:
                pass                                                        # 阳光菇
            elif index == 10:
                pass                                                        # 大喷菇
            elif index == 11:
                pass                                                        # 嗜藤碑
            elif index == 12:
                pass                                                        # 魅惑菇
            elif index == 13:
                pass                                                        # 胆小菇
            elif index == 14:
                pass                                                        # 寒冰菇
            elif index == 15:
                pass                                                        # 毁灭菇
            elif index == 16:
                pass                                                        # 荷叶
            elif index == 17:
                pass                                                        # 窝瓜
            elif index == 18:
                self.plant_list.insert(index, ThreePea(self))               # 三线射手
            elif index == 19:
                pass                                                        # 水草
            elif index == 20:
                self.plant_list.insert(index, Pepper(self))                 # 辣椒
            elif index == 21:
                pass                                                        # 地刺
            elif index == 22:
                pass                                                        # 火炬树桩
            elif index == 23:
                pass                                                        # 高坚果
            elif index == 24:
                pass                                                        # 海蘑菇
            elif index == 25:
                pass                                                        # 路灯花
            elif index == 26:
                pass                                                        # 仙人掌
            elif index == 27:
                self.plant_list.insert(index, Clover(self))                 # 三叶草
            elif index == 28:
                pass                                                        # 双头射手
            elif index == 29:
                pass                                                        # 星星果
            elif index == 30:
                pass                                                        # 南瓜头
            elif index == 31:
                pass                                                        # 花盘
            elif index == 32:
                pass                                                        # 大蒜
            elif index == 33:
                pass                                                        # 窝瓜
            elif index == 34:
                self.plant_list.insert(index, FourPea(self))                # 机枪射手
            elif index == 35:
                pass                                                        # 双子向日葵
            elif index == 36:
                pass                                                        # 忧郁菇
            elif index == 37:
                pass                                                        # 地刺王
            elif index == 38:
                pass                                                        # 坚果保龄球
            elif index == 39:
                pass                                                        # 毁灭保龄球
            elif index == 40:
                pass                                                        # 模仿者
            self._sort_plant_to_group(new_plant, lattice)

    def _add_sunlight_in_group(self):
        """每隔一断时间增加或减少阳光"""
        current_time = time()
        if (current_time - self.when_sunlight_fall_last_time) >= self.setting.fall_sunlight_in_day:
            new_sunlight = SunLight(self)
            self.sunlights.add(new_sunlight)
            self.when_sunlight_fall_last_time = current_time

    def _add_zombie_in_group(self):
        """根据随机产生的索引创建相应的僵尸实例"""
        index = randint(0, 500)
        if index < len(self.zombie_list) - 1:
            new_zombie = self.zombie_list.pop(index)
            if index == 0:
                self.zombie_list.insert(index, GeneralZombie(self))
            elif index == 1:
                self.zombie_list.insert(index, FlagZombie(self))
            elif index == 2:
                self.zombie_list.insert(index, RoadBlockZombie(self))
            elif index == 3:
                self.zombie_list.insert(index, DrumZombie(self))
            elif index == 4:
                self.zombie_list.insert(index, FootballZombie(self))
            elif index == 5:
                self.zombie_list.insert(index, PoleVaultZombie(self))
            elif index == 6:
                self.zombie_list.insert(index, IceCarZombie(self))
            elif index == 7:
                self.zombie_list.insert(index, ImpZombie(self))
            elif index == 8:
                self.zombie_list.insert(index, ClownZombie(self))
            elif index == 9:
                self.zombie_list.insert(index, ScreenDoorZombie(self))
            elif index == 10:
                self.zombie_list.insert(index, NewspaperZombie(self))
            elif index == 11:
                self.zombie_list.insert(index, SnorkelZombie(self))
            elif index == 12:
                self.zombie_list.insert(index, DolphinRiderZombie(self))
            elif index == 13:
                self.zombie_list.insert(index, DuckyDrumZombie(self))
            elif index == 14:
                self.zombie_list.insert(index, DuckyRoadBlockZombie(self))
            elif index == 15:
                self.zombie_list.insert(index, DuckyGeneralZombie(self))
            elif index == 16:
                self.zombie_list.insert(index, DancingZombie(self))
            elif index == 17:
                self.zombie_list.insert(index, BuckupDancerZombie(self))
            self._sort_zombie_to_group(new_zombie)

    def _check_and_update_zombie_status(self):
        """检查僵尸的身体情况"""
        for zombies in self.zombies_lists:
            for zombie in zombies:
                current_time = time()
                if zombie.is_static:
                    if current_time - zombie.is_frozen_time >= 1.5:
                        zombie.is_static = False
                        zombie.speed = zombie.original_speed

    def _check_bullets_and_zombies_collide(self):
        """检测子弹和僵尸之间的碰撞并执行相应的效果"""
        for zombies_list, bullets_list in zip(self.zombies_lists, self.bullets_lists):
            collision_list = self._check_zombie_health_and_remove_zombie_or_bullets(zombies_list, bullets_list)
            if collision_list:
                # 避免一个子弹接触多个僵尸,所以这里我们将僵尸作为键,子弹作为值
                for zombie, bullets in collision_list.items():
                    for bullet in bullets:
                        if zombie.is_dead():
                            zombie.was_shot_to_die = True
                            zombie.index = 0
                            break
                        bullet.is_hit = True
                        if isinstance(bullet, Pea):
                            self.music.play_short_time_sound(self.setting.pea_hit_sound)
                        elif isinstance(bullet, IcePea):
                            if zombie.can_be_controlled:
                                self.music.play_short_time_sound(self.setting.ice_hit)
                        elif isinstance(bullet, FirePea):
                            self.music.play_short_time_sound(self.setting.fire_pea)
                        zombie.update_zombie_health(bullet.hurt)
                    zombie.update_zombie_move_status()

    def _check_cars_is_collide_zombies(self):
        """检测小推车和僵尸的碰撞"""
        for car in self.background.cars.sprites():
            car_right = car.rect.right
            collides = []
            zombies_copy = self.zombies_lists[car.car_index].copy()
            for zombie in zombies_copy:
                if not zombie.is_dead():  # 只有活着的僵尸才能够触发小推车
                    zombie_center = zombie.attack_coord[0]
                    if zombie_center <= car_right:
                        collides.append(zombie)
                        if not zombie.was_shot_to_die:
                            zombie.health = 0
                            zombie.index = 0
                            zombie.was_shot_to_die = True
                            if (isinstance(zombie, GeneralZombie) or isinstance(zombie, FootballZombie)
                                    or isinstance(zombie, RoadBlockZombie) or isinstance(zombie, DrumZombie))\
                                    or isinstance(zombie, ScreenDoorZombie) or isinstance(zombie, FlagZombie)\
                                    or isinstance(zombie, DuckyDrumZombie) or isinstance(zombie, DuckyRoadBlockZombie)\
                                    or isinstance(zombie, DuckyGeneralZombie):
                                zombie.flying_head.set_surface_location(zombie.rect.midbottom, 1)
                            elif isinstance(zombie, ClownZombie):
                                zombie.flying_head.set_surface_location(
                                    (zombie.was_attacked_coord[0],
                                     self.setting.appear_locations[zombie.lattice_index][1]),
                                    1)
            if collides and not car.is_drive:
                car.is_drive = True
                self.music.play_short_time_sound(self.setting.car_collide)

    def _check_ice_road_is_touch_areas(self):
        """检测冰道是否铺在可以种植的格子上"""
        for lattice in self.background.lattices:  # 遍历45个格子
            for ice_roads in self.ice_roads_lists:  # 遍历五行冰道
                collision_list = pygame.sprite.spritecollide(lattice, ice_roads, False)
                if collision_list:  # 这个格子与冰道有交集
                    if not lattice.don_t_plant:
                        lattice.don_t_plant = True
                    break
                else:  # 这个格子与冰道无交集
                    if lattice.don_t_plant:
                        lattice.don_t_plant = False

    def _check_events(self):
        """"检测每一帧鼠标的发生事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标左键按下的区域
                if event.button == 1:
                    mouse_down_pos = pygame.mouse.get_pos()
                    self._check_mouse_left_click_event(mouse_down_pos)
            elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标左键松开的区域
                if event.button == 1:
                    mouse_up_pos = pygame.mouse.get_pos()
                    self._check_mouse_left_loosen_event(mouse_up_pos)
            elif event.type == pygame.MOUSEMOTION:  # 鼠标左键经过的区域
                mouse_move_pos = event.pos
                self._check_mouse_move_event(mouse_move_pos)

    def _check_is_click_shovel(self, mouse_pos):
        """检测是否点击铲子"""
        if self.plant_cards.shovel_rect.collidepoint(mouse_pos):
            return True
        return False

    def _check_is_dig_plant_and_clean_lattice(self, mouse_pos):
        """检查是否点击了种植植物格子"""
        # 主窗口对内部surface操作需要计算在内部surface的实际坐标
        inner_surface_offset = self.rect
        mouse_pos_inner = (mouse_pos[0] - inner_surface_offset[0],
                           mouse_pos[1] - inner_surface_offset[1])
        row, cols = (0, 0)
        for area in self.background.lattices.sprites():
            if area.rect.collidepoint(mouse_pos_inner):
                if area.is_plant:
                    area.is_plant = False
                    row, cols = area.line, area.cols
                    break
        for plants in self.plants_lists:
            for plant in plants.sprites():
                if plant.row_cols[0] == row and plant.row_cols[1] == cols:
                    if plant.can_be_destroy:
                        plant.clear_zombies_status()
                    plants.remove(plant)
                    break

    def _check_mouse_is_pass_or_click(self, mouse_pos):
        """检测鼠标是否经过目标区域"""
        if self.home_page.rect1.collidepoint(mouse_pos):
            index = 1
        elif self.home_page.rect2.collidepoint(mouse_pos):
            index = 2
        elif self.home_page.rect3.collidepoint(mouse_pos):
            index = 3
        elif self.home_page.rect4.collidepoint(mouse_pos):
            index = 4
        elif self.home_page.rect5.collidepoint(mouse_pos):
            index = 5
        elif self.home_page.rect6.collidepoint(mouse_pos):
            index = 6
        elif self.home_page.rect7.collidepoint(mouse_pos):
            index = 7
        elif self.home_page.rect8.collidepoint(mouse_pos):
            index = 8
        elif self.home_page.rect9.collidepoint(mouse_pos):
            index = 9
        elif self.home_page.rect10.collidepoint(mouse_pos):
            index = 10
        elif self.home_page.rect12.collidepoint(mouse_pos):
            index = 12
        else:
            index = -1
        return index

    def _check_mouse_left_click_event(self, mouse_down_pos):
        """检查并处理鼠标左键点击不同位置的情况"""
        # ******************************************* 游戏未进入 **************************************************#
        if not self.is_enter and not self.is_start_game and not self.is_start_select:
            if self.enter.check_is_enter_game(mouse_down_pos):
                self.is_enter = True
                self.music_start_time = 0
        # ********************************** 游戏选项 ***************************************#
        elif self.is_enter:
            if self.is_in_home_page:  # 在主页面选择的时候
                # 只有当没有进入设置，更改用户信息时才会执行下面的所有语句
                if not self.is_draw_in_home_page:
                    self.home_index = self._check_mouse_is_pass_or_click(mouse_down_pos)
                    if self.home_index == 1:
                        self.music.stop_play_music()
                        self._prep_plant_select_interface()
                        self.music_start_time = 0
                        self.is_enter = False
                        self.is_in_home_page = False
                        self.is_start_select = True
                    elif self.home_index == 2:
                        pass
                    elif self.home_index == 3:
                        pass
                    elif self.home_index == 4:
                        pass
                    # 选项
                    elif self.home_index == 5:
                        self.music.pause_play_music()
                        self.option.is_enter = True
                        self.is_draw_in_home_page = True
                        self.home_index = -1
                    # 帮助
                    elif self.home_index == 6:
                        self.music.play_short_time_sound(self.setting.turn_book)
                        self.help.is_enter = True
                        self.is_in_home_page = False
                        self.music.pause_play_music()
                    # 退出
                    elif self.home_index == 7:
                        pygame.quit()
                        sys.exit()
                    # 花园
                    elif self.home_index == 8:
                        self.music.stop_play_music()
                        self.music_start_time = 0
                        self.garden.is_enter = True
                        self.is_in_home_page = False
                    # 图鉴
                    elif self.home_index == 9:
                        self.music_start_time = 0
                        self.almanac.is_enter = True
                        self.is_in_home_page = False
                        self.music.pause_play_music()
                    else:  # 如果为-1就通过
                        pass
                else:  # 将视图绘制到主页中的一部分，取消主页位置的检索，仅仅在特定视图内触发关键按钮后回复恢复位置检索
                    if self.option.is_enter:
                        self.option.check_mouse_click_event(mouse_down_pos)
            else:  # 到特定的页面使用各种功能时
                if self.help.is_enter:
                    if self.help.check_is_click_main_menu(mouse_down_pos):
                        self.help.is_enter = False
                        self.is_in_home_page = True
                        self.music.unpause_play_music()
                elif self.almanac.is_enter:
                    if self.almanac.check_mouse_is_click_or_pass_main_menu(mouse_down_pos):
                        self.almanac.is_enter = False
                        self.is_in_home_page = True
                        self.music_start_time = 0
                        self.music.unpause_play_music()
                elif self.garden.is_enter:
                    if self.garden.check_is_click_main_menu(mouse_down_pos):
                        self.garden.is_enter = False
                        self.is_in_home_page = True
                        self.music_start_time = 0
                    elif self.garden.check_is_click_sign(mouse_down_pos):
                        self.garden.update_next_garden()
                    elif self.garden.check_is_click_or_pass_store(mouse_down_pos):
                        pass
                else:
                    pass
        # ********************************** 游戏未暂停 ***************************************#
        elif self.is_start_select:
            if not self.option.is_enter:  # 没有进入菜单
                # 卡片数量小于10并且点击的是植物选择区域就增加卡片
                if len(self.plant_cards.show_plant_cards) < 10 and self.plant_select_board.check_click(mouse_down_pos):
                    self.plant_card_index = self.plant_select_board.index
                    self.plant_cards.add_card_to_list(self.plant_card_index)
                elif self.plant_cards.check_button.check_which_button_is_clicked(mouse_down_pos):
                    pass
                elif self.plant_cards.check_is_remove_card(mouse_down_pos):
                    self.plant_card_index = self.plant_cards.card_index
                    self.plant_select_board.recover_card_status(self.plant_card_index)
                elif self.plant_select_board.check_is_click_start_button(mouse_down_pos):
                    self.plant_cards.check_button.is_select_end = True
                    self.plant_cards.check_button.is_move = True
                    self.plant_select_board.is_arrive_location = False
                    self.plant_select_board.is_down = True
                    self.is_start_select = False
                    self.is_start_game = True
                    self._prep_game_resource()
                elif self.plant_cards.check_is_click_main_menu(mouse_down_pos):
                    self.option.is_enter = True
                    self.music.play_short_time_sound(self.setting.pause)
                    self.is_pause = True
            else:  # 进入了菜单
                self.option.check_mouse_click_event(mouse_down_pos)
        elif self.is_start_game:
            # ************************* 点击了暂停 ************************************#
            if not self.option.is_enter:
                # ***************************** 点击了视图按钮 ********************************#
                if self.plant_cards.check_button.check_which_button_is_clicked(mouse_down_pos):
                    pass
                # ***************************** 点击了主菜单 ********************************#
                elif self.plant_cards.check_is_click_main_menu(mouse_down_pos):
                    self.option.is_enter = True
                    self.music.play_short_time_sound(self.setting.pause)
                    self.is_pause = True
                # ***************************** 点击了铲子 ********************************#
                elif not self.plant_cards.shovel_active and self.plant_cards.check_is_click_shovel(mouse_down_pos):
                    self.music.play_short_time_sound(self.setting.shovel_sound)
                    self.plant_cards.shovel_active = not self.plant_cards.shovel_active
                elif self.plant_cards.shovel_active:
                    if self.plant_cards.check_is_click_shovel(mouse_down_pos):
                        self.music.play_short_time_sound(self.setting.shovel_back_sound)
                    else:
                        self.music.play_short_time_sound(self.setting.plant_sound_in_grass)
                    self.plant_cards.shovel_active = False
                # ***************************** 收取了阳光 ********************************#
                elif self._check_is_click_sunlight(mouse_down_pos):
                    self.plant_cards.sunlight_stat.prep_sunlight_value(25)
                # ***************************** 选择了一颗植物 ********************************#
                elif (not self.plant_cards.is_select_plant
                      and self.plant_cards.check_is_can_click_plant_card(mouse_down_pos) == 1):
                    self.plant_card_index = self.plant_cards.card_index
                # ***************************** 选择了植物可能会做如下的操作********************************#
                elif self.plant_cards.is_select_plant:
                    # ***************************** 选择了植物又取消选择 ********************************#
                    if self.plant_cards.check_is_can_click_plant_card(mouse_down_pos) == 2:
                        self.plant_card_index = self.plant_cards.card_index
                    # ***************************** 选择了植物开始种植植物********************************#
                    elif self._check_where_plant(mouse_down_pos):
                        self.plant_cards.sunlight_stat.prep_sunlight_value(
                            -self.plant_cards.show_plant_cards[self.plant_cards.list_index].sunlight_cost)
                        self.plant_cards.show_plant_cards[self.plant_cards.list_index].is_rest_time = True
                        self.plant_cards.check_is_can_click_plant_card(mouse_down_pos)
                        self.plant_cards.list_index = -1
            else:
                # ***************************** 点击了返回游戏的按钮 ********************************#
                self.option.check_mouse_click_event(mouse_down_pos)

    def _check_mouse_left_loosen_event(self, mouse_up_pos):
        """检测鼠标左键松开事件"""
        if self.is_enter:
            if self.option.is_enter:
                self.option.check_mouse_choose_event(mouse_up_pos)
            else:
                pass
        elif self.is_start_select or self.is_start_game:
            if self.option.is_enter:
                self.option.check_mouse_choose_event(mouse_up_pos)

    def _check_mouse_move_event(self, mouse_move_pos):
        """检测鼠标移动的事件并处理"""
        # ********************************** 游戏选项 ***************************************#
        if not self.is_enter and not self.is_start_select and not self.is_start_game:
            if self.enter.check_is_pass_start_game(mouse_move_pos):
                self.enter.is_light = True
            else:
                self.enter.is_light = False
        elif self.is_enter:
            if self.is_in_home_page:  # 在主页时的操作
                if not self.is_draw_in_home_page:
                    self.home_index = self._check_mouse_is_pass_or_click(mouse_move_pos)
            else:  # 不在主页时的操作
                if self.help.is_enter:
                    if self.help.check_is_click_main_menu(mouse_move_pos):
                        pass
                elif self.almanac.is_enter:
                    if self.almanac.check_mouse_is_click_or_pass_main_menu(mouse_move_pos):
                        pass
                    elif self.almanac.check_mouse_is_click_or_pass_plant_view(mouse_move_pos):
                        pass
                elif self.garden.is_enter:
                    if self.garden.check_is_click_or_pass_store(mouse_move_pos):
                        pass
                else:
                    pass
        elif self.is_start_select:
            if self.plant_select_board.check_is_click_start_button(mouse_move_pos):
                pass

    def _check_pepper_and_ice_roads_collide(self):
        """检测火爆辣椒和冰道之间的碰撞"""
        for plants in self.plants_lists:
            for plant in plants:
                if isinstance(plant, Pepper) and plant.is_work_hurt:
                    if plant.line == 1:
                        if self.ice_roads_lists[0]:
                            self.ice_roads_lists[0].empty()
                        if self.ice_roads_lists[1]:
                            self.ice_roads_lists[1].empty()
                    elif plant.line == 2:
                        if self.ice_roads_lists[0]:
                            self.ice_roads_lists[0].empty()
                        if self.ice_roads_lists[1]:
                            self.ice_roads_lists[1].empty()
                        if self.ice_roads_lists[2]:
                            self.ice_roads_lists[2].empty()
                    elif plant.line == 3:
                        if self.ice_roads_lists[1]:
                            self.ice_roads_lists[1].empty()
                        if self.ice_roads_lists[2]:
                            self.ice_roads_lists[2].empty()
                        if self.ice_roads_lists[3]:
                            self.ice_roads_lists[3].empty()
                    elif plant.line == 4:
                        if self.ice_roads_lists[2]:
                            self.ice_roads_lists[2].empty()
                        if self.ice_roads_lists[3]:
                            self.ice_roads_lists[3].empty()
                        if self.ice_roads_lists[4]:
                            self.ice_roads_lists[4].empty()
                    elif plant.line == 5:
                        if self.ice_roads_lists[3]:
                            self.ice_roads_lists[3].empty()
                        if self.ice_roads_lists[4]:
                            self.ice_roads_lists[4].empty()
                    return None

    def _check_plants_and_zombies_collide(self):
        """检测植物和僵尸的碰撞"""
        for plants, zombies in zip(self.plants_lists, self.zombies_lists):
            collision_dict = self._find_plants_and_zombies_collide_dict(plants, zombies)
            if collision_dict:
                for plant, zombie_list in collision_dict.items():
                    for zombie in zombie_list:
                        if isinstance(zombie, IceCarZombie):
                            plant.health = 0
                            for zombie_c in zombie_list:
                                zombie_c.is_touch_plant = False
                                zombie_c.index = 0
                            break
                        else:
                            zombie.update_collided_plant_health(plant)
                            if plant.health <= 0:  # 如果该植物在接触到这个僵尸计算伤害之后已经死亡， 我们将接触该植物的所有僵尸释放并
                                # 跳转到下一个键值对
                                for zombie_c in zombie_list:
                                    zombie_c.is_touch_plant = False
                                    zombie_c.index = 0
                                break

    def _check_is_click_sunlight(self, mouse_pos):
        """检查是否点击到了阳光"""
        for sunlight in self.sunlights:
            if not sunlight.is_click:  # 该阳光从未被点击过
                if sunlight.check_is_click_sunlight(mouse_pos):  # 点击了该阳光
                    return True
        return False

    def _check_music_interval_time(self, current_time, interval_time):
        """"判断音乐播放的持续时间是否已经超过了间隔时间"""
        # 游戏开始后才会对其中的暂停间隔时间做加法运算
        if self.is_start_game:
            self.music_start_time += self.pause_time
        if current_time - self.music_start_time >= interval_time:
            return True
        return False

    def _check_where_plant(self, mouse_pos):
        """"检查是否点击到了可以种植植物的区域"""
        inner_surface_offset = self.rect
        mouse_pos_inner = (mouse_pos[0] - inner_surface_offset[0],
                           mouse_pos[1] - inner_surface_offset[1])
        for lattice in self.background.lattices:
            if lattice.rect.collidepoint(mouse_pos_inner):  # 我们只对点击到的格子进行操作
                if not lattice.is_plant and not lattice.don_t_plant:  # 我们只允许一个格子容纳一颗植物
                    if self.plant_list[self.plant_card_index]:  # 我们只对正常选择的模式进行操作
                        self._add_plant_in_area(self.plant_card_index, lattice)
                        return True
        return False

    def _check_zombies_health_and_remove(self):
        """将真正死亡的僵尸移除"""
        temp_zombies = self.zombies_lists.copy()
        index = 0
        for zombies in temp_zombies:
            for zombie in zombies.sprites():
                if zombie.is_the_zombie_really_dead():
                    print(zombie.name, '被移除')
                    self.zombies_lists[index].remove(zombie)
            index += 1

    def _check_zombie_health_and_remove_zombie_or_bullets(self, zombies_list, bullets_list):
        """根据僵尸的血量是否超出临界值确定是否忽略僵尸或者移除子弹"""
        new_collision_dict = {}
        for zombie in zombies_list:
            # 没有被炸死，没有被打死，也并非处于无敌状态
            if not zombie.was_shot_to_die and not zombie.was_boom_to_die and not zombie.is_invincible:
                values = []
                for bullet in bullets_list:
                    collision_x_center_zombie = zombie.was_attacked_coord[0]
                    collision_x_center_bullet = bullet.rect.center[0]
                    collision_x_left_bullet = bullet.rect.topleft[0]
                    if (collision_x_left_bullet <= collision_x_center_zombie <= collision_x_center_bullet
                            and not bullet.is_hit):
                        values.append(bullet)
                        if isinstance(bullet, FirePea):
                            bullet.burn_fire.set_surface_location(zombie.was_attacked_coord)
                            if zombie.is_static:
                                zombie.is_static = False
                                zombie.speed = zombie.original_speed
                        elif isinstance(bullet, IcePea):
                            if zombie.can_be_controlled:
                                bullet.ice.set_surface_location(zombie.was_frozen_coord)
                                bullet.ice.ice_apper_time = time()
                                zombie.is_frozen_time = time()
                                zombie.is_static = True
                                zombie.speed = 0
                        elif isinstance(bullet, Pea):
                            bullet.pea_break.set_surface_location(zombie.was_attacked_coord)
                            bullet.pea_break.pea_break_time = time()
                new_collision_dict[zombie] = values
        return new_collision_dict

    def _check_zombies_is_arrive(self, zombies, plant=None):
        """检测僵尸是否到达了指定位置"""
        # 仅对子弹类植物做此判断
        if not plant:
            for zombie in zombies:
                if zombie.attack_coord[0] <= self.setting.fire_distance:  # 这一行僵尸已经到了攻击范围内
                    return True
        else:
            for zombie in zombies:
                if plant.attack_coord[0] < zombie.attack_coord[0] <= self.setting.fire_distance:  # 这一行僵尸已经到了攻击范围内
                    if not zombie.was_shot_to_die and not zombie.was_boom_to_die:
                        # 并且僵尸走在植物的前面没有死亡
                        return True
        return False

    def _create_different_line_bullets_group(self):
        """创建不同行的子弹组"""
        self.bullets_lists = []
        if self.map_index == 2 or self.map_index == 3:
            for _ in range(0, 6):
                bullet_line = Group()
                self.bullets_lists.append(bullet_line)
        else:
            for _ in range(0, 5):
                bullet_line = Group()
                self.bullets_lists.append(bullet_line)

    def _create_different_line_plants_group(self):
        """创建不同行的植物组"""
        self.plants_lists = []
        if self.map_index == 2 or self.map_index == 3:
            for _ in range(0, 6):
                plant_line = Group()
                self.plants_lists.append(plant_line)
        else:
            for _ in range(0, 5):
                plant_line = Group()
                self.plants_lists.append(plant_line)

    def _create_different_line_zombies_group(self):
        """创建不同行的僵尸组"""
        self.zombies_lists = []
        if self.map_index == 2 or self.map_index == 3:
            for _ in range(0, 6):
                zombie_line = Group()
                self.zombies_lists.append(zombie_line)
        else:
            for _ in range(0, 5):
                zombie_line = Group()
                self.zombies_lists.append(zombie_line)

    def _create_different_line_ice_roads_group(self):
        """创建不同的冰道行"""
        self.ice_roads_lists = []
        if self.map_index == 2 or self.map_index == 3:
            for _ in range(0, 4):
                ice_road_line = Group()
                self.ice_roads_lists.append(ice_road_line)
        else:
            for _ in range(0, 5):
                ice_road_line = Group()
                self.ice_roads_lists.append(ice_road_line)

    def _create_bullet_instance_list(self):
        """创建各种子弹列表"""
        self.bullet_list = [Pea(self),
                            IcePea(self),
                            FirePea(self)]

    def _create_plant_instance_list(self):
        """"根据索引和植物格子"""
        self.plant_list = [PeaShooter(self),
                           SunFlower(self),
                           Cherry(self),
                           WallNut(self),
                           None,
                           IceShooter(self),
                           ManEatingFlower(self),
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           ThreePea(self),
                           None,
                           Pepper(self),
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           Clover(self),
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,
                           FourPea(self),
                           None,
                           None,
                           None,
                           None,
                           None,
                           None,]

    def _create_zombie_instance_list(self):
        """"创建僵尸实例列表"""
        self.zombie_list = [GeneralZombie(self),
                            FlagZombie(self),
                            RoadBlockZombie(self),
                            DrumZombie(self),
                            FootballZombie(self),
                            PoleVaultZombie(self),
                            IceCarZombie(self),
                            ImpZombie(self),
                            ClownZombie(self),
                            ScreenDoorZombie(self),
                            NewspaperZombie(self),
                            SnorkelZombie(self),
                            DolphinRiderZombie(self),
                            DuckyDrumZombie(self),
                            DuckyRoadBlockZombie(self),
                            DuckyGeneralZombie(self),
                            DancingZombie(self),
                            BuckupDancerZombie(self),]

    def _check_plant_kind_and_do_event(self):
        """寻找植物的种类然后做相应的事件"""
        current_time = time()
        # 一行一行的执行,每次执行五次
        index = 0
        for plants, bullets, zombies in zip(self.plants_lists, self.bullets_lists, self.zombies_lists):
            if zombies and self._check_zombies_is_arrive(zombies):  # 这一行有僵尸并且已经到达了射程范围内
                for plant in plants.sprites():
                    if isinstance(plant, SunFlower):                                                       # 向日葵
                        plant.check_is_create_sunlight()
                    elif isinstance(plant, PeaShooter) and self._check_zombies_is_arrive(zombies, plant):  # 豌豆射手
                        plant.add_bullet(index, current_time)
                    elif isinstance(plant, WallNut):                                                       # 坚果墙
                        plant.check_health_status()
                    elif isinstance(plant, IceShooter) and self._check_zombies_is_arrive(zombies, plant):
                        # 检测到是寒冰豌豆射手
                        plant.add_bullet(index, current_time)
                    elif isinstance(plant, ThreePea) and self._check_zombies_is_arrive(zombies, plant):    # 三线射手
                        plant.add_bullet(index, current_time)
                    elif isinstance(plant, FourPea) and self._check_zombies_is_arrive(zombies, plant):     # 机枪射手
                        plant.add_bullet(index, current_time)
                    elif isinstance(plant, ManEatingFlower):  # 检测到是食人花
                        plant.check_is_attack_zombies(zombies)
                    elif isinstance(plant, Cherry):                                                        # 樱桃炸弹
                        if plant.is_work_hurt:  # 检测到是否播放到了伤害帧
                            plant.check_ashes_plants_and_zombies_collide(index, self.setting.cherry_bomb)
                    elif isinstance(plant, Pepper):                                                        # 火爆辣椒
                        if plant.pepper_is_end_play:
                            if plant.is_work_hurt:  # 检测到是否播放到了伤害帧
                                plant.check_ashes_plants_and_zombies_collide(index, self.setting.pepper_burn)
            else:  # 这一行没有僵尸或者僵尸没有到达攻击范围内,通常是灰烬植物
                for plant in plants.sprites():
                    if isinstance(plant, Cherry):                                                          # 樱桃炸弹
                        if plant.is_work_hurt:  # 检测到是否播放到了伤害帧
                            plant.check_ashes_plants_and_zombies_collide(index, self.setting.cherry_bomb)
                    elif isinstance(plant, ThreePea):                                                      # 三线射手
                        if plant.check_zombies_is_appear_in_other_line(index):  # 在其它行中发现了僵尸
                            plant.add_bullet(index, current_time)
                    elif isinstance(plant, Pepper):                                                        # 火爆辣椒
                        if plant.is_work_hurt:  # 检测到是否播放到了伤害帧
                            plant.check_ashes_plants_and_zombies_collide(index, self.setting.pepper_burn)
            index += 1

    def _find_plants_and_zombies_collide_dict(self, plants, zombies):
        """返回一个植物和僵尸的碰撞列表"""
        collision_dict = {}
        for plant in plants:
            if plant.can_be_destroy:
                plant.zombie_list.clear()
                plant_left_x = plant.was_attacked_coord[0]
                plant_right_x = plant.was_attacked_coord[1]
                zombie_list = []
                for zombie in zombies:
                    if not zombie.was_shot_to_die and not zombie.was_boom_to_die:
                        if plant_left_x < zombie.attack_coord[0] < plant_right_x:
                            # ******************** 下列僵尸碰到植物一击必杀 *********************************
                            if isinstance(zombie, IceCarZombie):
                                zombie_list.append(zombie)
                            # ******************** 下列僵尸只会吃咬植物 *********************************
                            elif isinstance(zombie, DancingZombie):
                                if zombie.is_can_be_change:
                                    if not zombie.is_touch_plant:
                                        zombie.index = 0
                                        zombie.is_touch_plant = True
                                    plant.add_zombie_to_attack_list(zombie)
                                    zombie_list.append(zombie)
                            elif isinstance(zombie, PoleVaultZombie):
                                if zombie.is_lost_pole:
                                    if not zombie.is_touch_plant:
                                        zombie.index = 0
                                        zombie.is_touch_plant = True
                                    plant.add_zombie_to_attack_list(zombie)
                                    zombie_list.append(zombie)
                                else:
                                    if not zombie.is_touch_plant and not zombie.is_jump and not zombie.is_fall:
                                        zombie.index = 0
                                        zombie.is_touch_plant = True
                                        zombie.is_jump = True
                            elif isinstance(zombie, SnorkelZombie):
                                if zombie.is_in_river:
                                    if not zombie.is_touch_plant:
                                        zombie.index = 0
                                        zombie.is_touch_plant = True
                                        zombie.is_invincible = False
                                        zombie.is_rise = True
                                    plant.add_zombie_to_attack_list(zombie)
                                    zombie_list.append(zombie)
                            elif isinstance(zombie, DolphinRiderZombie):
                                if zombie.is_in_river:
                                    if zombie.is_lost_dolphin and zombie.jump_is_end_play:
                                        if not zombie.is_touch_plant:
                                            zombie.index = 0
                                            zombie.is_touch_plant = True
                                        plant.add_zombie_to_attack_list(zombie)
                                        zombie_list.append(zombie)
                                    else:
                                        if not zombie.is_jump:
                                            zombie.is_invincible = True
                                            zombie.is_touch_plant = True
                                            zombie.is_jump = True
                                            zombie.index = 0
                                            zombie.x -= (zombie.width - 80)
                                            zombie.rect.x = zombie.x
                            elif (isinstance(zombie, DuckyRoadBlockZombie) or isinstance(zombie, DuckyDrumZombie)
                                    or isinstance(zombie, DuckyGeneralZombie)):
                                if zombie.is_in_river:
                                    if not zombie.is_touch_plant:
                                        zombie.index = 0
                                        zombie.is_touch_plant = True
                                    plant.add_zombie_to_attack_list(zombie)
                                    zombie_list.append(zombie)
                            else:
                                if not zombie.is_touch_plant:
                                    zombie.index = 0
                                    zombie.is_touch_plant = True
                                plant.add_zombie_to_attack_list(zombie)
                                zombie_list.append(zombie)
                collision_dict[plant] = zombie_list
        return collision_dict

    def _plot_game_elements(self):
        """"更新并绘制元素"""
        self.surface.fill(self.setting.fill_color)
        self.background.draw_background()
        if not self.option.is_enter:
            self.static_zombies.blit_zombies(self.is_pause, self.plant_cards.check_button.inner_rect.topleft)
            self._update_game_music()
            # 区域的隐藏绘制
            self.home_line.plot_area()
            # 区域的明显绘制
            self._update_plants_and_zombies_and_bullets()
            self._show_plants_and_zombies_and_bullets()
            self.main_screen.blit(self.surface, self.plant_cards.check_button.inner_rect.topleft)
            self.plant_cards.blit_all(self.is_pause)
            # 绘制到主屏幕上
            if self.plant_select_board.is_enter:
                self.plant_select_board.show_plant_cards()
            self._show_sunlight(self.is_pause)
        else:
            self.static_zombies.blit_zombies(self.is_pause, self.plant_cards.check_button.inner_rect.topleft)
            self._show_plants_and_zombies_and_bullets()
            self.main_screen.blit(self.surface, self.plant_cards.check_button.inner_rect.topleft)
            self.plant_cards.blit_all(self.is_pause)
            # 绘制到主屏幕上
            if self.plant_select_board.is_enter:
                self.plant_select_board.show_plant_cards()
            self._show_sunlight(self.is_pause)
            self.option.plot_set_board()

    def _plot_game_enter_interface(self):
        self.enter.plot_wait_background()
        self._work_time_and_play_music(self.setting.wait_interval, self.setting.wait)

    def _plot_game_home_page_interface(self):
        # 绘制主页
        if self.is_in_home_page:  # 现在的页面可以展示主页
            # 音乐如果被暂停了就会继续播放音乐，如果没有暂停就会继续计算时间
            self._work_time_and_play_music(self.setting.home_page_interval, self.setting.home_page_music)
            self.home_page.plot_home_page(self.home_index)
            if self.option.is_enter:
                self.option.plot_set_board()  # 先展示按钮下坠的效果，紧接着对是否跳出了该视图进行对应的属性设置

        else:  # 现在的页面不能够展示主页
            if self.help.is_enter:
                self.music.pause_play_music()
                self.help.plot_help_view()
            elif self.almanac.is_enter:
                self._work_time_and_play_music(self.setting.choose_seed_interval, self.setting.choose_seed)
                self.almanac.plot_almanac_view()
            elif self.garden.is_enter:
                self.garden.plot_garden_view()
                self._work_time_and_play_music(self.setting.garden_interval, self.setting.garden_zen)

    def _plot_plant_select_interface(self):
        """绘制植物的选择界面"""
        self.background.draw_background()
        self.static_zombies.blit_zombies(self.is_pause, self.plant_cards.check_button.inner_rect.topleft)
        self.plant_cards.blit_all(self.is_pause)
        if self.plant_select_board.is_enter:
            self.plant_select_board.show_plant_cards()
        if self.option.is_enter:
            self.option.plot_set_board()

    def _prep_home_page(self):
        """进入游戏后准备游戏主页面"""
        self.background = Background(self)
        self.home_page = HomePage(self)
        self.option = OptionView(self)
        self.help = HelpView(self)
        self.almanac = AlmanacView(self)
        self.garden = GardenView(self)
        self.map_index = 4

    def _prep_plant_select_interface(self):
        """植物选择界面"""
        self.background = Background(self)
        self.plant_cards = PlantCards(self)
        self.plant_select_board = PlantsSelectBoard(self)
        self.plant_select_board.is_enter = True
        self.background.select_background(self.map_index)
        self.static_zombies = StaticZombies(self)
        self.plant_card_index = -1
        self.is_pause = False

    def _prep_game_resource(self):
        """"游戏确认开始将准备游戏资源"""
        self.music_index = -1
        self.music_pause_time = 0
        self.pause_time = 0
        self.when_sunlight_fall_last_time = time()

        self.home_line = HomeLine(self)
        self.sunlights = Group()

        self._create_plant_instance_list()
        self._create_zombie_instance_list()
        self._create_bullet_instance_list()

        self._create_different_line_bullets_group()
        self._create_different_line_plants_group()
        self._create_different_line_ice_roads_group()
        self._create_different_line_zombies_group()

    def _sort_plant_to_group(self, plant, lattice):
        """将新种植的植物分配到指定组中"""
        self.plants_lists[lattice.line - 1].add(plant)
        plant.reset_surface_coordinate(lattice)
        # 是否需要荷叶才能够种植
        if lattice.is_need_plant_lilypad:
            plant.is_in_pool = True
        # 是否需要种植盆栽
        elif lattice.is_need_plant_flower_pot:
            plant.is_in_grass = True
        plant.row_cols = lattice.line, lattice.cols
        lattice.is_plant = True

    def _sort_zombie_to_group(self, zombie):
        """将出现的僵尸按照行的顺序分配到指定到组中"""
        self.zombies_lists[zombie.lattice_index].add(zombie)

    def _show_plants_and_zombies_and_bullets(self):
        """先绘制植物，紧接着僵尸，最后子弹"""
        index = 0
        for plants, ice_roads, zombies, bullets in \
                (zip(self.plants_lists, self.ice_roads_lists, self.zombies_lists, self.bullets_lists)):
            for ice_road in ice_roads.sprites():
                ice_road.show_ice_road()
            for plant in plants.sprites():
                plant.show_plant(self.is_pause)
            for zombie in zombies.sprites():
                if isinstance(zombie, IceCarZombie):  # 通过冰车僵尸增加冰道
                    zombie.show_zombie(self.is_pause, self.ice_roads_lists[index])
                else:
                    zombie.show_zombie(self.is_pause)
            for bullet in bullets.sprites():
                bullet.draw_bullet(self.is_pause)
            index += 1

    def _show_sunlight(self, pause):
        """在屏幕上绘制阳光"""
        if not self.is_pause:
            current_time = time()
            sun_list = self.sunlights.copy()
            for sun in sun_list:
                if current_time - sun.alive_time >= sun.alive_time_limit:  # 存活时间大于设定时间
                    self.sunlights.remove(sun)
                elif sun.rect.topleft[0] < 10 and sun.rect.topleft[1] < 10:  # 到达指定区域后移除
                    self.sunlights.remove(sun)
            self._add_sunlight_in_group()
        for sunlight in self.sunlights:
            sunlight.draw_sunlight(pause)

    def _update_game_music(self):
        """根据不同时间间隔更新音乐"""
        current_time = time()
        if (self._check_music_interval_time(current_time, self.setting.game_music_interval[self.music_index])
                or self.music_index == -1):
            self.music_index = randint(0, 8)
            self.music.play_music(self.setting.game_start_musics[self.music_index])
            self.music_start_time = current_time

    def _update_plants_and_zombies_and_bullets(self):
        """依次更新植物，僵尸，子弹的状态"""
        # 更新冰道：
        self._check_ice_road_is_touch_areas()
        self._check_pepper_and_ice_roads_collide()
        current_time = time()
        for ice_road_list in self.ice_roads_lists:
            ice_road_copy = ice_road_list.copy()
            for ice_road in ice_road_copy:
                if isinstance(ice_road, IceRoadHead):
                    if current_time - ice_road.last_plot_time >= 30:
                        ice_road_list.empty()
                        break
        # 更新植物
        if not self.is_pause:
            self._check_plant_kind_and_do_event()
            self._check_plants_and_zombies_collide()
            for plants in self.plants_lists:
                temp_plants = plants.copy()
                for plant in temp_plants:
                    if plant.health <= 0 or plant.is_end_play:
                        row, cols = plant.row_cols
                        for lattice in self.background.lattices:
                            if lattice.line == row and lattice.cols == cols:
                                lattice.is_plant = False
                                break
                        plants.remove(plant)
        # 更新僵尸
        if not self.is_pause:
            self._check_bullets_and_zombies_collide()
            self._check_and_update_zombie_status()
            self._check_zombies_health_and_remove()
            # self._add_zombie_in_group()
        # 更新子弹
        for bullets in self.bullets_lists:
            bullets_copy = bullets.copy()
            for bullet in bullets_copy:
                if bullet.check_is_surpass_distance():
                    bullets.remove(bullet)
                elif bullet.is_end_play:
                    bullets.remove(bullet)

    def _work_time_and_play_music(self, interval_time, music):
        """"根据时间间隔播放音乐"""
        current_time = time()
        if not self.is_draw_in_home_page:  # 主页视图如果什么都没有我们就正常播放音乐并计算持续时长
            # 其中的没有包括已经进入到游戏视图，主页视图
            if self._check_music_interval_time(current_time, interval_time) or self.music_start_time == 0:
                self.music.play_music(music)
                self.music_start_time = current_time
                self.pause_time = 0
        else:
            self.music_start_time = current_time

    def run_game(self):
        """"游戏主要运行方法"""
        while True:
            self.main_screen.fill(self.setting.fill_color)
            self._check_events()
            if self.is_start_game:  # 选择好了植物进入了游戏
                self._plot_game_elements()
            elif self.is_start_select:  # 开始选择植物
                self._plot_plant_select_interface()
            elif self.is_enter:  # 进入了游戏主页面
                self._plot_game_home_page_interface()
            elif not self.is_start_game and not self.is_start_game and not self.is_enter:  # 仅仅是进入了游戏
                self._plot_game_enter_interface()
            pygame.display.flip()
            self.clock.tick(60)
