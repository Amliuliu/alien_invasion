import sys
import pygame
from settings import Settings
from ship import Ship
from random import randint
from bullet import Bullet
game_version = "Ver 1.0.0" #创建游戏

class AlineInvasion:
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()   #初始化游戏模块

        #不添加Setting设置类模块前的代码：参数与主程序未分开
        # self.screen_size = [1000,800]      #也可以直接使用元组固定显示窗口大小   
        # self.screen = pygame.display.set_mode(self.screen_size) #创建游戏窗口
        # self.bg_color = [0,100,230]     #设置背景颜色属性

        #添加Setting设置类后的代码：参数与主程序已完全分离
        self.settings = Settings()  #获取setting类相关设置
        
        #设置显示界面大小
        self.screen_size = [
                            self.settings.screen_width,
                            self.settings.screen_height,
                            ]    
        
        #全屏显示
        # self.screen = pygame.display.set_mode([0,0],pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # #按照设定值生成显示区域
        self.screen = pygame.display.set_mode(self.screen_size) 
        
        #设置界面显示颜色
        self.bg_color = [
                        self.settings.bg_color_r,
                        self.settings.bg_color_g,
                        self.settings.bg_color_b,
                        ]   

        #创建游戏说明
        pygame.display.set_caption(f"Aline Invasion {game_version}")   
        
        #将主程序中生成的实例传递给Ship，所以Ship类中定义的ai_game才具有主程序实例中的所有属性(重要，否则无法在ship中调取主函数生成的显示界面相应的属性)
        self.ship = Ship(self)   
        
        #创建存储子弹的编组
        self.bullets = pygame.sprite.Group()  
    
    def screen_color(self):
        ''' 设置背景颜色随机改变+延时'''    
        self.bg_color[0] = randint(0,255)
        self.bg_color[1] = randint(0,255)
        self.bg_color[2] = randint(0,255)
        
        for number in range(1,10000000): 
            ""  

    def _check_keydown_events(self,event): #必须使用event形参输入，否则代码块中的event会出现未定义情况
        '''判断按键按下事件'''
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = True       
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True 
        #该按q退出指令只能在英文输入法或大写锁定开启下才能进行
        elif event.key == pygame.K_q:  
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        '''判断按键弹起事件'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False   

    def _fire_bullet(self):
        '''创建一颗子弹，将其加入编组当中'''
        new_bullet = Bullet(self) #创建子弹
        self.bullets.add(new_bullet) #加入编组

    def _check_events(self):
        '''响应按键和鼠标事件（重要）'''
        for event in pygame.event.get():  #获取用户输入事件
            if event.type == pygame.QUIT: #判断用户输入事件
                sys.exit()                #退出游戏   
            elif event.type == pygame.KEYDOWN:   #判断按键按下事件
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:     #判断按键弹起事件
                self._check_keyup_events(event)
    
    def _update_screen(self):
        '''更新显示界面'''
        #背景颜色填充-fill()方法
        self.screen.fill(self.bg_color) 
        
        #生成飞船
        self.ship.blitme()

        #生成编组内每颗子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #让最近绘制的屏幕可见-屏幕事件刷新方法flip()
        pygame.display.flip() 
    
    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            # self.screen_color() #背景颜色变更
            self.ship.update()
            self.bullets.update() #对编组调用update(),编组自动对其中每个对象调用update()
            self._update_screen()

if __name__ == '__main__':
    '''当执行文件为当前文件时，才开始运行游戏'''
    ai = AlineInvasion()
    ai.run_game()


















