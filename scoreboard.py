import pygame.font

class Scoreboard:
    '''显示得分信息的类'''
    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #显示得分信息时的字体设置
        
