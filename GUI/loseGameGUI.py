import pygame
from .setting import *
from database import ConnectDatabase

class lose:
    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.position_x = width_screen_game * 1.0
        self.position_y = height_screen_game * 1.0

        # self.db = ConnectDatabase()
        # point = self.db.query("SELECT points FROM player WHERE id = 1")
        # self.points = point[0][0]
        self.lostIIustration = resizeImage(pygame.image.load('./images/losetext.png'),self.position_x*0.8,self.position_y*0.2)
        self.timeOutIIustration = resizeImage(pygame.image.load('./images/lost.png'),self.position_x*0.9,self.position_y*0.55)
        # self.coins_text = font_28.render(str(number_of_coins), True, rgbBackground_dark)
        self.btLose = font_30.render("Click here to continue", True, (133,129,117))
        self.btLose_rect = self.btLose.get_rect()

    def lose_game(self, points):
        self.screen.fill(rgbBackground_light)

        #Hiển thị số xu và hình minh họa coin
        coins_text = font_28.render(str(points), True, rgbBackground_dark)
        coin_width, coin_height = coins_text.get_size()
        self.screen.blit(coins_text, (5, 5))
        self.screen.blit(coinIIustration,(coin_width+8,7))

        #Thêm hình puzzle
        rotated_image = pygame.transform.rotate(puzzleIllustration, -34)
        self.screen.blit(rotated_image,(-120,height_screen_game - 200 + 40))

        #thêm các đám mấy
        self.screen.blit(resizeImage(cloudIllustration, 64, 24),(width_screen_game - 64 - 20,10))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(10,30))
        self.screen.blit(resizeImage(cloudIllustration, 58, 22),(width_screen_game//2 - 50,height_screen_game/6))
        self.screen.blit(resizeImage(cloudIllustration, 76, 30),(width_screen_game - 50,height_screen_game // 2 + 100))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(width_screen_game*2/3,height_screen_game*5/6)) 

        #Vẽ chữ lose
        win_widtd, win_height = self.lostIIustration.get_size()
        self.screen.blit(self.lostIIustration,((self.position_x - win_widtd)/2, self.position_y*0.08))

         #vẽ btnPlayGame
        bt_width, bt_height = self.btLose.get_size()
        self.btLose_rect.topleft = ((self.position_x- bt_width)/2 , self.position_y*0.3)
        self.screen.blit(self.btLose,self.btLose_rect)

        #Vẽ hình ảnh timeout
        cup_width, cup_height = self.timeOutIIustration.get_size()
        self.screen.blit(self.timeOutIIustration,((self.position_x-cup_width)/2, self.position_y*0.39))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btLose_rect.collidepoint(event.pos):
                click_btn_sound.play()
                print("aww")
                return all_screen_value[2]