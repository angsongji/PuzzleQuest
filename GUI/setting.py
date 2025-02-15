import pygame
import tkinter as tk
import database

pygame.init()

def resizeImage(image, width, height):
    return pygame.transform.scale(image, (width, height))

# def stringToPuzzle(value):
#     arr_num = [int(num) if num != '0' else "empty" for num in value.split(',')]
#     return arr_num

def stringToPuzzle(value):
    arr_num = [int(num) for num in value.split(',')]
    return arr_num

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def stringToColor(string):
    # Loại bỏ dấu ngoặc đơn và khoảng trắng
    string = string.strip("() ")
    # Chia chuỗi và chuyển đổi thành tuple màu
    color_tuple = tuple(map(int, string.split(',')))
    return color_tuple

def puzzleToString(value):
    # Biến đổi danh sách
    transformed_list = [str(item) if item != "empty" else '0' for item in value]
    # Nối các phần tử thành chuỗi
    result = ','.join(transformed_list)
    return result


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Bỏ ký tự '#' ở đầu
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

root = tk.Tk()
root.withdraw()  # Ẩn cửa sổ tkinter

# Lấy kích thước màn hình
width_screen_game = int(root.winfo_screenwidth() / 4)
height_screen_game = int(root.winfo_screenheight() * 3 / 4)

font_28 = pygame.font.SysFont('Arial', 28)
font_22 = pygame.font.SysFont('Arial', 22)
font_30 = pygame.font.SysFont('Arial', 30,bold=True)
rgbBackground_light = (251,240,199)
rgbBackground_dark = (130,105,77)
number_of_coins = 0 # Khởi tạo giá trị là 0, nhưng xuống bên dưới có lấy từ database lên
coins_achieved = 0


time_finsh = 6
game_size = 3
box_size = 30
puzzle_size = 100
init_puzzle = []

color_box_sm = (139, 0, 0)
# color_text_num = rgbBackground_light
color_box_bg = rgbBackground_dark
puzzleIllustration = resizeImage(pygame.image.load('./images/puzzleDecorate.png'), 300, 200)
cloudIllustration = pygame.image.load('./images/cloud.png')
coinIIustration =  resizeImage(pygame.image.load('./images/coin.png'), 30, 30)
cursor_image = resizeImage(pygame.image.load('./images/cursor.png'),10,26)
all_screen_value = (
    'home_game', #0
    'home_tutorial', #1
    'main_game', #2
    'tutorial', #3
    'pause', #4
    'lose_game', #5
    'win_game', #6
    'store_color', #7
    'my_color' #8
)
sound_Game = pygame.mixer.music.load('./audio/backgroundMusic.mp3')
click_puzzle_sound = pygame.mixer.Sound('./audio/clickPuzzle.mp3')
click_btn_sound = pygame.mixer.Sound('./audio/clickBtn.mp3')
win_sound = pygame.mixer.Sound('./audio/win.wav')
lose_sound = pygame.mixer.Sound('./audio/lose.wav')
db = database.ConnectDatabase() 
db_player = db.query("SELECT * FROM player WHERE id = 1")
number_of_coins = db_player[0][1]


db_listPuzzle = db.query("SELECT * FROM puzzle")
# goal_game= ['1','2','3','4','5','6','7','8', 'empty']
goal = stringToPuzzle(db_listPuzzle[0][1])
# print(goal_game)
# if goal_game == goal : 
#     print("Ket qua dung")
# else: 
#     print("Ket qua sai")
db_listGame = db.query("SELECT * FROM game")
for row_game in db_listGame :
    if row_game[1] == 0 :
        print("so luong thoi gian hosn thanh",row_game[2]*2)
        time_finsh = row_game[2] + 4
        break
        
db.closeConnection()