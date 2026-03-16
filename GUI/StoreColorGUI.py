import pygame
from .setting import *
from .MyColorGUI import MyColor

class StoreColor(MyColor):
    
    def __init__(self, display_screen_game):
        super().__init__(display_screen_game)
        self.colors = []
        self.coins = number_of_coins
        self.buyIllustration = resizeImage(pygame.image.load('./images/bought.png'), 120, 30)
        self.buyIllustration_rect = self.buyIllustration.get_rect() 
        self.prices = []
        db = database.ConnectDatabase() 
        rows_color = db.query("SELECT * FROM color")
        db.closeConnection()
        for row1 in rows_color:
            flag = False
            for row2 in self.rows_color_purchased:
                if stringToColor(row1[1]) == stringToColor(row2[1]) :
                    flag = True
                    break
            if not flag :
                self.colors.append(stringToColor(row1[1]))
                self.prices.append(row1[2])
        if len(self.colors) != 0:
            self.color = self.colors[0]
            self.price = self.prices[0]

    def draw(self):
        self.drawBtnBack()
        if len(self.colors) != 0:
            self._drawPuzzleAndColor()
            self.drawCoinAndBtn()

    
    def drawCoinAndBtn(self):
        #Hiển thị số xu và hình minh họa coin
        coins_text = font_28.render(str(self.coins), True, rgbBackground_dark)
        coin_width, coin_height = coins_text.get_size()
        self.screen.blit(coins_text, (width_screen_game-45-coin_width, 10))
        self.screen.blit(coinIIustration,(width_screen_game-40,11))

        #Hien gia cua mau do
        price_text = font_28.render(str(self.price), True, rgbBackground_dark)
        price_width, price_height = price_text.get_size()
        self.screen.blit(price_text, (width_screen_game//2 - 20,  (box_size * 2) * game_size + self.height_wrap_squares + height_screen_game//4))
        self.screen.blit(coinIIustration,(width_screen_game//2 + price_width//2,  (box_size * 2) * game_size + self.height_wrap_squares + height_screen_game//4))

        #Hien nut mua
        if self.coins >= self.price:   
            self.buyIllustration_rect.topleft = ((width_screen_game / 2) - 60, (box_size * 2) * game_size + self.height_wrap_squares + height_screen_game//4 + 50 ) 
            self.screen.blit(self.buyIllustration, self.buyIllustration_rect)


    def handle_event(self, event):
        # Kiểm tra sự kiện click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.backIllustration_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[0]
            if self.buyIllustration_rect.collidepoint(event.pos):
                    click_btn_sound.play()
                    if(self.coins >= self.price):
                        index_remove = 0
                        found = False  # Biến đánh dấu xem đã tìm thấy màu hay chưa
                        for index, c in enumerate(self.colors):
                            if self.color == c:
                                found = True
                                index_remove = index
                                break

                        # Nếu tìm thấy màu, xóa khỏi danh sách
                        if found:
                            color = self.color
                            self.coins = self.coins - self.price
                            self.colors.pop(index_remove)
                            self.prices.pop(index_remove)
                            if len(self.colors) != 0:
                                self.color = self.colors[0]
                                self.price = self.prices[0]
                            else:
                                self.color = ""
                                self.price = 0
                            db = database.ConnectDatabase() 
                            db.execute("INSERT INTO color_purchased (id, hex) VALUES (?, ?)", (1, str(color).replace('(', '').replace(')', '')))
                            db.execute("UPDATE player SET points = ? WHERE id = ?", (str(self.coins), 1))
                            db.closeConnection() 
                            
                        self.draw()
                        # self._drawBtn(self.selectIllustration, self.selectIllustration_rect)
                        # db = database.ConnectDatabase() 
                        # db.execute("UPDATE player SET hex_selected = ? WHERE id = ?", (str(self.color), 1))
                        # db.closeConnection()   
            
            mouse_x, mouse_y = event.pos
            for square in self.squares:
                flag, hex, price = square.click(mouse_x, mouse_y)
                if flag:
                    click_puzzle_sound.play()
                    self.color = hex
                    self.price = price
                    self.draw()
                    break
    
    def resetCoins(self):
        db = database.ConnectDatabase() 
        db_player = db.query("SELECT * FROM player WHERE id = 1")
        self.coins = db_player[0][1]
        db.closeConnection()