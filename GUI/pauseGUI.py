import pygame
from .setting import *

class pause:
    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.position_x = width_screen_game * 1.0
        self.position_y = height_screen_game * 1.0
        self.btContinue = resizeImage(pygame.image.load('./images/btContinue.png'), self.position_x *0.6, self.position_y*0.1)
        self.btContinue_rect = self.btContinue.get_rect()
        self.btExitPlay = resizeImage(pygame.image.load('./images/btExit.png'), self.position_x *0.6, self.position_y*0.1)
        self.btExitPlay_rect = self.btExitPlay.get_rect()

    def pause_game(self):
        self.screen.fill(rgbBackground_light)
        
        #Thêm hình puzzle
        rotated_image = pygame.transform.rotate(puzzleIllustration, -34)
        self.screen.blit(rotated_image,(-120,height_screen_game - 200 + 40))

        #thêm các đám mấy
        self.screen.blit(resizeImage(cloudIllustration, 64, 24),(width_screen_game - 64 - 20,10))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(10,30))
        self.screen.blit(resizeImage(cloudIllustration, 58, 22),(width_screen_game//2 - 50,height_screen_game/6))
        self.screen.blit(resizeImage(cloudIllustration, 76, 30),(width_screen_game - 50,height_screen_game // 2 + 100))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(width_screen_game*2/3,height_screen_game*5/6))  

        #Thêm btExitPlay và btContinue
        btExit_width, btExit_height = self.btExitPlay.get_size()
        btContinue_width, btContinue_height = self.btContinue.get_size()

        self.btContinue_rect.topleft = ((width_screen_game - btContinue_width)/2,self.position_y*0.35)
        self.screen.blit(self.btContinue, self.btContinue_rect)

        self.btExitPlay_rect.topleft = ((width_screen_game - btContinue_width)/2,self.position_y*0.50)
        self.screen.blit(self.btExitPlay, self.btExitPlay_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btContinue_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[2]
            elif self.btExitPlay_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[0]