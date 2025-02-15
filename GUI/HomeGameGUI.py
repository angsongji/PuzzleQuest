import pygame
from .setting import *

class HomeGame:
    '''
    Giao diện trang chủ trò chơi, 
    hiển thị số tiền hiện có, 
    nút bấm play, nút bấm vào cửa hàng màu sắc, nút bấm vào danh sách các màu đã mua
    '''
    def __init__(self, display_screen_game): #display_screen_game là biến cửa sổ trò chơi
        self.screen = display_screen_game
        #Tải ảnh từ ./images/buttonPlay.png đồng thời gọi hàm resizeImage để ép ảnh về kích thước 100x100
        self.playIllustration = resizeImage(pygame.image.load('./images/buttonPlay.png'), 100, 100)
        #Lấy đối tượng Rect dùng để xử lí sự kiện click trên playIllustration
        self.playIllustration_rect = self.playIllustration.get_rect()
        self.wordPuzzleIllustration = resizeImage(pygame.image.load('./images/word_Puzzle.png'), width_screen_game -40 , 90)
        self.wordGameIllustration = resizeImage(pygame.image.load('./images/word_Game.png'), width_screen_game // 3 + 30  , 50)
        self.coins = number_of_coins #number_of_coins là biến từ setting.py
        self.cartIllustration = resizeImage(pygame.image.load('./images/shopping-cart.png'), 30, 30)
        self.cartIllustration_rect = self.cartIllustration.get_rect() 
        self.paletteIllustration = resizeImage(pygame.image.load('./images/palette.png'), 30, 30)
        self.paletteIllustration_rect = self.paletteIllustration.get_rect() 
        

    def draw(self):
        self.screen.fill(rgbBackground_dark) #tô màu nền là màu rgbBackground_dark
        
        #Hiển thị số xu và hình minh họa coin
        coins_text = font_28.render(str(self.coins), True, rgbBackground_light)
        coin_width, coin_height = coins_text.get_size()
        self.screen.blit(coins_text, (5, 5))
        self.screen.blit(coinIIustration,(coin_width+8,7))

        #Thêm hình puzzle
        self.screen.blit(puzzleIllustration,(width_screen_game - 300 // 2 -10, -200 // 2 + 10))
        rotated_image = pygame.transform.rotate(puzzleIllustration, -34)
        self.screen.blit(rotated_image,(-120,height_screen_game - 200 + 40))

        #Thêm hình các đám mấy
        self.screen.blit(resizeImage(cloudIllustration, 64, 24),(-32,40))
        self.screen.blit(resizeImage(cloudIllustration, 76, 30),(10,height_screen_game // 2 - 100))
        self.screen.blit(resizeImage(cloudIllustration, 64, 24),(width_screen_game*2/3,height_screen_game // 2))
        self.screen.blit(resizeImage(cloudIllustration, 76, 30),(width_screen_game - 50,height_screen_game // 2 + 100))

        #Thêm nút play
        self.playIllustration_rect.topleft = ((width_screen_game //2) - (100 //2),height_screen_game // 2 + 100) 
        self.screen.blit(self.playIllustration,self.playIllustration_rect)

        #thêm tên game
        rotated_wordPuzzle = pygame.transform.rotate(self.wordPuzzleIllustration, 15)
        self.screen.blit(rotated_wordPuzzle,(0,70))
        rotated_wordGame = pygame.transform.rotate(self.wordGameIllustration, -10)
        self.screen.blit(rotated_wordGame,(width_screen_game // 2 ,height_screen_game/4 + 20))

        #Thêm nút xem danh sách màu đã mua va nút xem cửa hàng màu sắc
        self.paletteIllustration_rect.topleft = ((width_screen_game - 50,height_screen_game - 100))
        self.screen.blit(self.paletteIllustration,self.paletteIllustration_rect)
        self.cartIllustration_rect.topleft = ((width_screen_game - 50,height_screen_game - 50))
        self.screen.blit(self.cartIllustration,self.cartIllustration_rect)

    def handle_event(self, event):
        #Xử lí sự kiện click
        #all_screen_value là biến từ setting.py
        #click_btn_sound là biến từ setting.py để tạo âm thanh lúc ấn vào nút
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.playIllustration_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[1]
            elif self.cartIllustration_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[7]
            elif self.paletteIllustration_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[8]
            
    def resetCoins(self): #Cập nhật số xu
        db = database.ConnectDatabase() 
        db_player = db.query("SELECT * FROM player WHERE id = 1")
        self.coins = db_player[0][1]
        db.closeConnection()
        