import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''创建外星人的类'''
    
    def __init__(self,ai_game):
        '''初始化外星人'''
        super().__init__()
        self.screen = ai_game.screen
        
        # #以下外星人位置代码不需要使用游戏窗口rect属性，注销
        # self.screen_rect = ai_game.screen.get_rect()

        #加载外星人图形并获取rect属性
        self.image = pygame.image.load('C:/Users/六六/Desktop/python_work/part2_project/alien_invasion/images/alien.png').convert()   #图片尺寸
        self.rect = self.image.get_rect()   #获取操作对象形状尺寸

        #外星人起始位置(距离屏幕左上角一个飞船距离)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人的水平位置
        self.x = float(self.rect.x)






