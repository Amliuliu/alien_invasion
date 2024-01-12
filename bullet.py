import pygame
#from settings import Settings 因为在__init__()函数中的ai_game形参被赋予的是main函数的实例，
#所以具有main函数实例的一切属性，所以不需要在进行Setting类导入也可以直接调用相关属性（非常重要，有助于理解各模块代码之间的联系）
from pygame.sprite import Sprite   #使用精灵

class Bullet(Sprite):
    '''创建子弹类'''
    def __init__(self,ai_game):
        '''初始化，在飞船当前位置创建一个子弹对象'''
        super().__init__()
        self.screen = ai_game.screen   #获取游戏窗口
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #在[0,0]处创建一个表示子弹的矩形
        #因为子弹没有来自于图像，所以需要使用pygame.Rect()方法进行从头创建
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)

        #将创建的子弹位置与创建的ship实例位置绑定
        self.rect.midtop = ai_game.ship.rect.midtop 
        
        #存储子弹位置给属性y
        self.y = float(self.rect.y)


    def update(self):
        '''向上移动子弹'''
        #更新表示子弹位置的属性y的值
        self.y -= self.settings.bullet_speed

        #更新子弹的rect.y属性
        self.rect.y = self.y

    def draw_bullet(self):
        '''绘制子弹'''
        pygame.draw.rect(self.screen,self.color,self.rect) #三个参数分别代表(1)要绘制的surface（2）要绘制的颜色（3）要绘制的矩形的位置和尺寸

