import sys
import pygame
from settings import Settings
from ship import Ship
from random import randint
from bullet import Bullet
from alien import Alien
game_version = "Ver 1.0.0" #创建游戏

class AlienInvasion:
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()   #初始化游戏模块

        #不添加Setting设置类模块前的代码：参数与主程序未分开-原始代码可以删除-注销代码0.0.0
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
        
        #创建存储子弹的编组，该编组为pygame.sprite.Group()类生成的一个实例
        self.bullets = pygame.sprite.Group()

        #创建外星人编组
        self.aliens = pygame.sprite.Group()
        #创建外星人
        self._creat_fleet()  #因为外星人不需要使用按键指令生成，所以此处直接进行创建
        
        #子弹添加连续射击使能初始化-注销代码1.0.0
        # self.fire_bullet = False   
    
    def screen_color(self):
        ''' 设置背景颜色随机改变'''  
        self.bg_color[0] = randint(0,255)
        self.bg_color[1] = randint(0,255)
        self.bg_color[2] = randint(0,255)

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
            #-注销代码1.0.0
            # self.fire_bullet = True
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
        #-注销代码1.0.0
        # elif event.key == pygame.K_SPACE:
        #     self.fire_bullet = False 

    def _fire_bullet(self):
        '''创建一颗子弹，将其加入编组当中'''
        # if self.fire_bullet == True:  #按下空格连续创建子弹--注销代码1.0.0
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) #创建子弹
            self.bullets.add(new_bullet) #将使用Bullet()类创建的精灵加入编组

    def _update_bullets(self):
        '''更新子弹状态和删除消失的子弹'''
        
        #生成子弹精灵--注销代码1.0.0
        # self._fire_bullet()
        
        #对编组调用update(),编组对其中每个精灵调用update(),用以更新所有子弹精灵的状态
        self.bullets.update()          

        #删除消失的子弹
        #执行for循环时使用的列表元素不能发生改变，故需要使用该编组的副本进行遍历，然后删除掉符合要求的对应元素即可
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_events(self):
        '''响应按键和鼠标事件（重要）'''
        for event in pygame.event.get():  #获取用户输入事件
            if event.type == pygame.QUIT: #判断用户输入事件
                sys.exit()                #退出游戏   
            elif event.type == pygame.KEYDOWN:   #判断按键按下事件
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:     #判断按键弹起事件
                self._check_keyup_events(event)
    
    def _creat_fleet(self):
        '''创建外星人群'''
        # 创建一个外星人
        alien = Alien(self)
        self.aliens.add(alien)
    

    def _update_screen(self):
        '''更新显示界面'''
        #背景颜色填充
        self.screen.fill(self.bg_color) 
        
        #绘制飞船
        self.ship.blitme()

        #绘制编组内每颗子弹
        for bullet in self.bullets.sprites(): #bullet.sprites()方法返回一个包含所有被创建的精灵的列表
            bullet.draw_bullet()

        #使用draw()方法将存储在编组aliens中的外星人在屏幕中画出
        self.aliens.draw(self.screen) #self.screen指绘制的surface

        #让最近绘制的屏幕可见-屏幕事件刷新方法flip()
        pygame.display.flip() 
    
    def run_game(self):
        '''开始游戏主循环'''
        while True:  #对于对象一定要记住先更新状态再更新图像，最后刷新画面
            #检测按键和鼠标输入事件
            self._check_events()
            
            # #屏幕颜色填充效果，不进行设置时运行游戏将在_update_screen()中调用默认背景颜色
            # self.screen_color() 
            
            #飞船位置状态更新-只包含相关属性，不进行生成，生成功能在_update_scerrn中定义
            self.ship.update()
            
            #子弹状态更新和删除消失的子弹(自动生成子弹动画)-只包含相关属性，不进行生成，生成功能在_update_scerrn中定义
            self._update_bullets() 
            
            #执行更新画面
            self._update_screen()


if __name__ == '__main__':
    '''当执行文件为当前文件时，才开始运行游戏'''
    ai = AlienInvasion()
    ai.run_game()


















