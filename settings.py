class Settings:
    '''存储游戏《外星人入侵》所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        
        #一般属性，游戏运行期间不进行改变
        #屏幕设置
        self.screen_width = 1400 #游戏窗口宽度
        self.screen_height =800  #游戏窗口高度
        self.bg_color_r = 0      #游戏窗口颜色
        self.bg_color_g = 0
        self.bg_color_b = 0
        
        #飞船设置
        self.ship_limit = 3      #飞船数量限制  

        #子弹设置
        self.bullet_width = 3    #子弹宽度
        self.bullet_height = 10  #子弹长度
        self.bullet_color = [255,0,0] #子弹颜色
        self.bullets_allowed = 10 #生成子弹数量限制
        
        #外星人设置
        self.fleet_drop_speed = 10 #外星人纵向移动速度

        #加快游戏速度的设置
        self.speedup_scale = 1.1

        #得分提高速度
        self.score_scale = 1.5

        #部分在游戏重新开始时需要初始化的属性
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed = 0.5    #飞船速度设置
        self.bullet_speed = 0.5  #子弹速度
        self.alien_speed = 0.1  #外星人横向移动速度
        self.fleet_direction = 1  #外星人左右移动标记，1为右，-1为左
        self.alien_points = 50   #计分

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale    #飞船速度提升
        self.bullet_speed *= self.speedup_scale  #子弹速度提升
        self.alien_speed *= self.speedup_scale  #外星人横向移动速度提升
        self.alien_points = int(self.alien_points * self.score_scale)  #计分提升


        



















