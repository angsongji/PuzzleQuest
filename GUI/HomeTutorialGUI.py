import pygame
from .setting import *

class HomeTutorial:
    
    def __init__(self, display_screen_game):
        #convert_alpha() sẽ giúp hình ảnh của hoạt động hiệu quả hơn khi hiển thị với nền trong suốt.
        self.screen = display_screen_game
        self.viewAskTutorial = pygame.image.load('./images/viewAskTutorial.png')
        self.btnSkip = resizeImage(pygame.image.load('./images/btnSkipTutorial.png').convert_alpha(), width_screen_game //3 + 10, 40)
        self.btnSkip_rect = self.btnSkip.get_rect()
        self.btnShow = resizeImage(pygame.image.load('./images/btnShowTutorial.png').convert_alpha(), width_screen_game //3 + 10, 40)
        self.btnShow_rect = self.btnShow.get_rect()


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

        #thêm view, btn
        self.screen.blit( resizeImage(self.viewAskTutorial, width_screen_game - 50,150),(25,height_screen_game//4))
        self.btnSkip_rect.topleft = (40,height_screen_game//4 + 150)
        self.screen.blit( self.btnSkip, self.btnSkip_rect)
        self.btnShow_rect.topleft = (width_screen_game // 2,height_screen_game//4 + 150)
        self.screen.blit( self.btnShow, self.btnShow_rect)


    def handle_event(self, event):
        #Xử lí sự kiện click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btnSkip_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[2]
            elif self.btnShow_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[3]
        return None