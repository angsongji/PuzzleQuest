import pygame
from .setting import *
from .square import *
from database import ConnectDatabase

class mainGame:

    def __init__(self, display_screen_game):
        self.screen = display_screen_game
        self.x_position = width_screen_game * 1.0
        self.y_position = height_screen_game * 1.0
        self.id = -1
        self.db = ConnectDatabase()
        self.points = number_of_coins
        self.color = (255,255,255)
        colors = self.db.query("SELECT hex_selected FROM player WHERE id = 1")
        if colors:
            color_hex = colors[0][0]  # Mã màu từ cơ sở dữ liệu
            color_rgb = tuple(map(int, color_hex.strip("()").split(",")))
            self.color = color_rgb

        play_score = self.db.query("SELECT steps FROM game WHERE id_init = ?", (self.id,))
        self.time_finsh = time_finsh
        self.time_text = font_28.render(str(self.time_finsh), True, (139, 0, 0))

        self.pauseIllustration = pygame.image.load('./images/pause.png')
        self.btPause_rect = self.pauseIllustration.get_rect()
        self.flagIIustration =  resizeImage(pygame.image.load('./images/flag.png'), 30, 30)
        self.coins_text = font_28.render(str(self.points), True, rgbBackground_dark)
    
        self.squares, self.empty_square, self.positions= self.create_grid()


    def draw_grid(self, display_screen_game, grid_x, grid_y, block_size, rows, cols, numbers, grid_background_color, line_color):
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

    def draw_grid_opp(self, display_screen_game, grid_x, grid_y, block_size, rows, cols):
        for row in range(rows):
            for col in range(cols):
                rect_x = grid_x + col * block_size
                rect_y = grid_y + row * block_size
                pygame.draw.rect(display_screen_game, rgbBackground_light, (rect_x, rect_y, block_size, block_size), 1)


    def getPuzzle(self):
        # db = ConnectDatabase()
        db_listPuzzle = self.db.query("SELECT * FROM puzzle")
        db_listGame = self.db.query("SELECT * FROM game")
        init_puzzle = []
        for row_game in db_listGame :
            if row_game[1] == 0 :
                for row_puzzle in db_listPuzzle:
                    if row_game[0] == row_puzzle[0]:
                        init_puzzle = stringToPuzzle(row_puzzle[1])
                        self.id = row_game[0]
                        break

                break
        return init_puzzle
  

    def create_grid(self):
        
        numbers = self.getPuzzle()
        squares = pygame.sprite.Group()
        empty_square = None
        positions = []  # Mảng lưu giá trị các ô theo thứ tự
        for row in range(game_size):
            for col in range(game_size):
                number = numbers.pop(0)
                square = Square(col, row, str(number),self.color)
                squares.add(square)
                positions.append(square.text)  # Lưu giá trị (thay vì tọa độ)
                if number == 0:
                    empty_square = square
        print(positions)
        return squares, empty_square, positions
    


    def draw_puzzle_game(self, grid_x_box, grid_y_box):
        self.squares.update(grid_x_box, grid_y_box)
        self.squares.draw(self.screen)

    def is_adjacent(self, square, empty_square):
        return abs(square.x - empty_square.x) + abs(square.y - empty_square.y) == 1



    def swapGUI(self, square, empty_square):
        # Hoán đổi vị trí
        square.x, empty_square.x = empty_square.x, square.x
        square.y, empty_square.y = empty_square.y, square.y

        # Cập nhật vị trí rect để vẽ
        square.rect.topleft = (square.x * puzzle_size, square.y * puzzle_size)
        empty_square.rect.topleft = (empty_square.x * puzzle_size, empty_square.y * puzzle_size)

        # Cập nhật mảng positions với giá trị mới
        idx_square = self.positions.index(square.text)
        idx_empty = self.positions.index(empty_square.text)
        self.positions[idx_square], self.positions[idx_empty] = self.positions[idx_empty], self.positions[idx_square]


    def reload(self):
        colors = self.db.query("SELECT hex_selected FROM player WHERE id = 1")
        color_hex = colors[0][0]  # Lấy mã màu đầu tiên từ kết quả
        color_rbg = tuple(map(int, color_hex.strip("()").split(",")))
        self.color = color_rbg

        steps = self.db.query("SELECT steps FROM game WHERE id_init = ?", (self.id,))
        self.time_finsh = steps[0][0] + 4

        db_player = self.db.query("SELECT * FROM player WHERE id = 1")
        self.points = db_player[0][1] 
        self.time_text = font_28.render(str(self.time_finsh), True, (139, 0, 0))

        self.coins_text = font_28.render(str(self.points), True, rgbBackground_dark)

        # Tạo lại lưới trò chơi
        self.squares, self.empty_square, self.positions = self.create_grid()

        # Vẽ lại màn hình trò chơi
        self.screen.fill(rgbBackground_light)
        self.main_game(0)


    def main_game(self, elapsed_time):
        self.screen.fill(rgbBackground_light)

        #Hiển thị số xu và hình minh họa coin
        coin_width, coin_height = self.coins_text.get_size()
        self.screen.blit(self.coins_text, (5, 5))
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

        # Thêm button pause
        pause_width, pause_height = self.pauseIllustration.get_size()
        self.btPause_rect.topleft = (width_screen_game - pause_width - 5,self.y_position * 0.01)
        self.screen.blit(self.pauseIllustration, self.btPause_rect)

        #vẽ cờ và thời gian    

        self.time_text = font_28.render(str(format_time(self.time_finsh)), True, (139, 0, 0))
        time_width, time_height = self.time_text.get_size()
        flag_width, flag_height = self.flagIIustration.get_size()

        padding = 10 
        total_width = flag_width + padding + time_width

        x_start = (self.x_position - total_width) / 2

        self.screen.blit(self.flagIIustration,(x_start,self.y_position * 0.1))
        self.screen.blit(self.time_text,(x_start + flag_width + padding,self.y_position * 0.1))

        # vẽ goal 
        grid_width = box_size * game_size
        grid_x = (self.x_position / 2) - (grid_width / 2)  # Center the grid horizontally
        self.draw_grid(self.screen, grid_x, self.y_position*0.16, box_size, game_size, game_size,goal, color_box_sm, rgbBackground_light)

        # Vẽ thời gian chơi
        
        player_time = format_time(elapsed_time)
        player_time_txt = font_30.render(player_time, True, color_box_sm)
        player_width, player_height = player_time_txt.get_size()
        self.screen.blit(player_time_txt, ((self.x_position-player_width)/2,self.y_position*0.34))

        #Vẽ màn hình game
        grid_width_box = puzzle_size * game_size
        grid_x_box = (self.x_position / 2) - (grid_width_box / 2) 
        grid_y_box = self.y_position * 0.43
        self.draw_puzzle_game(grid_x_box, grid_y_box)
        self.draw_grid_opp(self.screen,grid_x_box,grid_y_box,puzzle_size,game_size,game_size)

        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btPause_rect.collidepoint(event.pos):
                self.paused = True
                click_btn_sound.play()
                return all_screen_value[4]
            
            
            mouse_x, mouse_y = event.pos
            for square in self.squares:
                if square.click(mouse_x, mouse_y) and self.is_adjacent(square, self.empty_square):
                    self.swapGUI(square, self.empty_square)
                    click_puzzle_sound.play()
                    goal_game = [int(num) for num in self.positions]

                    if goal_game == goal:
                        play_score = self.db.query("SELECT steps FROM game WHERE id_init = ?", (self.id,))
                        update_result = self.db.execute("UPDATE game SET status = ? WHERE id_init = ?", (1, self.id))
                        self.points += play_score[0][0]
                        player_id = 1  
                        update_points_result = self.db.execute("UPDATE player SET points = points + ? WHERE id = ?", (play_score[0][0], player_id))
                        return all_screen_value[6] , play_score[0][0]
                    
         

                