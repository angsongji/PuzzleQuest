import pygame
import random
import Algorithm_Astart

from .setting import *

class win:
    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.position_x = width_screen_game * 1.0
        self.position_y = height_screen_game * 1.0


        self.winTextIIustration = resizeImage(pygame.image.load('./images//wintext.png'),self.position_x*0.8,self.position_y*0.2)
        self.cupIIustration = resizeImage(pygame.image.load('./images/win.png'),self.position_x*0.9,self.position_y*0.55)
        self.lostIIustration = pygame.image.load('./images/losetext.png')
        self.btWin = font_30.render("Click here to continue", True, (255,195,0))
        self.btWin_rect = self.btWin.get_rect()

    def win_game(self, score, points):
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

        #Vẽ chữ Win
        win_widtd, win_height = self.winTextIIustration.get_size()
        self.screen.blit(self.winTextIIustration,((self.position_x - win_widtd)/2, self.position_y*0.08))
    
        #Số tiền đạt được khi hoàn thành trò chơi
        achv_coins = font_28.render(str(score), True, rgbBackground_dark)
        achv_coins_width, achv_coins_height = achv_coins.get_size()
        img_coins_width, img_coins_height = coinIIustration.get_size()
        padding = 5
        total_width = achv_coins_width + padding + img_coins_width
        x_start = (self.position_x - total_width)/2

        self.screen.blit(achv_coins,(x_start,self.position_y * 0.28))
        self.screen.blit(coinIIustration,(x_start + achv_coins_width + padding,self.position_y * 0.28))

        #vẽ btnPlayGame
        bt_width, bt_height = self.btWin.get_size()
        self.btWin_rect.topleft = ((self.position_x- bt_width)/2 , self.position_y*0.35)
        self.screen.blit(self.btWin,self.btWin_rect)

        #Vẽ hình ảnh cup
        cup_width, cup_height = self.cupIIustration.get_size()
        self.screen.blit(self.cupIIustration,((self.position_x-cup_width)/2, self.position_y*0.39))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btWin_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[2] 
            

    def createRandom(self):
        list_numbers = Algorithm_Astart.RandomNumbers().create()
        db = database.ConnectDatabase() 
        puzzles = db.query("SELECT * FROM puzzle")
        flag = False
    
        # Kiểm tra xem puzzle đã tồn tại trong cơ sở dữ liệu chưa
        for row in puzzles:
            if row[1] == puzzleToString(list_numbers):
                flag = True
                break

        if not flag:  # Nếu không tìm thấy, trả về kết quả hợp lệ
            db.execute("INSERT INTO puzzle (value) VALUES (?)", (puzzleToString(list_numbers),))
            db.closeConnection()
            return len(puzzles) + 1, list_numbers  # Trả về ID và danh sách số
        
        db.closeConnection()  # Đảm bảo đóng kết nối nếu không sử dụng
        return self.createRandom()  # Gọi đệ quy nếu tìm thấy puzzle đã tồn tại

        
        
        
    def createOtherGame(self, attempts=0, max_attempts=15):
        db = database.ConnectDatabase() 
        games = db.query("SELECT * FROM game")
        if len(games) == 100 :
            print("DA 100 VAN, KHONG RANDOM")
            random_game_index = random.randint(0, len(games)-1)
            db.execute("UPDATE game SET status = ? WHERE id_init = ?", (0, games[random_game_index][0]))
        else:
            id_puzzle,list_numbers = self.createRandom()
            # Tạo mảng từ 0 đến 8
            
            # Kiểm tra đường đi đến mục tiêu
            path = Algorithm_Astart.Astar(list_numbers)
            if path.steps() != 0: #Có đường đi
                db.execute("INSERT INTO puzzle (value) VALUES (?)", (puzzleToString(list_numbers),))
                db.execute("INSERT INTO game (id_init, steps) VALUES (?, ?)", (id_puzzle, path.steps()))
            else:
                if attempts < max_attempts:
                    self.createOtherGame(attempts + 1, max_attempts)  # Gọi lại với số lần thử tăng lên
                else:
                    random_game_index = random.randint(0, len(games))
                    db.execute("UPDATE game SET status = ? WHERE id_init = ?", (0, games[random_game_index][0]))
        db.closeConnection()
        return None