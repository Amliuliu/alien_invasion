import pygame
#from settings import Settings 因为在__init__()函数中的ai_game形参被赋予的是main函数的实例，
#所以具有main函数实例的一切属性，所以不需要在进行Setting类导入也可以直接调用相关属性（非常重要，有助于理解各模块代码之间的联系）
class Ship:
    '''管理飞船的类'''
    def __init__(self,ai_game):    #ai_game来自于main函数的实例
        '''初始化飞船并设置其初始位置'''
        self.screen = ai_game.screen   #获取游戏窗口
        self.screen_rect = ai_game.screen.get_rect()  #获取游戏窗口形状尺寸

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('C:/Users/六六/Desktop/python_work/part2_project/alien_invasion/images/ship.png').convert()   #图片尺寸
        self.rect = self.image.get_rect()   #获取操作对象形状尺寸

        #对于每艘飞船，都将其放在屏幕底部中央
        # self.rect.midleft = self.screen_rect.midleft #其他位置设置
        # self.rect.midtop = self.screen_rect.midtop
        # self.rect.midright = self.screen_rect.midright
        # self.rect.center = self.screen_rect.center
        self.rect.midbottom = self.screen_rect.midbottom  #对象在窗口生成的位置

        self.settings = ai_game.settings  #调用Settings类中的属性，后续会使用其中的速度设置参数
        
        self.x = float(self.rect.x) #使用属性x存储小数值（self.rect.x属性只能存储整数，导致设置的带有小数位的速度等参数无法计算）
        self.y = float(self.rect.y) 

        self.moving_right = False #初始化移动设置，不进行移动
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self): 
        '''操作对象移动'''
        #使用if语句而不是if-else语句可以解决按键优先级导致的bug  
        #使用边界检测条件共同配合限制对象移动范围在屏幕界面内
        if self.moving_right and self.rect.right < self.screen_rect.right:   
            self.x += self.settings.ship_speed                    
        if self.moving_left and self.rect.left > 0:       
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #将移动结果传递给对象位置变量进行更新
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        '''在指定位置绘制(生成)飞船'''
        self.screen.blit(self.image,self.rect)     #生成可操作对象

