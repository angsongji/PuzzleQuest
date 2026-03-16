import pygame
from .setting import *
from .square import Square

class MyColor:
    #Giao diện các màu đã mua
    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.color = color_box_bg
        self.backIllustration = resizeImage(pygame.image.load('./images/back.png'), 20, 20)
        self.backIllustration_rect = self.backIllustration.get_rect() 
        self.selectIllustration = resizeImage(pygame.image.load('./images/select.png'), 120, 30)
        self.selectIllustration_rect = self.selectIllustration.get_rect() 
        self.squares = pygame.sprite.Group()  # Nhóm cho các hình vuông màu sắc
        self.height_wrap_squares = 0
        self.colors = [] #Mảng mã màu
        self.prices = [] #Mảng tiền tương ứng với mã màu
        self.getListColor()

    def getListColor(self):
        db = database.ConnectDatabase() 
        self.rows_color_purchased = db.query("SELECT * FROM color_purchased WHERE id = 1")
        db.closeConnection()
        self.colors.clear()
        self.prices.clear()
        for row in self.rows_color_purchased:
            self.colors.append(stringToColor(row[1]))  #Danh sách màu trong database self.colors
            self.prices.append(0) #Màu đã mua nên giá tiền là 0

    def draw(self):
        self.drawBtnBack() #Thêm nút back về home vào giao diện
        self._drawPuzzleAndColor() #Thêm puzzle mẫu và các màu sắc đã mua
        self._drawBtn(self.selectIllustration, self.selectIllustration_rect) #Thêm nút chọn màu sắc
    
    def drawBtnBack(self):
        self.screen.fill((255, 255, 255))
        # Thêm nút back
        self.backIllustration_rect.topleft = (15, 15) 
        self.screen.blit(self.backIllustration, self.backIllustration_rect)

    def _drawPuzzleAndColor(self):
        self.squares.empty()

        # Hoặc khởi tạo lại nhóm
        self.squares = pygame.sprite.Group()

        # Thêm hình puzzle
        grid_width = (box_size * 2) * game_size 
        grid_x = (width_screen_game / 2) - (grid_width / 2)  # Center the grid horizontally
        self._draw_grid(self.screen, grid_x, height_screen_game * 0.1, box_size * 2, game_size, game_size, goal, self.color, rgbBackground_light)

        # Thêm các màu sắc (hình vuông)
        x = 30
        y = height_screen_game // 2 + 15
        i = 0
        for c in self.colors:
            if x > width_screen_game - 50 : 
                x = 30
                y = y + 40
            sprite = self.Square(x, y, c, price= self.prices[i])
            i = i + 1
            x = x + 40
            self.squares.add(sprite)  # Thêm hình vuông vào nhóm

        # Vẽ tất cả các hình vuông
        self.squares.draw(self.screen)

        if self.height_wrap_squares == 0:
                bounding_rect = self._get_bounding_rect()
                self.height_wrap_squares = bounding_rect.height
        

    
    def _drawBtn(self, image, image_rect):
        if self.color != color_box_bg : 
            image_rect.topleft = ((width_screen_game / 2) - 60, height_screen_game - (box_size * 2) * game_size - self.height_wrap_squares) 
            self.screen.blit(image, image_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.backIllustration_rect.collidepoint(event.pos):
                click_btn_sound.play()
                return all_screen_value[0]
            if self.selectIllustration_rect.collidepoint(event.pos):
                    click_btn_sound.play()
                    global color_box_bg
                    color_box_bg = self.color
                    self.draw()
                    self._drawBtn(self.selectIllustration, self.selectIllustration_rect)
                    db = database.ConnectDatabase() 
                    db.execute("UPDATE player SET hex_selected = ? WHERE id = ?", (str(self.color), 1)) #Cập nhật mã màu đang chọn trong database
                    db.closeConnection()   
            mouse_x, mouse_y = event.pos
            for square in self.squares: #gắn sự kiện click trên mỗi màu
                flag, hex, price = square.click(mouse_x, mouse_y)
                if flag:
                    click_puzzle_sound.play()
                    self.color = hex
                    self.draw()
                    self._drawBtn(self.selectIllustration, self.selectIllustration_rect)
                    break

    #Vẽ giao diện puzzle
    def _draw_grid(self, display_screen_game, grid_x, grid_y, block_size, rows, cols, numbers, grid_background_color, line_color):
        pygame.draw.rect(display_screen_game, grid_background_color, (grid_x, grid_y, block_size * cols, block_size * rows))
        for row in range(rows):
            for col in range(cols):
                x = grid_x + col * block_size
                y = grid_y + row * block_size
                pygame.draw.rect(display_screen_game, line_color, (x, y, block_size, block_size), 1)
                number = numbers[row * cols + col]
                if number != 0:
                    text_surface = font_28.render(str(number), True, rgbBackground_light)
                    text_rect = text_surface.get_rect(center=(x + block_size // 2, y + block_size // 2))
                    display_screen_game.blit(text_surface, text_rect)

    def _get_bounding_rect(self): #Kích thước bao quanh nhóm square
        if not self.squares:
            return pygame.Rect(0, 0, 0, 0)  # Trả về rect rỗng nếu không có sprite

        # Lấy rect đầu tiên để bắt đầu
        bounding_rect = self.squares.sprites()[0].rect.copy()

        for sprite in self.squares:
            bounding_rect = bounding_rect.union(sprite.rect)

        return bounding_rect

    def reload(self):
        self.getListColor()
        self.draw()

    class Square(pygame.sprite.Sprite): #Lớp hình vuông đại diện cho từng ô màu sắc mà người dùng sẽ click chọn
        def __init__(self, x, y, hex, hex_selected=color_box_bg, size=30, price = 0):
            super().__init__()
            self.price = price
            self.hex = hex
            self.x = x
            self.y = y
            self.image = pygame.Surface((size, size))
            self.image.fill(self.hex)
            self.rect = self.image.get_rect(topleft=(self.x , self.y))  # Cần đặt topleft

        def click(self, mouse_x, mouse_y):
            if self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom:
                return True, self.hex, self.price  # Trả về True khi nhấp thành công
            return False, None, None


