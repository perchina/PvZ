import pygame


class Radio:
    """"这是一个音频播放"""
    def __init__(self, ai_game):
        """音频播放方法"""
        self.setting = ai_game.setting
        self.sound_scale = 1  # 响声大小默认设置为一，即最大音量

    def adjust_music_high_or_low(self, scale):
        """根据比例调整游戏背景音乐大小"""
        pygame.mixer.music.set_volume(scale)

    def check_music_is_pause(self):
        """检测音乐是否正在播放"""
        if not pygame.mixer.music.get_busy():
            # 如果音乐正在播放就返回真，如果暂停播放，就返回真；而在这里是如果被暂停就返回真， 如果未被暂停就返回假
            return True
        return False

    def play_short_time_sound(self, sound):
        """播放指定的声音"""
        music = pygame.mixer.Sound(sound)
        music.set_volume(self.sound_scale)
        music.play()

    def play_music(self, music):
        """"播放指定音乐"""
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

    def pause_play_music(self):
        """暂停音乐"""
        pygame.mixer.music.pause()

    def unpause_play_music(self):
        """继续播放音乐"""
        pygame.mixer.music.unpause()

    def stop_play_music(self):
        """立即停止音乐"""
        pygame.mixer.music.stop()


