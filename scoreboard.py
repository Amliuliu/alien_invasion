import pygame.font #该模块可将文本渲染到文本上

from pygame.sprite import Group  #创建飞船编组，导入Group类
from ship import Ship  #创建飞船编组，导入Ship类

class Scoreboard:
    '''显示得分信息的类'''
    
    def __init__(self,ai_game):
        self.ai_game = ai_game #将游戏实例赋予属性，后续需要使用游戏实例来生成飞船编组
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #显示得分信息时的字体设置
        self.text_color = [0,255,0]  #得分字体颜色
        
        self.font = pygame.font.SysFont(None,48) #指定字体字号来渲染文本，None指默认字体，48指字号,为当前类的全局变量

        #显示最高得分的颜色设置，字体设置跟随得分文本字体的全局设置
        self.high_score_text_color = [255,0,0]  #最高分字体颜色

        #显示游戏等级颜色设置
        self.game_level_text_color = [0,0,255]  #游戏等级字体颜色

        #得分图像
        self.prep_score()

        #最高分图像
        self.high_score_update()

        #游戏等级图像
        self.game_level()

        #创建用于表示飞船生命的图像
        self.ship_life()

    def high_score_update(self):
        '''最高分转换为图像'''
        
        round_high_score = round(self.stats.high_score,-1) 
        high_score_str = "{:,}".format(round_high_score)
        self.high_score_str_image = self.font.render(f"High Score:{high_score_str}",True,self.high_score_text_color,
                                                    (self.settings.bg_color_r,
                                                    self.settings.bg_color_g,
                                                    self.settings.bg_color_b) )
        
        #将最高分位置放置在右上角
        self.high_score_str_image_rect = self.high_score_str_image.get_rect()
        self.high_score_str_image_rect.right = self.screen_rect.right - 20
        self.high_score_str_image_rect.top = 20

    def check_high_score(self):
        '''检查是否获得最高分'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.high_score_update()

    def prep_score(self):
        '''将得分转换为图像'''
        
        #round()函数通常用于控制小数精确到某一位，精确位数通常由第二个实参指定，但第二个实参为负数时，将会把这个数舍入到最近的整数
        round_score = round(self.stats.score,-1) 
        
        #使用字符串格式设置指令，使其在数字转化为字符串时在中间插入","  --以后可能用到
        score_str = "{:,}".format(round_score)
        
        self.score_str_image = self.font.render(f"Score:{score_str}",True,self.text_color,
                                                    (self.settings.bg_color_r,
                                                    self.settings.bg_color_g,
                                                    self.settings.bg_color_b) )
        
        #将得分位置放置在右上角
        self.score_str_image_rect = self.score_str_image.get_rect()
        self.score_str_image_rect.right = self.screen_rect.right - 20
        self.score_str_image_rect.top = self.score_str_image_rect.height +30

    def game_level(self):
        '''游戏等级转化为图像'''

        game_level = self.stats.level
        game_level_str = "{:,}".format(game_level)
        self.game_level_str_image = self.font.render(f"Game Level:{game_level_str}",True,self.game_level_text_color,
                                                    (self.settings.bg_color_r,
                                                    self.settings.bg_color_g,
                                                    self.settings.bg_color_b) )

        #将最高分位置放置在中上
        self.game_level_str_image_rect = self.game_level_str_image.get_rect()
        self.game_level_str_image_rect.centerx = self.screen_rect.centerx
        self.game_level_str_image_rect.top = 20

    def check_game_level(self):
        '''游戏等级更新'''
        self.stats.level += 1
        self.game_level()

    def ship_life(self):
        '''创建用于表示飞船生命的编组'''
        self.ships = Group() #创建一个编组
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game) #使用游戏实例创建飞船
            ship.rect.x = 20 + ship_number * ship.rect.width
            ship.rect.y = 20   #生成飞船的位置
            self.ships.add(ship) #将创建的飞船实例存入编组中

    def show_score(self):
        '''绘制图像'''
        #绘制得分图像
        self.screen.blit(self.score_str_image,self.score_str_image_rect) 
        #绘制最高分图像
        self.screen.blit(self.high_score_str_image,self.high_score_str_image_rect) 
        #绘制游戏等级图像
        self.screen.blit(self.game_level_str_image,self.game_level_str_image_rect)
        #绘制编组内的所有精灵
        self.ships.draw(self.screen) 





