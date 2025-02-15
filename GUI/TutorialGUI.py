import pygame
from .setting import *

class Tutorial:
    
    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.viewTutorial = pygame.image.load('./images/tutorial.png')
        self.btnFinish = resizeImage(pygame.image.load('./images/btnFinishTutorial.png').convert_alpha(), width_screen_game //3 + 10, 40)
        self.btnFinish_rect = self.btnFinish.get_rect() 
    
    def draw(self):
        self.screen.fill(rgbBackground_light)

        #thêm hình puzzle
        rotated_image = pygame.transform.rotate(puzzleIllustration, -34)
        self.screen.blit(rotated_image,(-120,height_screen_game - 200 + 40))
        

        #thêm các đám mấy
        self.screen.blit(resizeImage(cloudIllustration, 64, 24),(width_screen_game - 64 - 20,10))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(10,30))
        self.screen.blit(resizeImage(cloudIllustration, 58, 22),(width_screen_game//2 - 50,height_screen_game/6))
        self.screen.blit(resizeImage(cloudIllustration, 76, 30),(width_screen_game - 50,height_screen_game // 2 + 100))
        self.screen.blit(resizeImage(cloudIllustration, 50, 20),(width_screen_game*2/3,height_screen_game*5/6))

        #thêm tutorial va btn
        self.screen.blit( resizeImage(self.viewTutorial, width_screen_game - 40,280),(20,height_screen_game//5))
        self.btnFinish_rect.topleft = (width_screen_game // 3 ,height_screen_game // 2 + 80)
        self.screen.blit( self.btnFinish, self.btnFinish_rect)

    def handle_event(self, event):
            #Xử lí sự kiện click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btnFinish_rect.collidepoint(event.pos):
                    click_btn_sound.play()
                    return all_screen_value[2]
            return None    