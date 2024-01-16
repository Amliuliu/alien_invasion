import pygame.font   #该模块可将文本渲染到文本上

class Button:
    '''定义按钮'''
    def __init__(self,ai_game,msg):
        '''初始化按钮属性'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.button_color = [0,255,0]
        self.text_color = [255,255,255]
        self.font = pygame.font.SysFont(None,48) #指定字体字号来渲染文本，None指默认字体，48指字号

        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        #按钮标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        '''将msg渲染为图像并使其在按钮中居中'''
        #font.render()方法将文本渲染为图像，True/False指定是否开启抗锯齿，最后两个参数为文本颜色和文本背景色，文本背景色没有指定时，python渲染文本将使用透明背景
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color) 
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''绘制按钮和文本''' 
        #以下两种创建按钮的方法可以任选其一
        self.screen.fill(self.button_color,self.rect)        
        # pygame.draw.rect(self.screen,self.button_color,self.rect)
        
        self.screen.blit(self.msg_image,self.msg_image_rect)     






