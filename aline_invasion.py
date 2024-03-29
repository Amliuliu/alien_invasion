import sys
from time import sleep
import pygame
from settings import Settings
from game_status import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from random import randint
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
        pygame.display.set_caption(f"Alien Invasion {game_version}")   
        
        #创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        #将主程序中生成的实例传递给Ship，所以Ship类中定义的ai_game才具有主程序实例中的所有属性(重要，否则无法在ship中调取主函数生成的显示界面相应的属性)
        self.ship = Ship(self)   
        
        #创建存储子弹的编组，该编组为pygame.sprite.Group()类生成的一个实例
        self.bullets = pygame.sprite.Group()

        #创建外星人编组
        self.aliens = pygame.sprite.Group()
        
        #创建外星人
        self._creat_fleet()  #因为外星人不需要使用按键指令生成，所以此处直接进行创建
        
        #创建开始按钮
        self.play_button = Button(self,"Play")
        
        #创建得分板
        self.sb = Scoreboard(self)

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
            self._fire_bullet()  #按K开火
        elif event.key == pygame.K_p:
            self._start_game()   #按p开始游戏

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

    def _check_play_botton(self,mouse_pos):
        '''在玩家鼠标单机开始键时才开始游戏'''
        if self.play_button.rect.collidepoint(mouse_pos): #rect属性的collidepoint()方法用于判定输入位置是否在当前rect坐标位置范围内(非常重要)
            self._start_game()

    def _check_events(self):
        '''响应按键和鼠标事件（重要）'''
        for event in pygame.event.get():  #获取用户输入事件
            if event.type == pygame.QUIT: #判断用户输入事件
                sys.exit()                #退出游戏   
            elif event.type == pygame.KEYDOWN:   #判断按键按下事件
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:     #判断按键弹起事件
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() #pygame.mouse.get_pos()返回一个元组，包含鼠标点击时的x，y坐标
                self._check_play_botton(mouse_pos)

    def _start_game(self):
        '''开始游戏'''
        if self.stats.game_active == False: #只有在游戏状态为False（即游戏结束时），才可以使用以下重置指令
            #重置游戏信息
            self.stats.reset_stats()  #重置飞船次数，得分，游戏等级
            self.sb.game_level()      #游戏等级更新
            self.stats.game_active = True  #重置开始标记
            self.sb.ship_life()      #飞船生命图像更新
            
            #重置飞船，外星人，子弹速度，基础分数
            self.settings.initialize_dynamic_settings() 
            self.sb.prep_score() #重置基础分数后需要进行刷新显示，否则下一次游戏开始后，在子弹撞击外星人之前分数将不会被更新回默认状态

            #清空余下外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新外星人,并将飞船放到初始位置
            self._creat_fleet()
            self.ship.center_ship()

            #开始游戏后隐藏鼠标
            pygame.mouse.set_visible(False)  #在游戏开始时初始化游戏等级

            #暂停1s
            sleep(0.5)       


    def _fire_bullet(self):
        '''创建一颗子弹，将其加入编组当中'''

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) #创建子弹
            self.bullets.add(new_bullet) #将使用Bullet()类创建的精灵加入编组

    def _update_bullets(self):
        '''更新子弹状态和删除消失的子弹'''
        
        #对编组调用update(),编组对其中每个精灵调用update(),用以更新所有子弹精灵的状态
        self.bullets.update()          

        #删除消失的子弹
        #执行for循环时使用的列表元素不能发生改变，故需要使用该编组的副本进行遍历，然后删除掉符合要求的对应元素即可
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        '''碰撞检测和新外星人生成'''
        self._check_bullet_alien_collisions()
        
    
    def _check_bullet_alien_collisions(self):
        '''碰撞检测和新外星人生成'''

        #碰撞检测，如果检测到碰撞的子弹和外星人则删除对象，并将删除的对象存在字典collisions中，True/False则代表检测到碰撞后是否需要删除还是保留该对象
        #如果一颗子弹同时击中多个外星人，则该键值对的键为子弹，值为当前所有击中的外星人生成的列表
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)    
        
        #击中后得分
        if collisions:
            for aliens in collisions.values():  #获取所有外星人（键值对的值）
                self.stats.score += self.settings.alien_points * len(aliens) #计算击杀的外星人分数  
                self.sb.prep_score() #获取分数后将当前值调用prep_score()生成分数图像
                self.sb.check_high_score()  #检查当前得分是否为最高分，若是则更新最高分 
        
        #一轮外星人被射杀完后创建一批新的外星人
        if not self.aliens: #检查编组是否为空
            self.bullets.empty()  #使用empty()方法清空编组
            self._creat_fleet()  #重新创建外星人
            self.settings.increase_speed() #游戏等级属性提升
            self.sb.check_game_level() #游戏等级提升

    def _creat_fleet(self):
        '''创建外星人群'''
        alien = Alien(self) #此处alien实例只是用于参数定义使用 
        alien_width,alien_height = alien.rect.size #获取外星人宽度和高度
        
        #计算屏幕可生成多少列外星人
        available_space_x = self.settings.screen_width - (2*alien_width)  #可生成外星人x区域
        number_aliens_x = available_space_x // (2*alien_width)  #可生成x列
        
        #计算屏幕可生成多少行外星人
        ship_height = self.ship.rect.height   #飞船高度
        available_space_y = self.settings.screen_height - 3*alien_height - ship_height  #可生成外星人y区域
        number_aliens_y = available_space_y // (2*alien_height)  #可生成Y行

        #创建外星人群(x,y方向同时建立)
        for alien_y in range(number_aliens_y):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number,alien_y)

    def _creat_alien(self,alien_number,alien_y):
        '''创建一个外星人阵列'''
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size #获取外星人宽度和高度

        alien.x = alien_width+2*alien_width*alien_number #每次循环时新生成的外星人x坐标依次改变
        alien.y = alien_height+2*alien_height*alien_y #每次循环时新生成的外星人y坐标改变

        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''检查编组中的外星人是否位于边缘'''
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''外星人位于边缘时，行为做以下处理'''
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''响应飞船被外星人撞到或者外星人到达屏幕底端事件'''
        if self.stats.ships_left > 0:
            #将ships_left减1
            self.stats.ships_left -= 1
            
            #清空剩余外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            #飞船生命图像更新
            self.sb.ship_life()      

            #创建一群新外星人,并将飞船放到初始位置
            self._creat_fleet()
            self.ship.center_ship()

            #暂停1s
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            print("您的角色已死亡，游戏结束！！！")

    def _check_aliens_bottom(self):
        '''检查外星人是否到达屏幕底端'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #与飞船被撞一样处理
                self._ship_hit()
                break

    def _update_alien(self):
        '''
        1.检查外星人是否处于边缘状态并做出相应行为处理
        2.更新外新人位置
        '''
        self._check_fleet_edges()
        self.aliens.update()
        
        #检测外星人与飞船的碰撞事件
        #spritecollideany()方法检测精灵和编组成员之间的碰撞事件，其形参顺序不能任意改变，如果未发生碰撞则该方法返回None值，后续代码不会执行
        #如果找到了与精灵发生碰撞的编组成员则返回该成员
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查外星人是否到达屏幕底端
        self._check_aliens_bottom()
        
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

        #绘制得分，飞船剩余生命
        self.sb.show_score()

        #在绘制完成其他元素后再绘制按钮，才可以使得按钮再图像最顶层
        if self.stats.game_active == False:
            self.play_button.draw_button()

        #让最近绘制的屏幕可见-屏幕事件刷新方法flip()
        pygame.display.flip() 
    
    def run_game(self):
        '''开始游戏主循环'''
        while True:  #对于对象一定要记住先更新状态再更新图像，最后刷新画面
            #检测按键和鼠标输入事件
            self._check_events()

            # #屏幕颜色填充效果，不进行设置时运行游戏将在_update_screen()中调用默认背景颜色
            # self.screen_color() 
            
            if self.stats.game_active:
                '''游戏结束时部分功能禁止运行-即当游戏处于非活跃状态时，可以不用更新游戏元素位置'''
                
                #飞船位置状态更新-只包含相关属性，不进行生成，生成功能在_update_scerrn中定义
                self.ship.update()
                
                #子弹状态更新和删除消失的子弹(自动生成子弹动画)-只包含相关属性，不进行生成，生成功能在_update_scerrn中定义
                self._update_bullets() 

                #入侵外星人位置状态更新
                self._update_alien()
            
            #执行更新画面
            self._update_screen()


if __name__ == '__main__':
    '''当执行文件为当前文件时，才开始运行游戏'''
    ai = AlienInvasion()   #创建游戏实例
    ai.run_game()          #运行游戏




































