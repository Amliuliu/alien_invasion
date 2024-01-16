import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''创建外星人的类'''
    
    def __init__(self,ai_game):
        '''初始化外星人'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载外星人图形并获取rect属性
        self.image = pygame.image.load('C:/Users/六六/Desktop/python_work/part2_project/alien_invasion/images/alien.png').convert()   #图片尺寸
        self.rect = self.image.get_rect()   #获取操作对象形状尺寸

        #外星人起始位置(距离屏幕左上角一个飞船距离)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人的水平&纵向位置
        self.x = float(self.rect.x)
        self.y=  float(self.rect.y)

    def check_edges(self):
        '''检测外星人移动是否超过屏幕边缘并变更移动方向'''
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:   
            return True
            
    def update(self):
        '''外星人横向位置变更'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        







