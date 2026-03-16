import copy
import random
class RandomNumbers:
    '''
    Thay vì dùng hàm từ module random để tạo ra mảng có giá trị ngẫu nhiên từ 0->8
    Sẽ có khả năng cao mảng random đó không có đường đi đến goal, việc dùng thuật toán A* sẽ trở nên lãng phí
    Giải pháp là tạo ra lớp RandomNumbers dùng để tạo mảng random với nguyên lý hoạt động là xáo trộn goal 
    '''
    def __init__(self):
        self.goal = [
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        ]
        

    def create(self): #Hàm để tạo ra trạng thái ngẫu nhiên
        puzzle = self.shuffle_puzzle() #Gọi hàm xáo trộn goal
        puzzle_flat = []  # Danh sách rỗng để chứa các phần tử
        for row in puzzle:
            for value in row:
                puzzle_flat.append(value)  # Thêm từng giá trị vào danh sách
        return puzzle_flat
        
    def shuffle_puzzle( self,moves=random.randint(30, 150)): 
        #moves là số lần xáo trộn, được lấy ngẫu nhiên từ [30,150]
        current_state = copy.deepcopy(self.goal)  # Tạo một bản sao của trạng thái goal
        for _ in range(moves):
            zero_position = self.find_zero_position(current_state)  # Tìm vị trí của ô số 0 trả về tuple
            # Lấy các bước di chuyển hợp lệ dựa trên vị trí của ô trống
            valid_moves = self.get_valid_moves(zero_position, current_state)
        
            # Chọn một nước đi ngẫu nhiên trong số các bước có thể đi
            move = random.choice(valid_moves)
            
            # Cập nhật trạng thái hiện tại thành trạng thái mới được chọn
            current_state = move
    
        return current_state

    def get_valid_moves(self,zero_position, state):
        i, j = zero_position #unpacking
        valid_moves = []
        # Xác định các bước di chuyển hợp lệ và tạo các trạng thái mới
        if i - 1 >= 0:  # Di chuyển lên
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
            valid_moves.append(new_state)
        if i + 1 <= 2:  # Di chuyển xuống
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
            valid_moves.append(new_state)
        if j - 1 >= 0:  # Di chuyển sang trái
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
            valid_moves.append(new_state)
        if j + 1 <= 2:  # Di chuyển sang phải
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]
            valid_moves.append(new_state)
        return valid_moves 

    def find_zero_position(self, state):
        for i, row in enumerate(state): #i: vị trí hàng, row: giá trị của hàng i
            for j, value in enumerate(row): #j: vị trí cột, value: giá trị của cột j
                if value == 0: #Nếu giá trị = 0 (ô trống)
                    return (i, j) #Trả về vị trí hàng i, cột j