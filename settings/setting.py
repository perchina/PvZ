import pygame
from PIL import Image


class Setting:
    """"需要用到的对象属性"""
    def __init__(self):
        """主程序的基本属性"""
    # *******************************************  屏幕属性 **************************************************#
        # 之前一直未考虑过不同显示器分辨率不同的问题，现在采用获取当前显示器的分辨率再使用最小比例缩放，使得游戏可以在每一台电脑上
        # 能够有效的展示，而不是存在窗口占满整个屏幕的情况
        self.screen_width, self.screen_height = (1080, 594)
        self.zombie_move_limit = self.screen_width * 0.193
        # 内部屏幕容纳内容的纵横宽高
        self.inner_screen_width, self.inner_screen_height = (int(self.screen_width * 1.6), self.screen_height)
        self.inner_screen_speed = 1
        self.inner_screen_coordinate = (-self.screen_width*0.2, 0)
        self.fill_color = (0, 0, 0)
        self.game_title = 'Plants Vs Zombies'
        self.wait_background = 'materials/game_background/wait_bg.png'
        self.grass_day = 'materials/game_background/background1.jpg'
        self.grass_night = 'materials/game_background/background2.jpg'
        self.swimming_pool_day = 'materials/game_background/background3.jpg'
        self.swimming_pool_night = 'materials/game_background/background4.jpg'
        self.pool_day_gif = 'materials/game_background/pool_day.gif'
        self.pool_night_gif = 'materials/game_background/pool_night.gif'
        self._create_pool_image_list()
        self.roof_day = 'materials/game_background/background5.jpg'
        self.roof_night = 'materials/game_background/background6boss.jpg'

        self.home_page = 'materials/game_elements/homepage.png'
        self.help_background = 'materials/game_background/help_background.png'
        self.almanac_background = 'materials/game_elements/Almanac_IndexBack.jpg'
        self.garden_list = ['materials/game_background/garden.jpg',
                            'materials/game_background/night_background.jpg',
                            'materials/game_background/water_background.jpg',]
    # *******************************************  字体属性 **************************************************#
        self.font_path = 'materials/font/truetype.ttf'
    # ****************************************** 植物选择面板属性 ************************************************#
        self.start_game_button = 'materials/game_elements/一起摇滚吧.png'
        self.plant_select_board_png = 'materials/game_elements/植物选择面板.png'
        # 植物展示卡片
        self.plant_select_list = ['materials/Plants/Peashooter/Peashooter.png',
                                  'materials/Plants/SunFlower/SunFlower.png',
                                  'materials/Plants/CherryBomb/CherryBomb.png',
                                  'materials/Plants/WallNut/WallNut.png',
                                  'materials/Plants/PotatoMine/PotatoMine.png',
                                  'materials/Plants/SnowPea/SnowPea.png',
                                  'materials/Plants/Chomper/Chomper.png',
                                  'materials/Plants/Repeater/Repeater.png',
                                  'materials/Plants/PuffShroom/PuffShroom.png',
                                  'materials/Plants/SunShroom/SunShroom.png',
                                  'materials/Plants/FumeShroom/FumeShroom.png',
                                  'materials/Plants/GraveBuster/GraveBuster.png',
                                  'materials/Plants/HypnoShroom/HypnoShroom.png',
                                  'materials/Plants/ScaredyShroom/ScaredyShroom.png',
                                  'materials/Plants/IceShroom/IceShroom.png',
                                  'materials/Plants/DoomShroom/DoomShroom.png',
                                  'materials/Plants/LilyPad/LilyPad.png',
                                  'materials/Plants/Squash/Squash.png',
                                  'materials/Plants/Threepeater/Threepeater.png',
                                  'materials/Plants/TangleKlep/TangleKlep.png',
                                  'materials/Plants/Jalapeno/Jalapeno.png',
                                  'materials/Plants/Spikeweed/Spikeweed.png',
                                  'materials/Plants/Torchwood/Torchwood.png',
                                  'materials/Plants/TallNut/TallNut.png',
                                  'materials/Plants/SeaShroom/SeaShroom.png',
                                  'materials/Plants/Plantern/Plantern.png',
                                  'materials/Plants/Cactus/Cactus.png',
                                  'materials/Plants/Blover/Blover.png',
                                  'materials/Plants/SplitPea/SplitPea.png',
                                  'materials/Plants/Starfruit/Starfruit.png',
                                  'materials/Plants/PumpkinHead/PumpkinHead.png',
                                  'materials/Plants/FlowerPot/FlowerPot.png',
                                  'materials/Plants/CoffeeBean/CoffeeBean.png',
                                  'materials/Plants/Garlic/Garlic.png',
                                  'materials/Plants/GatlingPea/GatlingPea.png',
                                  'materials/Plants/TwinSunflower/TwinSunflower.png',
                                  'materials/Plants/GloomShroom/GloomShroom.png',
                                  'materials/Plants/Spikerock/Spikerock.png',
                                  'materials/Plants/WallNut/坚果保龄球彩黑.png',
                                  'materials/Plants/WallNut/毁灭坚果彩黑.png']
        self.imitator_color = 'materials/Plants/Imitator/模仿者.png'
        self.imitator_black = 'materials/Plants/Imitator/模仿者槽阴影.png'
        # 植物卡片
        self.card_list = [['materials/Plants/Peashooter/豌豆卡片.png',
                           'materials/Plants/Peashooter/豌豆卡片阴影.png', 0, 100, 7.5],
                          ['materials/Plants/SunFlower/向日葵卡片.png',
                          'materials/Plants/SunFlower/向日葵卡片阴影.png', 1, 50, 7.5],
                          ['materials/Plants/CherryBomb/樱桃卡片.png',
                           'materials/Plants/CherryBomb/樱桃卡片阴影.png', 2, 150, 50],
                          ['materials/Plants/WallNut/土豆卡片.png',
                           'materials/Plants/WallNut/土豆卡片阴影.png', 3, 50, 30],
                          ['materials/Plants/PotatoMine/PotatoMine卡片.png',
                           'materials/Plants/PotatoMine/PotatoMine阴影.png', 4, 25, 30],
                          ['materials/Plants/SnowPea/寒冰射手卡片.png',
                           'materials/Plants/SnowPea/寒冰射手卡片阴影.png', 5, 175, 7.5],
                          ['materials/Plants/Chomper/食人花卡片.png',
                           'materials/Plants/Chomper/食人花卡片阴影.png', 6, 150, 7.5],
                          ['materials/Plants/Repeater/Repeater卡片.png',
                           'materials/Plants/Repeater/Repeater阴影.png', 7, 200, 7.5],
                          ['materials/Plants/PuffShroom/PuffShroom卡片.png',
                           'materials/Plants/PuffShroom/PuffShroom阴影.png', 8, 0, 7.5],
                          ['materials/Plants/SunShroom/SunShroom卡片.png',
                           'materials/Plants/SunShroom/SunShroom阴影.png', 9, 25, 7.5],
                          ['materials/Plants/FumeShroom/FumeShroom卡片.png',
                           'materials/Plants/FumeShroom/FumeShroom阴影.png', 10, 75, 7.5],
                          ['materials/Plants/GraveBuster/GraveBuster卡片.png',
                           'materials/Plants/GraveBuster/GraveBuster阴影.png', 11, 75, 7.5],
                          ['materials/Plants/HypnoShroom/HypnoShroom卡片.png',
                           'materials/Plants/HypnoShroom/HypnoShroom阴影.png', 12, 75, 30],
                          ['materials/Plants/ScaredyShroom/ScaredyShroom卡片.png',
                           'materials/Plants/ScaredyShroom/ScaredyShroom阴影.png', 13, 25, 7.5],
                          ['materials/Plants/IceShroom/IceShroom卡片.png',
                           'materials/Plants/IceShroom/IceShroom阴影.png', 14, 75, 50],
                          ['materials/Plants/DoomShroom/DoomShroom卡片.png',
                           'materials/Plants/DoomShroom/DoomShroom阴影.png', 15, 125, 50],
                          ['materials/Plants/LilyPad/LilyPad卡片.png',
                           'materials/Plants/LilyPad/LilyPad阴影.png', 16, 25, 7.5],
                          ['materials/Plants/Squash/Squash卡片.png',
                           'materials/Plants/Squash/Squash阴影.png', 17, 50, 30],
                          ['materials/Plants/Threepeater/三线射手卡片.png',
                           'materials/Plants/Threepeater/Threepeater阴影.png', 18, 325, 7.5],
                          ['materials/Plants/TangleKlep/Float卡片.png',
                           'materials/Plants/TangleKlep/Float阴影.png', 19, 25, 30],
                          ['materials/Plants/Jalapeno/辣椒卡片.png',
                           'materials/Plants/Jalapeno/辣椒卡片阴影.png', 20, 125, 50],
                          ['materials/Plants/Spikeweed/Spikeweed卡片.png',
                           'materials/Plants/Spikeweed/Spikeweed阴影.png', 21, 100, 7.5],
                          ['materials/Plants/Torchwood/Torchwood卡片.png',
                           'materials/Plants/Torchwood/Torchwood阴影.png', 22, 175, 7.5],
                          ['materials/Plants/TallNut/TallNut卡片.png',
                           'materials/Plants/TallNut/TallNut阴影.png', 23, 125, 30],
                          ['materials/Plants/SeaShroom/SeaShroom卡片.png',
                           'materials/Plants/SeaShroom/SeaShroom阴影.png', 24, 0, 30],
                          ['materials/Plants/Plantern/Plantern卡片.png',
                           'materials/Plants/Plantern/Plantern阴影.png', 25, 25, 30],
                          ['materials/Plants/Cactus/Cactus卡片.png',
                           'materials/Plants/Cactus/Cactus阴影.png', 26, 125, 7.5],
                          ['materials/Plants/Blover/三叶草卡片.png',
                           'materials/Plants/Blover/三叶草卡片阴影.png', 27, 100, 7.5],
                          ['materials/Plants/SplitPea/SplitPea卡片.png',
                           'materials/Plants/SplitPea/SplitPea阴影.png', 28, 125, 7.5],
                          ['materials/Plants/Starfruit/Starfruit卡片.png',
                           'materials/Plants/Starfruit/Starfruit阴影.png', 29, 125, 7.5],
                          ['materials/Plants/PumpkinHead/PumpkinHead卡片.png',
                           'materials/Plants/PumpkinHead/PumpkinHead阴影.png', 30, 125, 30],
                          ['materials/Plants/FlowerPot/FlowerPot卡片.png',
                           'materials/Plants/FlowerPot/FlowerPot阴影.png', 31, 25, 7.5],
                          ['materials/Plants/CoffeeBean/Gralic卡片.png',
                           'materials/Plants/CoffeeBean/Gralic阴影.png', 32, 75, 7.5],
                          ['materials/Plants/Garlic/Garlic卡片.png',
                           'materials/Plants/Garlic/Garli阴影.png', 33, 50, 7.5],
                          ['materials/Plants/GatlingPea/GatlingPea钻石.png',
                           'materials/Plants/GatlingPea/机枪射手卡片阴影.png', 34, 3, 50],
                          ['materials/Plants/TwinSunflower/TwinSunflower卡片.png',
                           'materials/Plants/TwinSunflower/TwinSunflower阴影.png', 35, 225, 50],
                          ['materials/Plants/GloomShroom/GloomShroom卡片.png',
                           'materials/Plants/GloomShroom/GloomShroom阴影.png', 36, 150, 50],
                          ['materials/Plants/Spikerock/Spikerock卡片.png',
                           'materials/Plants/Spikerock/Spikerock阴影.png', 37, 225, 50],
                          ['materials/Plants/WallNut/坚果保龄球.png',
                           'materials/Plants/WallNut/坚果保龄球阴影.png', 38, 75, 30],
                          ['materials/Plants/WallNut/毁灭保龄球.png',
                           'materials/Plants/WallNut/毁灭保龄球阴影.png', 39, 175, 50],
                          ['materials/Plants/Imitator/模仿者卡片.png',
                           'materials/Plants/Imitator/模仿者卡片阴影.png', 40, 0, 7.5],
                          ]
        # 植物种植模型
        self.select_plant_list = [['materials/Plants/Peashooter/0.gif', (65, 75), 0],
                                  ['materials/Plants/SunFlower/0.gif', (65, 75), 0],
                                  ['materials/Plants/CherryBomb/0.gif', (68, 60), 0],
                                  ['materials/Plants/WallNut/0.gif', (65, 75), 0],
                                  ['materials/Plants/PotatoMine/0.gif', (65, 55), 0],
                                  ['materials/Plants/SnowPea/0.gif', (65, 75), 0],
                                  ['materials/Plants/Chomper/0.gif', (80, 75), 0],
                                  ['materials/Plants/Repeater/0.gif', (65, 75), 0],
                                  ['materials/Plants/PuffShroom/0.gif', (39, 45), 0],
                                  ['materials/Plants/SunShroom/0.gif', (52, 52), 0],
                                  ['materials/Plants/FumeShroom/0.gif', (80, 75), 0],
                                  ['materials/Plants/GraveBuster/0.gif', (80, 65), 0],
                                  ['materials/Plants/HypnoShroom/0.gif', (65, 75), 0],
                                  ['materials/Plants/ScaredyShroom/0.gif', (65, 75), 0],
                                  ['materials/Plants/IceShroom/0.gif', (75, 75), 0],
                                  ['materials/Plants/DoomShroom/0.gif', (85, 80), 0],
                                  ['materials/Plants/LilyPad/0.gif', (65, 55), 0],
                                  ['materials/Plants/Squash/0.gif', (65, 75), 0],
                                  ['materials/Plants/Threepeater/0.gif', (65, 75), 0],
                                  ['materials/Plants/TangleKlep/0.gif', (65, 60), 0],
                                  ['materials/Plants/Jalapeno/0.gif', (55, 75), 0],
                                  ['materials/Plants/Spikeweed/0.gif', (70, 35), 0],
                                  ['materials/Plants/Torchwood/0.gif', (65, 75), 0],
                                  ['materials/Plants/TallNut/0.gif', (96, 150), 0],
                                  ['materials/Plants/SeaShroom/0.gif', (39, 45), 0],
                                  ['materials/Plants/Plantern/0.gif', (80, 80), 0],
                                  ['materials/Plants/Cactus/0.gif', (80, 80), 0],
                                  ['materials/Plants/Blover/0.gif', (78, 90), 0],
                                  ['materials/Plants/SplitPea/0.gif', (80, 75), 0],
                                  ['materials/Plants/Starfruit/0.gif', (85, 85), 0],
                                  ['materials/Plants/PumpkinHead/0.gif', (90, 65), 0],
                                  ['materials/Plants/FlowerPot/0.gif', (65, 60), 0],
                                  ['materials/Plants/CoffeeBean/0.gif', (39, 45), 0],
                                  ['materials/Plants/Garlic/0.gif', (65, 75), 0],
                                  ['materials/Plants/GatlingPea/0.gif', (78, 90), 0],
                                  ['materials/Plants/TwinSunflower/0.gif', (78, 90), 0],
                                  ['materials/Plants/GloomShroom/0.gif', (91, 105), 0],
                                  ['materials/Plants/Spikerock/0.gif', (70, 35), 0],
                                  ['materials/Plants/WallNut/2.gif', (75, 85), -30],
                                  ['materials/Plants/WallNut/1.gif', (110, 110), -30],
                                  ['materials/Plants/Imitator/模仿者.gif', (65, 75), 0],]
    # *******************************************  植物卡片属性 **************************************************#
        self.plant_shadow = 'materials/Plants/plantshadow32.png'
        self._create_shadow_image_list()
        self.grow_soil_gif = 'materials/Plants/泥土飞起.gif'
        self._create_grow_soil_image_list()
        self.grow_water_gif = 'materials/Plants/水花飞起.gif'
        self._create_grow_water_image_list()

        # 向日葵
        self.sunflower_gif = 'materials/Plants/SunFlower/SunFlower.gif'
        self._create_sunflower_image_list()
        # 坚果墙
        self.potato_gif = 'materials/Plants/WallNut/WallNut.gif'
        self.potato_health_less_half_gif = 'materials/Plants/WallNut/Wallnut_cracked1.gif'
        self.potato_health_near_zero = 'materials/Plants/WallNut/Wallnut_cracked2.gif'
        self._create_potato_image_list()
        # 寒冰射手
        self.ice_shooter_gif = 'materials/Plants/SnowPea/SnowPea.gif'
        self._create_ice_shooter_image_list()
        # 豌豆射手
        self.pea_shooter_gif = 'materials/Plants/Peashooter/Peashooter.gif'
        self._create_pea_shooter_image_list()
        # 食人花
        self.man_eating_flower_gif = 'materials/Plants/Chomper/Chomper.gif'
        self.man_eating_flower_attack_gif = 'materials/Plants/Chomper/ChomperAttack.gif'
        self.man_eating_flower_eat_gif = 'materials/Plants/Chomper/ChomperDigest.gif'
        self._create_man_eating_flower_image_list()
        # 樱桃炸弹
        self.cherry_gif = 'materials/Plants/CherryBomb/CherryBomb.gif'
        self.cherry_boom_gif = 'materials/Plants/CherryBomb/Boom.gif'
        self._create_cherry_image_list()
        # 三叶草
        self.clover_gif = 'materials/Plants/Blover/Blover.gif'
        self._create_clover_image_list()
        # 机枪射手
        self.four_pea_gif = 'materials/Plants/GatlingPea/GatlingPea.gif'
        self._create_four_pea_shooter_image_list()
        # 三线射手
        self.three_pea_gif = 'materials/Plants/Threepeater/Threepeater.gif'
        self._create_three_pea_shooter_image_list()
        # 火爆辣椒
        self.pepper_gif = 'materials/Plants/Jalapeno/Jalapeno.gif'
        self.pepper_fire_gif = 'materials/Plants/Jalapeno/JalapenoAttack.gif'
        self._create_pepper_image_list()
    # ******************************************* 子弹属性 **************************************************#
        self.pea_max_distance = self.inner_screen_width * 0.7
        self.fire_distance = self.inner_screen_width * 0.7
        # 普通豌豆
        self.pea_gif = 'materials/bullets/pea.png'
        self.pea_broken = 'materials/bullets/pea_hit.gif'
        self._create_pea_bullet_image_list()
        self._create_broken_pea_bullet_image_list()
        # 寒冰豌豆
        self.ice_pea_gif = 'materials/bullets/ice_pea.png'
        self.ice_pea_to_frozen = 'materials/game_elements/寒冰射手冰冻效果.png'
        self._create_ice_pea_bullet_image_list()
        self._create_ice_image_list()
        # 火焰豌豆
        self.fire_pea_gif = 'materials/bullets/fire_pea.gif'
        self.fire_burn_list = ['materials/game_elements/fire1.png',
                               'materials/game_elements/fire1_1.png',
                               'materials/game_elements/fire1_2.png',
                               'materials/game_elements/fire1_3.png',
                               'materials/game_elements/fire2.png',
                               'materials/game_elements/fire3.png',
                               'materials/game_elements/fire4.png',
                               'materials/game_elements/fire4b.png',
                               'materials/game_elements/fire5.png',
                               'materials/game_elements/fire5b.png',
                               'materials/game_elements/fire6.png',
                               'materials/game_elements/fire6b.png',
                               'materials/game_elements/fire7.png',
                               'materials/game_elements/fire7b.png',
                               'materials/game_elements/fire8.png',]
        self._create_fire_pea_bullet_image_list()
        self._create_burning_fire_image_list()
    # ******************************************* 僵尸属性 **************************************************#
        self.appear_locations = [
            (self.inner_screen_width, self.screen_height * 0.278),
            (self.inner_screen_width, self.screen_height * 0.444),
            (self.inner_screen_width, self.screen_height * 0.622),
            (self.inner_screen_width, self.screen_height * 0.777),
            (self.inner_screen_width, self.screen_height * 0.948)]
        # 僵尸出土
        self.zombie_appear_soil_gif = 'materials/Zombies/BackupDancer/Mound.gif'
        self._create_zombie_appear_soil_image_list()
        # 普通僵尸
        self.general_zombie_static_gif = 'materials/Zombies/Zombie/0.gif'
        self.zombie_boom_gif = 'materials/Zombies/Zombie/BoomDie.gif'
        self.general_zombie1_gif = 'materials/Zombies/Zombie/1.gif'
        self.general_zombie2_gif = 'materials/Zombies/Zombie/2.gif'
        self.general_zombie3_gif = 'materials/Zombies/Zombie/3.gif'
        self.general_zombie_walk1_gif = 'materials/Zombies/Zombie/Zombie.gif'
        self.general_zombie_walk2_gif = 'materials/Zombies/Zombie/Zombie2.gif'
        self.general_zombie_walk3_gif = 'materials/Zombies/Zombie/Zombie3.gif'
        self.general_zombie_walk_without_head_gif = 'materials/Zombies/Zombie/ZombieLostHead.gif'
        self.general_zombie_shot_to_die_gif = 'materials/Zombies/Zombie/ZombieDie.gif'
        self.zombie_head_fall_gif = 'materials/Zombies/Zombie/ZombieHead.gif'
        self.zombie_attack_gif = 'materials/Zombies/Zombie/ZombieAttack.gif'
        self.zombie_attack_without_head_gif = 'materials/Zombies/Zombie/ZombieLostHeadAttack.gif'
        self._create_general_zombie_image_list()
        self._create_flying_head_image_list()
        # 旗子僵尸
        self.flag_zombie_static_gif = 'materials/Zombies/FlagZombie/0.gif'
        self.flag_zombie_gif = 'materials/Zombies/FlagZombie/1.gif'
        self.flag_zombie_walk_gif = 'materials/Zombies/FlagZombie/FlagZombie.gif'
        self.flag_zombie_attack_gif = 'materials/Zombies/FlagZombie/FlagZombieAttack.gif'
        self.flag_zombie_walk_without_head_gif = 'materials/Zombies/FlagZombie/FlagZombieLostHead.gif'
        self.flag_zombie_attack_without_head_gif = 'materials/Zombies/FlagZombie/FlagZombieLostHeadAttack.gif'
        self._create_flag_zombie_image_list()
        # 路障僵尸
        self.roadblock_zombie_static_gif = 'materials/Zombies/ConeheadZombie/0.gif'
        self.roadblock_zombie_gif = 'materials/Zombies/ConeheadZombie/1.gif'
        self.roadblock_zombie_walk_gif = 'materials/Zombies/ConeheadZombie/ConeheadZombie.gif'
        self.roadblock_zombie_attack_gif = 'materials/Zombies/ConeheadZombie/ConeheadZombieAttack.gif'
        self._create_roadblock_zombie_image_list()
        # 铁桶僵尸
        self.drum_zombie_static_gif = 'materials/Zombies/BucketheadZombie/0.gif'
        self.drum_zombie_gif = 'materials/Zombies/BucketheadZombie/1.gif'
        self.drum_zombie_walk_gif = 'materials/Zombies/BucketheadZombie/BucketheadZombie.gif'
        self.drum_zombie_attack_gif = 'materials/Zombies/BucketheadZombie/BucketheadZombieAttack.gif'
        self._create_drum_zombie_image_list()
        # 橄榄球僵尸
        self.football_zombie_static_gif = 'materials/Zombies/FootballZombie/0.gif'
        self.football_zombie_gif = 'materials/Zombies/FootballZombie/1.gif'
        self.football_zombie_walk_gif = 'materials/Zombies/FootballZombie/FootballZombie.gif'
        self.football_zombie_attack_in_armor_gif = 'materials/Zombies/FootballZombie/FootballZombieAttack.gif'
        self.football_zombie_attack_without_armor_gif = ('materials/Zombies/FootballZombie/FootballZombieOrnLos'
                                                         'tAttack.gif')
        self.football_zombie_run_without_head_gif = 'materials/Zombies/FootballZombie/LostHead.gif'
        self.football_zombie_attack_without_head_gif = 'materials/Zombies/FootballZombie/LostHeadAttack.gif'
        self.football_zombie_lost_armor_gif = 'materials/Zombies/FootballZombie/FootballZombieOrnLost.gif'
        self.football_zombie_shot_to_die_gif = 'materials/Zombies/FootballZombie/Die.gif'
        self.football_zombie_boom_gif = 'materials/Zombies/FootballZombie/BoomDie.gif'
        self._create_football_zombie_image_list()
        # 撑杆跳僵尸
        self.polevaulting_zombie_static_gif = 'materials/Zombies/PoleVaultingZombie/0.gif'
        self.polevaulting_zombie_gif = 'materials/Zombies/PoleVaultingZombie/1.gif'
        self.polevaulting_zombie_run_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombie.gif"
        self.polevaulting_zombie_run_without_head_gif = ('materials/Zombies/PoleVaultingZombie/PoleVaultingZombie'
                                                         'LostHead.gif')
        self.polevaulting_zombie_jump_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombieJump.gif"
        self.polevaulting_zombie_stand_on_ground_gif = ("materials/Zombies/PoleVaultingZombie/PoleVaultingZombie"
                                                        "Jump2.gif")
        self.polevaulting_zombie_walk_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombieWalk.gif"
        self.polevaulting_zombie_walk_without_head_gif = ("materials/Zombies/PoleVaultingZombie/PoleVaultingZombie"
                                                          "LostHeadWalk.gif")
        self.polevaulting_zombie_die_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombieDie.gif"
        self.polevaulting_zombie_head_fall_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombieHead.gif"
        self.polevaulting_zombie_eat_gif = "materials/Zombies/PoleVaultingZombie/PoleVaultingZombieAttack.gif"
        self.polevaulting_zombie_eat_without_head_gif = ("materials/Zombies/PoleVaultingZombie/PoleVaultingZombieLost"
                                                         "HeadAttack.gif")
        self.polevaulting_zombie_boom_gif = 'materials/Zombies/PoleVaultingZombie/BoomDie.gif'
        self._create_polevault_zombie_image_list()
        # 冰车僵尸
        self.ice_car_zombie_static_gif = 'materials/Zombies/Zomboni/0.gif'
        self.ice_car_zombie_gif = 'materials/Zombies/Zomboni/1.gif'
        self.ice_car_zombie_walk_gif = 'materials/Zombies/Zomboni/1.gif'
        self.ice_car_zombie_health_about_half_gif = 'materials/Zombies/Zomboni/2.gif'
        self.ice_car_zombie_health_about_zero_gif = 'materials/Zombies/Zomboni/3.gif'
        self.ice_car_zombie_stop_gif = 'materials/Zombies/Zomboni/4.gif'
        self.ice_car_zombie_explosion_gif = 'materials/Zombies/Zomboni/5.gif'
        self.ice_car_zombie_be_boom_gif = 'materials/Zombies/Zomboni/BoomDie.gif'
        self._create_ice_car_zombie_image_list()
        # 小鬼僵尸
        self.imp_zombie_static_gif = 'materials/Zombies/Imp/0.gif'
        self.imp_zombie_walk_gif = 'materials/Zombies/Imp/1.gif'
        self.imp_zombie_attack_gif = 'materials/Zombies/Imp/Attack.gif'
        self.imp_zombie_boom_gif = 'materials/Zombies/Imp/BoomDie.gif'
        self.imp_zombie_shot_to_die_gif = 'materials/Zombies/Imp/Die.gif'
        self._create_imp_zombie_image_list()
        # 小丑僵尸
        self.clown_zombie_static_gif = 'materials/Zombies/JackinTheBoxZombie/0.gif'
        self.clown_zombie_gif = 'materials/Zombies/JackinTheBoxZombie/1.gif'
        self.clown_zombie_walk_gif = 'materials/Zombies/JackinTheBoxZombie/Walk.gif'
        self.clown_zombie_walk_without_head_gif = 'materials/Zombies/JackinTheBoxZombie/LostHead.gif'
        self.clown_zombie_attack_gif = 'materials/Zombies/JackinTheBoxZombie/Attack.gif'
        self.clown_zombie_attack_without_head_gif = 'materials/Zombies/JackinTheBoxZombie/LostHeadAttack.gif'
        self.clown_zombie_was_scared_gif = 'materials/Zombies/JackinTheBoxZombie/OpenBox.gif'
        self.clown_zombie_explosion_gif = 'materials/Zombies/JackinTheBoxZombie/Boom.gif'
        self.clown_zombie_die_gif = 'materials/Zombies/JackinTheBoxZombie/Die.gif'
        self.clown_zombie_boom_gif = 'materials/Zombies/JackinTheBoxZombie/BoomDie.gif'
        self._create_clown_zombie_image_list()
        #  铁栅门僵尸
        self.screen_door_zombie_static_gif = 'materials/Zombies/ScreenDoorZombie/0.gif'
        self.screen_door_zombie_gif = 'materials/Zombies/ScreenDoorZombie/1.gif'
        self.screen_door_zombie_walk_gif = 'materials/Zombies/ScreenDoorZombie/HeadWalk1.gif'
        self.screen_door_zombie_attack_gif = 'materials/Zombies/ScreenDoorZombie/HeadAttack1.gif'
        self.screen_door_zombie_attack_without_head_gif = 'materials/Zombies/ScreenDoorZombie/LostHeadAttack1.gif'
        self.screen_door_zombie_walk_without_head_gif = 'materials/Zombies/ScreenDoorZombie/LostHeadAttack1.gif'
        self._create_screen_door_zombie_image_list()
        #  读报僵尸
        self.newspaper_zombie_static_gif = 'materials/Zombies/NewspaperZombie/0.gif'
        self.newspaper_zombie_gif = 'materials/Zombies/NewspaperZombie/1.gif'
        self.newspaper_zombie_walk_gif = 'materials/Zombies/NewspaperZombie/HeadWalk1.gif'
        self.newspaper_zombie_walk_without_head_gif = 'materials/Zombies/NewspaperZombie/LostHeadWalk1.gif'
        self.newspaper_zombie_walk_without_newspaper_gif = 'materials/Zombies/NewspaperZombie/HeadWalk0.gif'
        self.newspaper_zombie_walk_without_newspaper_and_head_gif = ('materials/Zombies/NewspaperZombie/LostHead'
                                                                     'Walk0.gif')
        self.newspaper_zombie_attack_gif = 'materials/Zombies/NewspaperZombie/HeadAttack1.gif'
        self.newspaper_zombie_attack_without_head_gif = 'materials/Zombies/NewspaperZombie/LostHeadAttack1.gif'
        self.newspaper_zombie_attack_without_newspaper_gif = 'materials/Zombies/NewspaperZombie/HeadAttack0.gif'
        self.newspaper_zombie_attack_without_newspaper_and_head_gif = ('materials/Zombies/NewspaperZombie/Lost'
                                                                       'HeadAttack0.gif')
        self.newspaper_zombie_doubt_gif = 'materials/Zombies/NewspaperZombie/LostNewspaper.gif'
        self.newspaper_zombie_was_shot_to_die_gif = 'materials/Zombies/NewspaperZombie/Die.gif'
        self.newspaper_zombie_head_fall_gif = 'materials/Zombies/NewspaperZombie/Head.gif'
        self.newspaper_zombie_boom_gif = 'materials/Zombies/NewspaperZombie/BoomDie.gif'
        self._create_newspaper_zombie_image_list()
        #  潜水僵尸
        self.snorkel_zombie_static_gif = 'materials/Zombies/SnorkelZombie/0.gif'
        self.snorkel_zombie_gif = 'materials/Zombies/SnorkelZombie/1.gif'
        self.snorkel_zombie_walk_in_land_gif = 'materials/Zombies/SnorkelZombie/Walk1.gif'
        self.snorkel_zombie_walk_in_river_gif = 'materials/Zombies/SnorkelZombie/Walk2.gif'
        self.snorkel_zombie_attack_in_river_gif = 'materials/Zombies/SnorkelZombie/Attack.gif'
        self.snorkel_zombie_jump_from_land_to_river_gif = 'materials/Zombies/SnorkelZombie/Jump.gif'
        self.snorkel_zombie_sink_gif = 'materials/Zombies/SnorkelZombie/Sink.gif'
        self.snorkel_zombie_risk_gif = 'materials/Zombies/SnorkelZombie/Risk.gif'
        self.snorkel_zombie_body_fall_gif = 'materials/Zombies/SnorkelZombie/Die.gif'
        self.snorkel_zombie_head_fall_gif = 'materials/Zombies/SnorkelZombie/Head.gif'
        self.snorkel_zombie_boom_gif = 'materials/Zombies/NewspaperZombie/BoomDie.gif'
        self._create_snorkel_zombie_image_list()
        # 海豚僵尸
        self.dolphin_rider_zombie_static_gif = 'materials/Zombies/DolphinRiderZombie/0.gif'
        self.dolphin_rider_zombie_gif = 'materials/Zombies/DolphinRiderZombie/1.gif'
        self.dolphin_rider_zombie_walk_in_land_with_dolphin_gif = "materials/Zombies/DolphinRiderZombie/Walk1.gif"
        self.dolphin_rider_zombie_walk_in_river_ride_dolphin_gif = 'materials/Zombies/DolphinRiderZombie/Walk2.gif'
        self.dolphin_rider_zombie_walk_in_river_without_dolphin_gif = 'materials/Zombies/DolphinRiderZombie/Walk3.gif'
        self.dolphin_rider_zombie_walk_in_land_without_dolphin_gif = 'materials/Zombies/DolphinRiderZombie/Walk4.gif'

        self.dolphin_rider_zombie_attack_in_river_without_dolphin_gif = ('materials/Zombies/DolphinRiderZombie/'
                                                                         'Attack.gif')
        self.dolphin_rider_zombie_throw_dolphin_gif = 'materials/Zombies/DolphinRiderZombie/Jump.gif'
        self.dolphin_rider_zombie_jump1_gif = 'materials/Zombies/DolphinRiderZombie/Jump2.gif'
        self.dolphin_rider_zombie_jump2_gif = 'materials/Zombies/DolphinRiderZombie/Jump3.gif'

        self.dolphin_rider_zombie_die_ride_dolphin_gif = 'materials/Zombies/DolphinRiderZombie/Die.gif'
        self.dolphin_rider_zombie_body_fall_water_gif = 'materials/Zombies/DolphinRiderZombie/Die2.gif'
        self.dolphin_rider_zombie_head_fall_gif = 'materials/Zombies/DolphinRiderZombie/Head.gif'
        self.dolphin_rider_zombie_boom_gif = 'materials/Zombies/NewspaperZombie/BoomDie.gif'
        self._create_dolphin_rider_zombie_image_list()
        # 鸭子铁桶僵尸
        self.ducky_drum_zombie_static_gif = 'materials/Zombies/DuckyTubeZombie3/0.gif'
        self.ducky_drum_zombie_gif = 'materials/Zombies/DuckyTubeZombie3/1.gif'
        self.ducky_drum_zombie_attack_with_armor_gif = 'materials/Zombies/DuckyTubeZombie3/Attack.gif'
        self.ducky_drum_zombie_attack_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Attack.gif'
        self.ducky_drum_zombie_walk_in_land_with_armor_gif = 'materials/Zombies/DuckyTubeZombie3/Walk1.gif'
        self.ducky_drum_zombie_walk_in_river_with_armor_gif = 'materials/Zombies/DuckyTubeZombie3/Walk2.gif'
        self.ducky_drum_zombie_walk_in_land_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Walk1.gif'
        self.ducky_drum_zombie_walk_in_river_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Walk2.gif'
        self.ducky_drum_zombie_was_shot_to_die_gif = 'materials/Zombies/DuckyTubeZombie1/Die.gif'
        self.ducky_drum_zombie_boom_gif = 'materials/Zombies/Zombie/BoomDie.gif'
        self._create_ducky_drum_zombie_image_list()
        # 鸭子路障僵尸
        self.ducky_roadblock_zombie_static_gif = 'materials/Zombies/DuckyTubeZombie2/0.gif'
        self.ducky_roadblock_zombie_gif = 'materials/Zombies/DuckyTubeZombie2/1.gif'
        self.ducky_roadblock_zombie_attack_with_armor_gif = 'materials/Zombies/DuckyTubeZombie2/Attack.gif'
        self.ducky_roadblock_zombie_attack_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Attack.gif'
        self.ducky_roadblock_zombie_walk_in_land_with_armor_gif = 'materials/Zombies/DuckyTubeZombie2/Walk1.gif'
        self.ducky_roadblock_zombie_walk_in_river_with_armor_gif = 'materials/Zombies/DuckyTubeZombie2/Walk2.gif'
        self.ducky_roadblock_zombie_walk_in_land_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Walk1.gif'
        self.ducky_roadblock_zombie_walk_in_river_without_armor_gif = 'materials/Zombies/DuckyTubeZombie1/Walk2.gif'
        self.ducky_roadblock_zombie_was_shot_to_die_gif = 'materials/Zombies/DuckyTubeZombie1/Die.gif'
        self.ducky_roadblock_zombie_boom_gif = 'materials/Zombies/Zombie/BoomDie.gif'
        self._create_ducky_roadblock_zombie_image_list()
        # 鸭子普通僵尸
        self.ducky_general_zombie_static_gif = 'materials/Zombies/DuckyTubeZombie1/0.gif'
        self.ducky_general_zombie_gif = 'materials/Zombies/DuckyTubeZombie1/1.gif'
        self.ducky_general_zombie_attack_in_river_gif = 'materials/Zombies/DuckyTubeZombie1/Attack.gif'
        self.ducky_general_zombie_walk_in_land_gif = 'materials/Zombies/DuckyTubeZombie1/Walk1.gif'
        self.ducky_general_zombie_walk_in_river_gif = 'materials/Zombies/DuckyTubeZombie1/Walk2.gif'
        self.ducky_general_zombie_was_shot_to_die_gif = 'materials/Zombies/DuckyTubeZombie1/Die.gif'
        self.ducky_general_zombie_boom_gif = 'materials/Zombies/Zombie/BoomDie.gif'
        self._create_ducky_general_zombie_image_list()
        # 舞王僵尸、
        self.dancing_zombie_light_png = 'materials/Zombies/DancingZombie/spotlight.png'
        self.dancing_zombie_light_shadow_png = 'materials/Zombies/DancingZombie/spotlight2.png'
        self.dancing_zombie_static_gif = 'materials/Zombies/DancingZombie/0.gif'
        self.dancing_zombie_gif = 'materials/Zombies/DancingZombie/SlidingStep.gif'
        self.dancing_zombie_enter_ground_gif = 'materials/Zombies/DancingZombie/SlidingStep.gif'
        self.dancing_zombie_enter_ground_without_head_gif = 'materials/Zombies/DancingZombie/LostHeadSlidingStep.gif'
        self.dancing_zombie_called_gif = 'materials/Zombies/DancingZombie/Summon.gif'
        self.dancing_zombie_called_without_head_gif = 'materials/Zombies/DancingZombie/LostHeadSummon.gif'

        self.dancing_zombie_sway_gif = 'materials/Zombies/DancingZombie/DancingZombie.gif'
        self.dancing_zombie_sway_without_head_gif = 'materials/Zombies/DancingZombie/LostHead.gif'
        self.dancing_zombie_dancing_gif = 'materials/Zombies/DancingZombie/Dancing.gif'
        self.dancing_zombie_dancing_without_head_gif = 'materials/Zombies/DancingZombie/LostHeadDancing.gif'
        self.dancing_zombie_attack_gif = 'materials/Zombies/DancingZombie/Attack.gif'
        self.dancing_zombie_attack_without_head_gif = 'materials/Zombies/DancingZombie/LostHeadAttack.gif'

        self.dancing_zombie_body_fall_gif = 'materials/Zombies/DancingZombie/Die.gif'
        self.dancing_zombie_head_fall_gif = 'materials/Zombies/DancingZombie/Head.gif'
        self.dancing_zombie_boom_gif = 'materials/Zombies/DancingZombie/BoomDie.gif'
        self._create_dancing_zombie_image_list()
        # 后援舞者僵尸
        self.backup_dancer_zombie_static_gif = 'materials/Zombies/BackupDancer/0.gif'
        self.backup_dancer_zombie_gif = 'materials/Zombies/BackupDancer/BackupDancer.gif'
        self.backup_dancer_zombie_sway_gif = 'materials/Zombies/BackupDancer/BackupDancer.gif'
        self.backup_dancer_zombie_dancing_gif = 'materials/Zombies/BackupDancer/Dancing.gif'
        self.backup_dancer_zombie_attack_gif = 'materials/Zombies/BackupDancer/Attack.gif'
        self.backup_dancer_zombie_sway_without_head_gif = 'materials/Zombies/BackupDancer/LostHead.gif'
        self.backup_dancer_zombie_dancing_without_head_gif = 'materials/Zombies/BackupDancer/LostHeadDancing.gif'
        self.backup_dancer_zombie_attack_without_head_gif = 'materials/Zombies/BackupDancer/LostHeadAttack.gif'
        self.backup_dancer_zombie_boom_gif = 'materials/Zombies/BackupDancer/BoomDie.gif'
        self.backup_dancer_zombie_body_fall_gif = 'materials/Zombies/BackupDancer/Die.gif'
        self.backup_dancer_zombie_head_fall_gif = 'materials/Zombies/BackupDancer/Head.gif'
        self._create_backup_dancer_zombie_image_list()
        #  静态僵尸列表
        self.zombie_static_attribute_list = [[[self.general_zombie1_gif,
                    self.general_zombie2_gif, self.general_zombie3_gif,], (130, 130), (130, 120), (-10, 125)],
                                [[self.flag_zombie_gif], (136, 130), (130, 120), (-10, 130)],
                                [[self.roadblock_zombie_gif], (136, 130), (130, 120),(-20, 125)],
                                [[self.drum_zombie_gif], (136, 130), (130, 120), (-5, 125)],
                                [[self.football_zombie_gif], (160, 145), (110, 140), (40, 143)],
                                [[self.polevaulting_zombie_gif], (290, 200), (270, 200), (0, 205)],
                                [[self.ice_car_zombie_gif], (420, 400), (400, 350), (15, 390)],
                                [[self.imp_zombie_walk_gif], (80, 120), (70, 100), (5, 125)],
                                [[self.clown_zombie_gif], (270, 270), (150, 150), (110, 180)],
                                [[self.screen_door_zombie_gif], (136, 130), (130, 120), (0, 125)],
                                [[self.newspaper_zombie_gif], (160, 135), (175, 140), (40, 135)],
                                [[self.snorkel_zombie_gif], (110, 170), (115, 170), (-5, 185)],
                                [[self.dolphin_rider_zombie_gif], (220, 220), (243, 198), (35, 223)],
                                [[self.ducky_general_zombie_gif], (136, 130), (130, 120), (-5, 130)],
                                [[self.ducky_roadblock_zombie_gif], (136, 130), (130, 120), (-5, 130)],
                                [[self.ducky_drum_zombie_gif], (136, 130), (130, 120), (-5, 125)],
                                [[self.dancing_zombie_gif], (150, 160), (150, 150), (-18, 165)]]
    # ****************************************** 僵尸道具属性 ******************************e*****************#
        self.ice_road = 'materials/game_elements/冰道.png'
        self.ice_road_head = 'materials/game_elements/冰道头.png'
        self._create_ice_road_image_list()
    # *******************************************  阳光属性 ************************************************#
        self.high_limit_x, self.low_limit_x = (800, 280)  # 阳光出现的横坐标位置
        self.high_limit_y = 500  # 阳光会掉落的y轴最远的的位置
        self.sun_speed = 1  # 阳光掉落速度
        self.collect_sun_speed = 15  # 阳光收集速度
        self.each_sunlight = 50
        self.start_sunlight = 50000  # 初始阳光
        self.sun = 'materials/Plants/Sun.gif'
        self.fall_sunlight_in_day = 15  # 阳光每设置的秒数落下一个
        self._create_sunlight_image_list()
    # ******************************************  游戏加载面板属性 ***********************************************#
        self.soil = 'materials/game_elements/LoadBar_dirt.png'
        self.grass = 'materials/game_elements/LoadBar_grass.png'
    # *******************************************  菜单按钮属性 **************************************************#
        self.pause_board = 'materials/game_elements/pause.png'
        self.menu = 'materials/game_elements/menu.png'
    # ******************************************* 主页属性 **************************************************#
        self.sunflower_trophy = 'materials/game_elements/Sunflower_trophy.png'
        self.mode_1 = 'materials/game_elements/冒险模式.png'
        self.mode_2 = 'materials/game_elements/迷你游戏.png'
        self.mode_3 = 'materials/game_elements/益智模式.png'
        self.mode_4 = 'materials/game_elements/解谜模式.png'
        self.mode_1_shadow = 'materials/game_elements/mode_1_shadow.png'
        self.mode234_shadow = 'materials/game_elements/mode234_shadow.png'
        self.option_light = 'materials/game_elements/Green_Option.png'
        self.help_light = 'materials/game_elements/Green_Help.png'
        self.quit_light = 'materials/game_elements/Green_Quit.png'
        self.garden_dark = 'materials/game_elements/GardenLowLight.png'
        self.garden_light = 'materials/game_elements/GardenHighLight.png'
        self.almanac_light = 'materials/game_elements/AlmanacHighLight.png'
        self.almanac_dark = 'materials/game_elements/AlmanacLowLight.png'
        self.store_light = 'materials/game_elements/StoreHighLight.png'
        self.store_dark = 'materials/game_elements/StoreLowLight.png'
        self.register_board = 'materials/game_elements/RegisterWoodBoard.png'
        self.save_board_light = 'materials/game_elements/SaveWoodBoardHighLight.png'
        self.save_board_dark = 'materials/game_elements/SaveWoodBoardLowLight.png'
        # 设置选项
        self.set_board = 'materials/game_elements/SetBoard.png'
        self.main_menu_back = 'materials/game_elements/返回主菜单按钮.png'
        self.game_view_back = 'materials/game_elements/返回游戏按钮.png'
        self.maker_list_button = 'materials/game_elements/制作者名单.png'
        self.goto_main_menu = 'materials/game_elements/返回主菜单小按钮.png'

        self.option_checkbox0 = 'materials/game_elements/options_checkbox0.png'
        self.option_checkbox1 = 'materials/game_elements/options_checkbox1.png'
        self.option_sliderknob2 = 'materials/game_elements/options_sliderknob2.png'
        self.option_sliderslot = 'materials/game_elements/options_sliderslot.png'
        # 帮助选项
        self.seed_button_light = 'materials/game_elements/主菜单亮.png'
        self.seed_button_dark = 'materials/game_elements/主菜单黑.png'
        self.help_content = 'materials/game_elements/Help.png'
        # 图鉴选项
        self.main_menu = 'materials/game_elements/MainButton.png'
        self.almanac_index = 'materials/game_elements/图鉴索引.png'
        self.check_plant_button_dark = 'materials/game_elements/查看植物黑.png'
        self.check_plant_button_light = 'materials/game_elements/查看植物亮.png'
        self.check_zombie_button = 'materials/game_elements/查看僵尸按钮.png'
        self.almanac_main_menu = 'materials/game_elements/图鉴关闭按钮.png'
        # 花园选项
        self.tool_container = 'materials/game_elements/tool_container.png'
        self.kettle = 'materials/game_elements/WateringCan.png'
        self.tree_food = 'materials/game_elements/TreeFood.png'
        self.bug_spray = 'materials/game_elements/BugSpray.png'
        self.phonograph = 'materials/game_elements/Phonograph.png'
        self.glove = 'materials/game_elements/Zen_GardenGlove.png'
        self.zen_money = 'materials/game_elements/Zen_MoneySign.png'
        self.zen_wheel_barrow = 'materials/game_elements/Zen_WheelBarrow.png'
        self.garden_store_dark = 'materials/game_elements/zenshopbutton.png'
        self.garden_store_light = 'materials/game_elements/zenshopbutton_highlight.png'
        self.tools = [self.kettle, self.tree_food, self.bug_spray, self.phonograph, self.glove, self.zen_money]
        self.next_garden = 'materials/game_elements/NextGarden.png'

    # *******************************************  小推车属性 **************************************************#
        self.tiny_grass_cleaner = 'materials/game_elements/LawnCleaner.png'
        self.tiny_pool_cleaner = 'materials/game_elements/icon_poolcleaner.png'
        self.tiny_roof_cleaner = 'materials/game_elements/icon_roofcleaner.png'
        self._create_tiny_car_image_list()
        self.car_coordinates = [(0, self.screen_height * 0.178),
                                (0, self.screen_height * 0.338),
                                (0, self.screen_height * 0.511),
                                (0, self.screen_height * 0.678),
                                (0, self.screen_height * 0.844)]
        self.start_location = self.inner_screen_width * 0.135
        self.car_limit = 5
        self.car_speed = 10
    # *******************************************  铲子和容器属性 **************************************************#
        self.container = 'materials/game_elements/container.png'
        self.shovel_bank = 'materials/game_elements/shovel_bank.png'
        self.shovel = 'materials/game_elements/shovel.png'
        self.sun_bank = 'materials/game_elements/SunBank.png'
    # *******************************************  视图按钮属性 **************************************************#
        self.check_view_button = 'materials/game_elements/check_view_button.png'
        self.left_eye = 'materials/game_elements/往左看.png'
        self.right_eye = 'materials/game_elements/往右看.png'
        self.reset_map_location = 'materials/game_elements/回归原位置.png'
        self.stop_the_location = 'materials/game_elements/停住视野.png'
    # *******************************************  选择框属性 **************************************************#
        self.choose_frame = 'materials/game_elements/choose_frame.png'
    # ******************************************* 音乐属性 **************************************************#
        self.wait = 'materials/game_music/game_in_waiting.mp3'
        self.wait_interval = 90  # 等待界面背景音乐每一播放时间间隔为90秒
        self.home_page_music = 'materials/game_music/Zombies_on_Your_Lawn.mp3'
        self.home_page_interval = 160
        self.choose_seed = 'materials/game_music/ChooseYourSeeds.mp3'
        self.choose_seed_interval = 22
        self.garden_zen = 'materials/game_music/garden_zen.mp3'
        self.garden_interval = 70
        self.game_start_musics = ['materials/game_music/Laura Shigihara - Brainiac Maniac.mp3',
                                  'materials/game_music/Laura Shigihara - Cerebrawl.mp3',
                                  'materials/game_music/Laura Shigihara - Graze the Roof.mp3',
                                  'materials/game_music/Laura Shigihara - Loonboon (1).mp3',
                                  'materials/game_music/Laura Shigihara - Grasswalk.mp3',
                                  'materials/game_music/Laura Shigihara - Moongrains IN-GAME.mp3',
                                  'materials/game_music/Laura Shigihara - Rigor Hormist.mp3',
                                  'materials/game_music/Laura Shigihara - Ultimate Battle.mp3',
                                  'materials/game_music/Laura Shigihara - Watery Graves.mp3',
                                  ]
        self.game_music_interval = [106, 121, 190, 121, 153, 196, 125, 120, 115]
    # ******************************************* 响声属性 **************************************************#
        self.big_chomp = 'materials/game_sound/bigchomp.ogg'
        self.button_click = 'materials/game_sound/buttonclick.mp3'
        self.car_collide = 'materials/game_sound/lawnmower.ogg'
        self.cherry_bomb = 'materials/game_sound/cherrybomb.mp3'
        self.clown_zombie_enter = 'materials/game_sound/小丑进场.ogg'
        self.clown_zombie_shout = 'materials/game_sound/小丑惊喜.ogg'
        self.clown_zombie_explode_sound = 'materials/game_sound/小丑爆炸.ogg'
        self.dirt_rise = 'materials/game_sound/dirt_rise.ogg'
        self.drum_zombie_was_hit = 'materials/game_sound/铁桶僵尸戴防具被击打.ogg'
        self.fire_pea = 'materials/game_sound/firepea.ogg'
        self.ice_car_enter = 'materials/game_sound/冰车进入.ogg'
        self.ice_car_explosion = 'materials/game_sound/冰车爆炸.ogg'
        self.ice_hit = 'materials/game_sound/寒冰打击声.ogg'
        self.mouse_pass = 'materials/game_sound/bleep.ogg'
        self.newspaper_zombie_excite = 'materials/game_sound/读报僵尸兴奋.ogg'
        self.pause = 'materials/game_sound/pause.mp3'
        self.pea_hit_sound = 'materials/game_sound/豌豆击中声.mp3'
        self.pea_shoot = 'materials/game_sound/豌豆发射声.ogg'
        self.pepper_burn = 'materials/game_sound/辣椒燃烧.ogg'
        self.pick_sunlight = 'materials/game_sound/points.mp3'
        self.plant_sound_in_grass = 'materials/game_sound/plant_in_grass.ogg'
        self.plant_sound_in_pool = 'materials/game_sound/plant_in_pool.ogg'
        self.pole_vault_jump = 'materials/game_sound/撑杆僵尸跳跃.ogg'
        self.roadblock_zombie_was_hit = 'materials/game_sound/路障僵尸戴帽子被击打音效.ogg'
        self.seed_choose = 'materials/game_sound/seedlift.mp3'
        self.shovel_back_sound = 'materials/game_sound/铲子归位.ogg'
        self.shovel_sound = 'materials/game_sound/shovel_sound.ogg'
        self.turn_book = 'materials/game_sound/paper.ogg'
        self.zombie_head_fly = 'materials/game_sound/僵尸头掉下.ogg'
        self.zombie_eat = 'materials/game_sound/chompsoft.ogg'
        self.zombie_eat_finish = 'materials/game_sound/gulp.ogg'
        self.zombie_enter_water = 'materials/game_sound/zombie_entering_water.mp3'

    def _load_and_get_image(self, file_path, image_width1=90, image_height1=80,
                            image_width2=90, image_height2=80, times=1, is_extend_list=False, is_smooth=False,
                            is_flip=False, horizontal=False, vertical=False):
        """"加载图片之后获取图片的每一帧"""
        image_list = []
        try:
            image = Image.open(file_path[0])
            while True:
                image.seek(len(image_list))  # 移动到指定帧，
                img = image.copy()  # 对指定的帧进行复制操纵
                img = img.convert("RGBA")  # 支持透明通道，即RGBA模式，没有它图像的第一帧会丢失
                pygame_image = pygame.image.fromstring(img.tobytes(), img.size, img.mode)  # 转换为pygame可识别的surface对象
                # 缩放Surface并显示
                pygame_image = (self._set_image_size_or_style
                                (pygame_image, image_width1, image_height1, is_smooth, is_flip, horizontal, vertical))
                image_list.append(pygame_image)
        except EOFError:
            pass
        if is_extend_list:  # 是否将第二个gif追加到第一个列表中
            temp_image_list = []
            image = Image.open(file_path[1])
            for _ in range(times):
                try:
                    while True:
                        image.seek(len(temp_image_list))  # 移动到指定帧，
                        img = image.copy()  # 对指定的帧进行复制操纵
                        img = img.convert("RGBA")  # 支持透明通道，即RGBA模式，没有它图像的第一帧会丢失
                        # 转换为pygame可识别的surface对象
                        pygame_image = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                        pygame_image = (self._set_image_size_or_style
                                        (pygame_image, image_width2, image_height2,
                                         is_smooth, is_flip, horizontal, vertical))  # 缩放Surface并显示
                        temp_image_list.append(pygame_image)
                except EOFError:
                    pass
                image_list.extend(temp_image_list)
                temp_image_list.clear()
        return image_list

    def _set_image_size_or_style(self, original_image, width=270, height=200, is_smooth=False,
                                 is_flip=False, horizontal=False, vertical=False):
        """设置每张图片的尺寸"""
        if not is_smooth:  # 没有选择平滑缩放
            image = pygame.transform.scale(original_image, (width, height))
        else:
            image = pygame.transform.smoothscale(original_image, (width, height))
        if is_flip:
            image = pygame.transform.flip(image, horizontal, vertical)  # 后面两个参数分别为水平反转， 垂直反转
        return image

    # ********************************************* 泳池图片加载  **********************************************
    def _create_pool_image_list(self):
        """创建泳池动画素材"""
        self.pool_day = self._load_and_get_image([self.pool_day_gif], 900, 176)
        self.pool_night = self._load_and_get_image([self.pool_night_gif], 900, 176)

    # ********************************************* 植物图片加载  **********************************************
    def _create_shadow_image_list(self):
        """创建阴影动画素材"""
        self.shadow = pygame.image.load(self.plant_shadow)

    def _create_grow_soil_image_list(self):
        """创建飞溅的泥土动画素材"""
        self.grow_soil = self._load_and_get_image([self.grow_soil_gif], image_width1=90, image_height1=30,
                                                  is_smooth=True)

    def _create_grow_water_image_list(self):
        """创建飞溅的水花动画素材"""
        self.grow_water = self._load_and_get_image([self.grow_water_gif],
                                                   90, 30, is_smooth=True)

    def _create_sunflower_image_list(self):
        """创建向日葵的动画素材"""
        self.sunflower_shake = self._load_and_get_image([self.sunflower_gif], image_width1=68, image_height1=168)

    def _create_ice_shooter_image_list(self):
        """创建寒冰射手的动画素材"""
        self.ice_shooter_shake = self._load_and_get_image([self.ice_shooter_gif],
                                                          image_width1=70, image_height1=70)

    def _create_pea_shooter_image_list(self):
        """创建豌豆射手的动画素材"""
        self.pea_shooter_shake = self._load_and_get_image([self.pea_shooter_gif],
                                                          image_width1=70, image_height1=70)

    def _create_man_eating_flower_image_list(self):
        """创建食人花的动画素材"""
        self.man_eating_flower_shake = self._load_and_get_image([self.man_eating_flower_gif],
                                                                image_width1=110, image_height1=100)
        self.man_eating_flower_attack = self._load_and_get_image([self.man_eating_flower_attack_gif],
                                                                image_width1=110, image_height1=100)
        self.man_eating_flower_rest = self._load_and_get_image([self.man_eating_flower_eat_gif],
                                                                image_width1=110, image_height1=100)

    def _create_potato_image_list(self):
        """创建小坚果的动画素材"""
        self.potato_shake = self._load_and_get_image([self.potato_gif],
                                               image_width1=75, image_height1=85)
        self.potato_half_health_shake = self._load_and_get_image([self.potato_health_less_half_gif],
                                               image_width1=75, image_height1=85)
        self.potato_zero_health_shake = self._load_and_get_image([self.potato_health_near_zero],
                                                                image_width1=75, image_height1=85)

    def _create_cherry_image_list(self):
        """创建樱桃炸弹的动画素材"""
        self.cherry_grown = self._load_and_get_image([self.cherry_gif, self.cherry_boom_gif],
            image_width1=110, image_height1=90, image_width2=300, image_height2=300, is_extend_list=True, times=3)

    def _create_clover_image_list(self):
        """创建豌豆射手的动画素材"""
        self.clover_shake = self._load_and_get_image([self.clover_gif],
                                                          image_width1=100, image_height1=100)

    def _create_four_pea_shooter_image_list(self):
        """创建机枪射手的动画素材"""
        self.four_pea_shooter_shake = self._load_and_get_image([self.four_pea_gif],
                                                          image_width1=75, image_height1=80)

    def _create_three_pea_shooter_image_list(self):
        """创建三线射手的动画素材"""
        self.three_pea_shooter_shake = self._load_and_get_image([self.three_pea_gif],
                                                          image_width1=75, image_height1=80)

    def _create_pepper_image_list(self):
        """创建火爆辣椒的动画素材"""
        self.pepper_grown = self._load_and_get_image([self.pepper_gif],
                                                          image_width1=80, image_height1=100)
        self.pepper_fire_burn = self._load_and_get_image([self.pepper_fire_gif],
                                                     image_width1=920, image_height1=90)

    # ********************************************* 小推车图片加载  **********************************************
    def _create_tiny_car_image_list(self):
        """创建小推车图片"""
        self.tiny_car_list = []
        image = pygame.image.load(self.tiny_grass_cleaner)
        self.tiny_car_list.append(self._set_image_size_or_style(image, 73, 60))
        image = pygame.image.load(self.tiny_pool_cleaner)
        self.tiny_car_list.append(self._set_image_size_or_style(image, 50, 60))
        image = pygame.image.load(self.tiny_roof_cleaner)
        self.tiny_car_list.append(self._set_image_size_or_style(image, 73, 60))

    # ********************************************* 僵尸图片加载  **********************************************
    def _create_flying_head_image_list(self):
        """创建飞翔的脑袋动画素材"""
        self.flying_head = self._load_and_get_image([self.zombie_head_fall_gif],
                                                    image_width1=120, image_height1=130)

    def _create_ice_road_image_list(self):
        """创建冰道素材"""
        image = pygame.image.load(self.ice_road)
        self.ice_road_image = self._set_image_size_or_style(image, 30, 70)
        image = pygame.image.load(self.ice_road_head)
        self.ice_road_head_image = self._set_image_size_or_style(image, 20, 70)

    def _create_zombie_appear_soil_image_list(self):
        """创建僵尸从地底出现时冒出的土壤"""
        self.zombie_appear_soil = self._load_and_get_image([self.zombie_appear_soil_gif],
                                                           100, 120, is_smooth=True)

    def _create_general_zombie_image_list(self):
        """创建普通僵尸的动画素材"""
        self.general_zombie_static = self._load_and_get_image([self.general_zombie_static_gif],
                                                                  130, 120)
        self.general_zombie_image_list = []
        # 普通僵尸原地摇摆形态
        zombie_walk1 = self._load_and_get_image([self.general_zombie1_gif],
                                                130, 120)
        zombie_walk2 = self._load_and_get_image([self.general_zombie2_gif],
                                                130, 120)
        zombie_walk3 = self._load_and_get_image([self.general_zombie3_gif],
                                                130, 120)
        self.general_zombie_image_list.append(zombie_walk1)
        self.general_zombie_image_list.append(zombie_walk2)
        self.general_zombie_image_list.append(zombie_walk3)
        self.general_zombie_walk_image_list = []
        # 普通僵尸行走形态
        zombie_walk1 = self._load_and_get_image([self.general_zombie_walk1_gif],
                                                            130, 120)
        zombie_walk2 = self._load_and_get_image([self.general_zombie_walk2_gif],
                                                130, 120)
        zombie_walk3 = self._load_and_get_image([self.general_zombie_walk3_gif],
                                                130, 120)
        self.general_zombie_walk_image_list.append(zombie_walk1)
        self.general_zombie_walk_image_list.append(zombie_walk2)
        self.general_zombie_walk_image_list.append(zombie_walk3)

        self.general_zombie_walk_without_head = self._load_and_get_image(
            [self.general_zombie_walk_without_head_gif, self.general_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.general_zombie_attack = self._load_and_get_image([self.zombie_attack_gif],
                                                              130, 120)
        self.general_zombie_attack_without_head = self._load_and_get_image([self.zombie_attack_without_head_gif,
                    self.zombie_attack_without_head_gif], 130, 120,
                    130, 120, is_extend_list=True, times=2)
        self.general_zombie_boom = self._load_and_get_image([self.zombie_boom_gif], image_width1=120,
                                                            image_height1=120)
        self.general_zombie_was_shot_to_die = self._load_and_get_image([self.general_zombie_shot_to_die_gif],
                                                            image_width1=130, image_height1=112)

    def _create_flag_zombie_image_list(self):
        """创建旗子僵尸的动画素材"""
        self.flag_zombie_static = self._load_and_get_image([self.flag_zombie_static_gif],
                                                                  130, 120)
        self.flag_zombie = self._load_and_get_image([self.flag_zombie_gif],
                                                    130, 120)
        self.flag_zombie_walk = self._load_and_get_image([self.flag_zombie_walk_gif],
                                                              130, 120)
        self.flag_zombie_walk_without_head = self._load_and_get_image(
            [self.flag_zombie_walk_without_head_gif, self.flag_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.flag_zombie_attack = self._load_and_get_image([self.flag_zombie_attack_gif],
                                                              130, 120)
        self.flag_zombie_attack_without_head = self._load_and_get_image([self.flag_zombie_attack_without_head_gif,
                    self.flag_zombie_attack_without_head_gif], 130, 120,
                    130, 120, is_extend_list=True, times=2)
        self.flag_zombie_boom = self._load_and_get_image([self.zombie_boom_gif], image_width1=120,
                                                            image_height1=120)
        self.flag_zombie_was_shot_to_die = self._load_and_get_image([self.general_zombie_shot_to_die_gif],
                                                            image_width1=130, image_height1=112)

    def _create_roadblock_zombie_image_list(self):
        """创建路障僵尸的动画素材"""
        self.roadblock_zombie_static = self._load_and_get_image([self.roadblock_zombie_static_gif],
                                                                  130, 120)
        self.roadblock_zombie = self._load_and_get_image([self.roadblock_zombie_gif],
                                                         130, 120)
        self.roadblock_zombie_walk_image_list = []
        zombie_walk1 = self._load_and_get_image([self.general_zombie_walk1_gif],
                                                130, 120)
        zombie_walk2 = self._load_and_get_image([self.general_zombie_walk2_gif],
                                                130, 120)
        zombie_walk3 = self._load_and_get_image([self.general_zombie_walk3_gif],
                                                130, 120)
        self.roadblock_zombie_walk_image_list.append(zombie_walk1)
        self.roadblock_zombie_walk_image_list.append(zombie_walk2)
        self.roadblock_zombie_walk_image_list.append(zombie_walk3)

        self.roadblock_zombie_walk_without_head = self._load_and_get_image(
            [self.general_zombie_walk_without_head_gif, self.general_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.roadblock_zombie_attack_without_head = self._load_and_get_image(
            [self.zombie_attack_without_head_gif, self.zombie_attack_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)

        self.roadblock_zombie_walk_with_armor = self._load_and_get_image([self.roadblock_zombie_walk_gif],
                                                                         image_width1=130, image_height1=112)
        self.roadblock_zombie_attack_with_armor = self._load_and_get_image([self.roadblock_zombie_attack_gif],

                                                            image_width1=130, image_height1=112)
        self.roadblock_zombie_attack_without_armor = self._load_and_get_image([self.zombie_attack_gif],
                                                            image_width1=130, image_height1=120)
        self.roadblock_zombie_boom = self._load_and_get_image([self.zombie_boom_gif], image_width1=120,
                                                            image_height1=120)
        self.roadblock_zombie_was_shot_to_die = self._load_and_get_image([self.general_zombie_shot_to_die_gif],
                                                            image_width1=130, image_height1=112)

    def _create_drum_zombie_image_list(self):
        """创建铁桶僵尸的动画素材"""
        self.drum_zombie_static = self._load_and_get_image([self.drum_zombie_static_gif],
                                                                  130, 120)
        self.drum_zombie = self._load_and_get_image([self.drum_zombie_gif],
                                                    130, 120)
        self.drum_zombie_walk_image_list = []
        zombie_walk1 = self._load_and_get_image([self.general_zombie_walk1_gif],
                                                130, 120)
        zombie_walk2 = self._load_and_get_image([self.general_zombie_walk2_gif],
                                                130, 120)
        zombie_walk3 = self._load_and_get_image([self.general_zombie_walk3_gif],
                                                130, 120)
        self.drum_zombie_walk_image_list.append(zombie_walk1)
        self.drum_zombie_walk_image_list.append(zombie_walk2)
        self.drum_zombie_walk_image_list.append(zombie_walk3)

        self.drum_zombie_walk_without_head = self._load_and_get_image(
            [self.general_zombie_walk_without_head_gif, self.general_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.drum_zombie_attack_without_head = self._load_and_get_image(
            [self.zombie_attack_without_head_gif, self.zombie_attack_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)

        self.drum_zombie_walk_with_armor = self._load_and_get_image([self.drum_zombie_walk_gif], image_width1=130,
                                                   image_height1=112)
        self.drum_zombie_attack_with_armor = self._load_and_get_image([self.drum_zombie_attack_gif],
                                                   image_width1=130, image_height1=112)
        self.drum_zombie_attack_without_armor = self._load_and_get_image([self.zombie_attack_gif],
                                                                  image_width1=130, image_height1=120)
        self.drum_zombie_boom = self._load_and_get_image([self.zombie_boom_gif], image_width1=120,
                                                   image_height1=120)
        self.drum_zombie_was_shot_to_die = self._load_and_get_image([self.general_zombie_shot_to_die_gif],
                                                            image_width1=130, image_height1=112)

    def _create_football_zombie_image_list(self):
        """创建橄榄球僵尸的动画素材"""
        self.football_zombie_static = self._load_and_get_image([self.football_zombie_static_gif],
                                                                  110, 140)
        self.football_zombie = self._load_and_get_image([self.football_zombie_gif],
                                                        110, 140)
        self.football_zombie_walk_with_armor = self._load_and_get_image([self.football_zombie_walk_gif],
                                                            image_width1=110, image_height1=140)
        self.football_zombie_attack_with_armor = self._load_and_get_image(
            [self.football_zombie_attack_in_armor_gif], image_width1=110, image_height1=140)
        self.football_zombie_walk_without_armor = self._load_and_get_image([self.football_zombie_lost_armor_gif],
                                            image_width1=110, image_height1=140)
        self.football_zombie_attack_without_armor = self._load_and_get_image(
            [self.football_zombie_attack_without_armor_gif], image_width1=110, image_height1=140)

        self.football_zombie_run_without_head = self._load_and_get_image([
            self.football_zombie_run_without_head_gif, self.football_zombie_run_without_head_gif],
            110, 140, 110, 140, is_extend_list=True, times=2)
        self.football_zombie_attack_without_head = self._load_and_get_image([
            self.football_zombie_attack_without_head_gif, self.football_zombie_attack_without_head_gif],
            110, 140, 110, 140, is_extend_list=True, times=2)

        self.football_zombie_boom = self._load_and_get_image([self.football_zombie_boom_gif], image_width1=130,
                                              image_height1=140)
        self.football_zombie_was_shot_to_die = self._load_and_get_image([self.football_zombie_shot_to_die_gif],
                                            image_width1=170, image_height1=170)

    def _create_polevault_zombie_image_list(self):
        """创建撑杆跳僵尸的动画素材"""
        self.pole_vault_zombie_static = self._load_and_get_image([self.polevaulting_zombie_static_gif],
                                                                  270, 200)
        self.pole_vault_zombie = self._load_and_get_image([self.polevaulting_zombie_gif],
                                                            270, 200)
        self.pole_vault_zombie_run = self._load_and_get_image([self.polevaulting_zombie_run_gif],
                                                    image_width1=270, image_height1=200)
        self.pole_vault_zombie_run_without_head = self._load_and_get_image([
            self.polevaulting_zombie_run_without_head_gif, self.polevaulting_zombie_run_without_head_gif],
            270, 200, 270, 200, is_extend_list=True, times=2)

        self.pole_vault_zombie_jump = self._load_and_get_image([self.polevaulting_zombie_jump_gif],
                                       image_width1=270, image_height1=200)
        self.pole_vault_zombie_fall = self._load_and_get_image([self.polevaulting_zombie_stand_on_ground_gif],
                                    image_width1=270, image_height1=200)
        self.pole_vault_zombie_walk = self._load_and_get_image([self.polevaulting_zombie_walk_gif],
                                    image_width1=270, image_height1=200)
        self.pole_vault_zombie_walk_without_head = self._load_and_get_image([
            self.polevaulting_zombie_walk_without_head_gif, self.polevaulting_zombie_walk_without_head_gif],
            270, 200, 270, 200, is_extend_list=True, times=2)

        self.pole_vault_zombie_attack = self._load_and_get_image([self.polevaulting_zombie_eat_gif],
                                                            image_width1=270, image_height1=200)
        self.pole_vault_zombie_attack_without_head = self._load_and_get_image([
            self.polevaulting_zombie_eat_without_head_gif, self.polevaulting_zombie_eat_without_head_gif],
            270, 200, 270, 200, is_extend_list=True, times=2)
        self.pole_vault_zombie_boom = self._load_and_get_image([self.polevaulting_zombie_boom_gif],
                                            image_width1=270, image_height1=200)
        self.pole_vault_zombie_body_fall = self._load_and_get_image([self.polevaulting_zombie_die_gif],
                                                                          image_width1=270, image_height1=200)
        self.pole_vault_zombie_head_fall = self._load_and_get_image([self.polevaulting_zombie_head_fall_gif],
                                                                    image_width1=270, image_height1=200)

    def _create_ice_car_zombie_image_list(self):
        """创建冰车僵尸的动画素材"""
        self.ice_car_zombie_static = self._load_and_get_image([self.ice_car_zombie_static_gif],
                                                                  400, 350)
        self.ice_car_zombie = self._load_and_get_image([self.ice_car_zombie_gif],
                                                       400, 350)
        self.ice_car_zombie_drive_full_health = self._load_and_get_image([self.ice_car_zombie_walk_gif],
                                                   image_width1=400, image_height1=350)
        self.ice_car_zombie_drive_half_health = self._load_and_get_image(
            [self.ice_car_zombie_health_about_half_gif], image_width1=400, image_height1=350)
        self.ice_car_zombie_drive_zero_health = self._load_and_get_image(
            [self.ice_car_zombie_health_about_zero_gif], image_width1=400, image_height1=350)
        self.ice_car_zombie_boom = self._load_and_get_image([self.ice_car_zombie_be_boom_gif], image_width1=400,
                                     image_height1=350)
        self.ice_car_zombie_was_shot_to_die = self._load_and_get_image([self.ice_car_zombie_stop_gif,
            self.ice_car_zombie_explosion_gif], image_width1=400, image_height1=350,
                                        image_width2=400, image_height2=350, is_extend_list=True)

    def _create_imp_zombie_image_list(self):
        """创建小鬼僵尸的动画素材"""
        self.imp_zombie_static = self._load_and_get_image([self.imp_zombie_static_gif],
                                                                  70, 100)
        self.imp_zombie_walk = self._load_and_get_image([self.imp_zombie_walk_gif],
                                                        70, 100)
        self.imp_zombie_attack = self._load_and_get_image([self.imp_zombie_attack_gif],
                                                          70, 100)
        self.imp_zombie_boom = self._load_and_get_image([self.imp_zombie_boom_gif],
                                                        70, 100)
        self.imp_zombie_was_shot_to_die = self._load_and_get_image([self.imp_zombie_shot_to_die_gif],
                                                                   70, 100)

    def _create_clown_zombie_image_list(self):
        """创建小丑僵尸的动画素材"""
        self.clown_zombie_zombie_static = self._load_and_get_image([self.clown_zombie_static_gif],
                                                                  150, 150)
        self.clown_zombie = self._load_and_get_image([self.clown_zombie_gif], 150, 150)
        self.clown_zombie_walk = self._load_and_get_image([self.clown_zombie_walk_gif],
                                                          150, 150,)

        self.clown_zombie_walk_without_head = self._load_and_get_image(
            [self.clown_zombie_walk_without_head_gif, self.clown_zombie_walk_without_head_gif],
            150, 150, 150, 150, is_extend_list=True, times=2)
        self.clown_zombie_attack = self._load_and_get_image([self.clown_zombie_attack_gif],
                                                              150, 150)

        self.clown_zombie_attack_without_head = self._load_and_get_image(
            [self.clown_zombie_attack_without_head_gif, self.clown_zombie_attack_without_head_gif],
            150, 150, 150, 150, is_extend_list=True, times=2)
        self.clown_zombie_boom = self._load_and_get_image([self.clown_zombie_boom_gif], image_width1=150,
                                                            image_height1=150)
        self.clown_was_scared = self._load_and_get_image([self.clown_zombie_was_scared_gif],
                                                         150, 150)
        self.clown_zombie_explode = self._load_and_get_image([self.clown_zombie_explosion_gif],
                                                          250, 250)
        self.clown_zombie_was_shot_to_die = self._load_and_get_image([self.clown_zombie_die_gif],
                                                                       image_width1=150, image_height1=150)

    def _create_screen_door_zombie_image_list(self):
        """创建铁栅门僵尸的动画素材"""
        self.screen_door_zombie_static = self._load_and_get_image([self.screen_door_zombie_static_gif],
                                                                  130, 120)
        self.screen_door_zombie = self._load_and_get_image([self.screen_door_zombie_gif],
                                                           130, 120)
        self.screen_door_zombie_walk = self._load_and_get_image([self.screen_door_zombie_walk_gif],
                                                          130, 120,)
        self.screen_door_zombie_walk_without_head = self._load_and_get_image(
            [self.screen_door_zombie_walk_without_head_gif, self.screen_door_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.screen_door_zombie_attack = self._load_and_get_image([self.screen_door_zombie_attack_gif],
                                                              130, 120)
        self.screen_door_zombie_attack_without_head = self._load_and_get_image(
            [self.screen_door_zombie_attack_without_head_gif, self.screen_door_zombie_attack_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)

        self.screen_door_zombie_walk_without_armor_image_list = []
        zombie_walk1 = self._load_and_get_image([self.general_zombie_walk1_gif],
                                                130, 120)
        zombie_walk2 = self._load_and_get_image([self.general_zombie_walk2_gif],
                                                130, 120)
        zombie_walk3 = self._load_and_get_image([self.general_zombie_walk3_gif],
                                                130, 120)
        self.screen_door_zombie_walk_without_armor_image_list .append(zombie_walk1)
        self.screen_door_zombie_walk_without_armor_image_list .append(zombie_walk2)
        self.screen_door_zombie_walk_without_armor_image_list .append(zombie_walk3)

        self.screen_door_attack_without_armor = self._load_and_get_image([self.zombie_attack_gif],
                                                          130, 120)
        self.screen_door_zombie_walk_without_armor_and_head = self._load_and_get_image(
            [self.general_zombie_walk_without_head_gif, self.general_zombie_walk_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.screen_door_zombie_attack_without_armor_and_head = self._load_and_get_image(
            [self.zombie_attack_without_head_gif, self.zombie_attack_without_head_gif],
            130, 120, 130, 120, is_extend_list=True, times=2)
        self.screen_door_zombie_was_shot_to_die = self._load_and_get_image(
            [self.general_zombie_shot_to_die_gif], image_width1=130, image_height1=120)
        self.screen_door_zombie_boom = self._load_and_get_image([self.zombie_boom_gif], image_width1=120,
                                                            image_height1=120)

    def _create_newspaper_zombie_image_list(self):
        """创建读报僵尸的动画素材"""
        self.newspaper_zombie_static = self._load_and_get_image([self.newspaper_zombie_static_gif],
                                                                175, 140)
        self.newspaper_zombie = self._load_and_get_image([self.newspaper_zombie_gif],
                                                            175, 140)
        self.newspaper_zombie_walk = self._load_and_get_image([self.newspaper_zombie_walk_gif],
                                                    image_width1=175, image_height1=140)
        self.newspaper_zombie_walk_without_head = self._load_and_get_image([
            self.newspaper_zombie_walk_without_head_gif, self.newspaper_zombie_walk_without_head_gif],
        175, 140, 175, 140, is_extend_list=True, times=2)

        self.newspaper_zombie_walk_without_newspaper = self._load_and_get_image(
            [self.newspaper_zombie_walk_without_newspaper_gif], image_width1=175, image_height1=140)
        self.newspaper_zombie_walk_without_newspaper_and_head = self._load_and_get_image(
            [self.newspaper_zombie_walk_without_newspaper_and_head_gif,
             self.newspaper_zombie_walk_without_newspaper_and_head_gif], image_width1=175, image_height1=140,
            image_width2=175, image_height2=140, is_extend_list=True, times=2)

        self.newspaper_zombie_attack = self._load_and_get_image([self.newspaper_zombie_attack_gif],
                                    image_width1=175, image_height1=140)
        self.newspaper_zombie_attack_without_head = self._load_and_get_image([
            self.newspaper_zombie_attack_without_head_gif, self.newspaper_zombie_attack_without_head_gif],
            175, 140, 175, 140, is_extend_list=True, times=2)

        self.newspaper_zombie_attack_without_newspaper = self._load_and_get_image(
            [self.newspaper_zombie_attack_without_newspaper_gif], image_width1=175, image_height1=140)
        self.newspaper_zombie_attack_without_newspaper_and_head = self._load_and_get_image([
            self.newspaper_zombie_attack_without_newspaper_and_head_gif,
            self.newspaper_zombie_attack_without_newspaper_and_head_gif],
            175, 140, 175, 140, is_extend_list=True, times=2)
        self.newspaper_zombie_doubt = self._load_and_get_image([self.newspaper_zombie_doubt_gif],
                                                               175, 140)

        self.newspaper_zombie_boom = self._load_and_get_image([self.newspaper_zombie_boom_gif],
                                            image_width1=175, image_height1=140)
        self.newspaper_zombie_body_fall = self._load_and_get_image([self.newspaper_zombie_was_shot_to_die_gif],
                                                                          image_width1=175, image_height1=140)
        self.newspaper_zombie_head_fall = self._load_and_get_image([self.newspaper_zombie_head_fall_gif],
                                                                    image_width1=175, image_height1=140)

    def _create_snorkel_zombie_image_list(self):
        """创建潜水僵尸的动画素材"""
        self.snorkel_zombie_static = self._load_and_get_image([self.snorkel_zombie_static_gif],
                                                                  115, 170)
        self.snorkel_zombie = self._load_and_get_image([self.snorkel_zombie_gif],
                                                            115, 170)
        self.snorkel_zombie_walk_in_land = self._load_and_get_image([self.snorkel_zombie_walk_in_land_gif],
                                                    image_width1=115, image_height1=170)
        self.snorkel_zombie_walk_in_river = self._load_and_get_image([self.snorkel_zombie_walk_in_river_gif],
        115, 170, )

        self.snorkel_zombie_attack_in_river = self._load_and_get_image([self.snorkel_zombie_attack_in_river_gif],
                                       image_width1=115, image_height1=170)
        self.snorkel_zombie_jump = self._load_and_get_image([self.snorkel_zombie_jump_from_land_to_river_gif],
                                    image_width1=115, image_height1=170)
        self.snorkel_zombie_sink = self._load_and_get_image([self.snorkel_zombie_sink_gif],
                                    image_width1=115, image_height1=170)
        self.snorkel_zombie_risk = self._load_and_get_image([self.snorkel_zombie_risk_gif],
            115, 170, )

        self.snorkel_zombie_body_fall = self._load_and_get_image([self.snorkel_zombie_body_fall_gif],
                                                            image_width1=115, image_height1=170)
        self.snorkel_zombie_head_fall = self._load_and_get_image([self.snorkel_zombie_head_fall_gif],
            115, 170, )
        self.snorkel_zombie_boom = self._load_and_get_image([self.snorkel_zombie_boom_gif],
                                            image_width1=175, image_height1=140)

    def _create_dolphin_rider_zombie_image_list(self):
        """创建海豚僵尸的动画素材"""
        self.dolphin_rider_zombie_static = self._load_and_get_image([self.dolphin_rider_zombie_static_gif],
                                                           243, 198)
        self.dolphin_rider_zombie = self._load_and_get_image([self.dolphin_rider_zombie_gif],
                                                     243, 198)
        self.dolphin_rider_zombie_walk_in_land_with_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_walk_in_land_with_dolphin_gif], 243, 198)
        self.dolphin_rider_zombie_walk_in_river_ride_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_walk_in_river_ride_dolphin_gif],
            243, 198)
        self.dolphin_rider_zombie_walk_in_river_without_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_walk_in_river_without_dolphin_gif], 243, 198)
        self.dolphin_rider_zombie_walk_in_land_without_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_walk_in_land_without_dolphin_gif], 243, 198)
        self.dolphin_rider_zombie_attack_in_river_without_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_attack_in_river_without_dolphin_gif], 243, 198)
        self.dolphin_rider_zombie_throw_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_throw_dolphin_gif], 243, 198)
        self.dolphin_rider_zombie_jump = self._load_and_get_image(
            [self.dolphin_rider_zombie_jump1_gif, self.dolphin_rider_zombie_jump2_gif],
            243, 198, 243, 198, is_extend_list=True, times=1)
        self.dolphin_rider_zombie_die_on_dolphin = self._load_and_get_image(
            [self.dolphin_rider_zombie_die_ride_dolphin_gif, self.dolphin_rider_zombie_die_ride_dolphin_gif],
            243, 198,  243, 198, is_extend_list=True, times=1)
        self.dolphin_rider_zombie_body_fall_water = self._load_and_get_image(
            [self.dolphin_rider_zombie_body_fall_water_gif], 243, 198)
        self.dolphin_rider_zombie_head_fall = self._load_and_get_image(
            [self.dolphin_rider_zombie_head_fall_gif], 117, 180)
        self.dolphin_rider_zombie_boom = self._load_and_get_image(
            [self.dolphin_rider_zombie_boom_gif], image_width1=175, image_height1=140)

    def _create_ducky_drum_zombie_image_list(self):
        """创建鸭子铁桶僵尸的动画素材"""
        self.ducky_drum_zombie_static = self._load_and_get_image([self.ducky_drum_zombie_static_gif],
                                                                  130, 120)
        self.ducky_drum_zombie = self._load_and_get_image([self.ducky_drum_zombie_gif],
             130, 120)

        self.ducky_drum_zombie_walk_in_land_with_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_walk_in_land_with_armor_gif], 130, 120
        )
        self.ducky_drum_zombie_walk_in_river_with_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_walk_in_river_with_armor_gif], image_width1=130, image_height1=112)
        self.ducky_drum_zombie_walk_in_land_without_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_walk_in_land_without_armor_gif], 130, 120)
        self.ducky_drum_zombie_walk_in_river_without_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_walk_in_river_without_armor_gif], 130, 120
        )

        self.ducky_drum_zombie_attack_with_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_attack_with_armor_gif], image_width1=130, image_height1=112)

        self.ducky_drum_zombie_attack_without_armor = self._load_and_get_image(
            [self.ducky_drum_zombie_attack_without_armor_gif], image_width1=130, image_height1=120)

        self.ducky_drum_zombie_boom = self._load_and_get_image(
            [self.ducky_drum_zombie_boom_gif], image_width1=120, image_height1=120)

        self.ducky_drum_zombie_was_shot_to_die = self._load_and_get_image(
            [self.ducky_drum_zombie_was_shot_to_die_gif], image_width1=130, image_height1=112)

    def _create_ducky_roadblock_zombie_image_list(self):
        """创建鸭子路障僵尸的动画素材"""
        self.ducky_roadblock_zombie_static = self._load_and_get_image([self.ducky_roadblock_zombie_static_gif],
                                                                 130, 120)
        self.ducky_roadblock_zombie = self._load_and_get_image([self.ducky_roadblock_zombie_gif],
                                                          130, 120)

        self.ducky_roadblock_zombie_walk_in_land_with_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_walk_in_land_with_armor_gif], 130, 120
        )
        self.ducky_roadblock_zombie_walk_in_river_with_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_walk_in_river_with_armor_gif], image_width1=130, image_height1=112)
        self.ducky_roadblock_zombie_walk_in_land_without_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_walk_in_land_without_armor_gif], 130, 120)
        self.ducky_roadblock_zombie_walk_in_river_without_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_walk_in_river_without_armor_gif], 130, 120
        )

        self.ducky_roadblock_zombie_attack_with_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_attack_with_armor_gif], image_width1=130, image_height1=112)

        self.ducky_roadblock_zombie_attack_without_armor = self._load_and_get_image(
            [self.ducky_roadblock_zombie_attack_without_armor_gif], image_width1=130, image_height1=120)

        self.ducky_roadblock_zombie_boom = self._load_and_get_image(
            [self.ducky_roadblock_zombie_boom_gif], image_width1=120, image_height1=120)

        self.ducky_roadblock_zombie_was_shot_to_die = self._load_and_get_image(
            [self.ducky_roadblock_zombie_was_shot_to_die_gif], image_width1=130, image_height1=112)

    def _create_ducky_general_zombie_image_list(self):
        """创建鸭子普通僵尸的动画素材"""
        self.ducky_general_zombie_static = self._load_and_get_image(
            [self.ducky_general_zombie_static_gif], 130, 120)
        self.ducky_general_zombie = self._load_and_get_image(
            [self.ducky_general_zombie_gif], 130, 120)

        self.ducky_general_zombie_walk_in_land = self._load_and_get_image(
            [self.ducky_general_zombie_walk_in_land_gif], 130, 120)
        self.ducky_general_zombie_walk_in_river = self._load_and_get_image(
            [self.ducky_general_zombie_walk_in_river_gif], 130, 120
        )
        self.ducky_general_zombie_attack = self._load_and_get_image(
            [self.ducky_general_zombie_attack_in_river_gif], image_width1=130, image_height1=120)

        self.ducky_general_zombie_boom = self._load_and_get_image(
            [self.ducky_general_zombie_boom_gif], image_width1=120, image_height1=120)

        self.ducky_general_zombie_was_shot_to_die = self._load_and_get_image(
            [self.ducky_general_zombie_was_shot_to_die_gif], image_width1=130, image_height1=112)

    def _create_dancing_zombie_image_list(self):
        """创建舞王僵尸的动画素材"""
        # image = pygame.image.load(self.dancing_zombie_light_png)
        # self.dancing_zombie_light = self._set_image_size_or_style(image, 400, 594)
        # image = pygame.image.load(self.dancing_zombie_light_shadow_png)
        # self.dancing_zombie_light_shadow = self._set_image_size_or_style(image, 400, 50)

        self.dancing_zombie_static = self._load_and_get_image(
            [self.dancing_zombie_static_gif], 150, 150)
        self.dancing_zombie = self._load_and_get_image(
            [self.dancing_zombie_gif], 150, 150)

        self.dancing_zombie_enter_ground = self._load_and_get_image(
            [self.dancing_zombie_enter_ground_gif], 150, 150,
            is_flip=True, horizontal=True)
        self.dancing_zombie_enter_ground_without_head = self._load_and_get_image(
            [self.dancing_zombie_enter_ground_without_head_gif], 140, 160,
            is_flip=True, horizontal=True)

        self.dancing_zombie_called = self._load_and_get_image(
            [self.dancing_zombie_called_gif], 150, 150)
        self.dancing_zombie_called_without_head = self._load_and_get_image(
            [self.dancing_zombie_called_without_head_gif], 150, 150)

        self.dancing_zombie_sway = self._load_and_get_image(
            [self.dancing_zombie_sway_gif], 150, 150)
        self.dancing_zombie_sway_without_head = self._load_and_get_image(
            [self.dancing_zombie_sway_without_head_gif], 150, 150)

        self.dancing_zombie_attack = self._load_and_get_image(
            [self.dancing_zombie_attack_gif], 150, 150)
        self.dancing_zombie_attack_without_head = self._load_and_get_image(
            [self.dancing_zombie_attack_without_head_gif], 150, 150)

        self.dancing_zombie_dancing = self._load_and_get_image(
            [self.dancing_zombie_dancing_gif], 150, 150)
        self.dancing_zombie_dancing_without_head = self._load_and_get_image(
            [self.dancing_zombie_dancing_without_head_gif], 150, 150)

        self.dancing_zombie_body_fall = self._load_and_get_image(
            [self.dancing_zombie_body_fall_gif], 150, 150)
        self.dancing_zombie_head_fall = self._load_and_get_image(
            [self.dancing_zombie_head_fall_gif], 150, 150)
        self.dancing_zombie_boom = self._load_and_get_image(
            [self.dancing_zombie_boom_gif], 150, 150)

    def _create_backup_dancer_zombie_image_list(self):
        """创建后援舞者僵尸的动画素材"""
        self.backup_dancer_zombie_static = self._load_and_get_image(
            [self.backup_dancer_zombie_static_gif], 100, 120)
        self.backup_dancer_zombie = self._load_and_get_image(
            [self.backup_dancer_zombie_gif], 100, 120)
        self.backup_dancer_zombie_sway = self._load_and_get_image(
            [self.backup_dancer_zombie_sway_gif], 100, 120)
        self.backup_dancer_zombie_dancing = self._load_and_get_image(
            [self.backup_dancer_zombie_dancing_gif], 100, 120)
        self.backup_dancer_zombie_attack = self._load_and_get_image(
            [self.backup_dancer_zombie_attack_gif], 100, 120)
        self.backup_dancer_zombie_sway_without_head = self._load_and_get_image(
            [self.backup_dancer_zombie_sway_without_head_gif], 100, 120)
        self.backup_dancer_zombie_dancing_without_head = self._load_and_get_image(
            [self.backup_dancer_zombie_dancing_without_head_gif], 100, 120)
        self.backup_dancer_zombie_attack_without_head = self._load_and_get_image(
            [self.backup_dancer_zombie_attack_without_head_gif], 100, 120)
        self.backup_dancer_zombie_body_fall = self._load_and_get_image(
            [self.backup_dancer_zombie_body_fall_gif], 160, 110)
        self.backup_dancer_zombie_head_fall = self._load_and_get_image(
            [self.backup_dancer_zombie_head_fall_gif], 100, 120)
        self.backup_dancer_zombie_boom = self._load_and_get_image(
            [self.backup_dancer_zombie_boom_gif], 130, 120)
        
    # ********************************************* 子弹图片加载  **********************************************
    def _create_pea_bullet_image_list(self):
        """创建豌豆子弹素材"""
        self.pea_bullet = self._load_and_get_image([self.pea_gif], image_width1=30, image_height1=30,
                                                   is_smooth=True)

    def _create_broken_pea_bullet_image_list(self):
        """创建破碎豌豆子弹素材"""
        self.broken_pea_bullet = []
        image = pygame.image.load(self.pea_broken)
        pygame_image = self._set_image_size_or_style(image, 40, 40)  # 缩放Surface并显示
        self.broken_pea_bullet.append(pygame_image)

    def _create_ice_pea_bullet_image_list(self):
        """创建寒冰豌豆子弹素材"""
        self.ice_pea_bullet = self._load_and_get_image([self.ice_pea_gif], image_width1=30, image_height1=30,
                                                       is_smooth=True)

    def _create_ice_image_list(self):
        """创建寒冰豌豆子弹素材"""
        self.ice = []
        image = pygame.image.load(self.ice_pea_to_frozen)
        pygame_image = self._set_image_size_or_style(image, 60, 40)
        self.ice.append(pygame_image)

    def _create_fire_pea_bullet_image_list(self):
        """创建火焰豌豆子弹素材"""
        # 小型火焰豌豆
        self.fire_pea_bullet1 = self._load_and_get_image([self.fire_pea_gif], image_width1=68, image_height1=40,
                                                    is_smooth=True)
        # 大型火焰豌豆
        self.fire_pea_bullet2 = self._load_and_get_image([self.fire_pea_gif], image_width1=85, image_height1=50,
                                                        is_smooth=True)

    def _create_burning_fire_image_list(self):
        """创建燃烧的火焰素材"""
        self.burning_fire = []
        for image in self.fire_burn_list:
            image = pygame.image.load(image)
            pygame_image = self._set_image_size_or_style(image, 60, 20)
            self.burning_fire.append(pygame_image)

    # ********************************************* 道具图片加载  **********************************************

    def _create_sunlight_image_list(self):
        """创建阳光素材"""
        self.sunlight = self._load_and_get_image([self.sun], image_width1=76, image_height1=76)
