from .puzzle import Puzzle
from queue import PriorityQueue

class Astar:
    def __init__(self, value):
        '''
        tham só value là một mảng có dạng [1, 3, 6, 8, 0, 2, 7, 5, 4]
        '''
        #Khởi tạo đối tượng Puzzle init cho bài toán A*
        #Chuyển value thành mảng 3x3 bằng hàm flat_To_Value_Puzzle
        self.puzzle_init = Puzzle(None, self.flat_To_Value_Puzzle(value))
        self.CLOSED = [] #CLOSED: Danh sách chứa các trạng thái đã duyệt.
        self.OPEN = PriorityQueue()  #Khởi tạo hàng đợi ưu tiên cho OPEN
        self.max_steps = 80 #Số bước tối đa để tránh lặp vô hạn bài toán A*
        self.solve_Problem() #Gọi hàm thực hiển giải thuật A*
        
       
    def solve_Problem(self):
         # Thêm tuple trạng thái khởi đầu cùng với giá trị f vào OPEN
        self.OPEN.put((self.puzzle_init.f_puzzle, self.puzzle_init)) 
        
        while not self.OPEN.empty(): #Hàng đợi chưa rỗng
            # Ký hiệu _ được sử dụng để chỉ rằng ta không quan tâm đến giá trị đó
            # Lấy trạng thái có độ ưu tiên cao nhất 
            _, current_puzzle = self.OPEN.get()  
            # Trừ 1 cho trạng thái ban đầu, nếu CLOSED đã duyệt số puzzle = max_steps thì không duyệt tiếp
            if len(self.CLOSED) - 1 > self.max_steps :
                break
            if not current_puzzle.is_goal():  #Nếu trạng thái vừa lấy ra từ hàng đợi không là trạng thái đích thì sẽ tìm các trạng thái kề
                for i in range(0,4): #Chạy i tương ứng 4 trạng thái kề từ trạng thái vừa lấy ra khỏi hàng đợi
                    nextPuzzle = self.next_puzzle(current_puzzle, i) #Gọi hàm next_puzzle để sinh ra trạng thái kề thứ i
                    if nextPuzzle is not None: #Nếu tồn tại trạng thái kề thứ i
                        #Kiểm tra nextPuzzle có ở trong OPEN chưa? 
                        #Sau đó trả về tuple (boolean, puzzle): boolean(True, False) và (puzzle hoặc None)
                        flag, puzzle_in_Open = self.in_Open(nextPuzzle) 
                        if flag: #Nếu trạng thái kề next có ở trong hàng đợi
                            if puzzle_in_Open.f_puzzle < nextPuzzle.f_puzzle:
                                continue
                        #Kiểm tra nextPuzzle có ở trong CLOSED chưa? 
                        #Sau đó trả về tuple (boolean, puzzle): boolean(True, False) và (puzzle hoặc None)
                        flag, puzzle_in_Close = self.in_Close(nextPuzzle)
                        if flag: #Nếu trạng thái kề next có ở trong CLOSED
                            if puzzle_in_Close.f_puzzle < nextPuzzle.f_puzzle:
                                continue
                            else:
                                self.OPEN.put((nextPuzzle.f_puzzle, nextPuzzle))
                        else:
                            self.OPEN.put((nextPuzzle.f_puzzle, nextPuzzle))
                
                self.CLOSED.append(current_puzzle) #Thêm current_puzzle vào danh sách đã duyệt CLOSED
            else:
                self.CLOSED.append(current_puzzle)
                break

    def next_puzzle(self, current, stt):
        """
        Một trạng thái có tối đa 4 trạng thái kề
        Hàm xây dựng các trạng thái kề từ trạng thái current.
        stt là thứ tự của trạng thái kề.
        """
        cp = current.copy_v_puzzle()  # Sao chép trạng thái hiện tại vào cp
        next_value = cp.v_puzzle  # Lấy giá trị ma trận của trạng thái cp
        for i in range(3):
            for j in range(3):
                if next_value[i][j] == 0:  # Tìm đến giá trị 0 trong ma trận
                    if stt == 0:  # Trạng thái kề 1 - lên
                        if i - 1 >= 0: #Kiểm tra Có thể di chuyển lên nếu không ra ngoài biên
                            next_value[i][j] = next_value[i - 1][j]
                            next_value[i - 1][j] = 0
                        else:
                            return None
                    elif stt == 1:  # Trạng thái kề 2 - xuống
                        if i + 1 <= 2: #Kiểm tra Có thể di chuyển xuống nếu không ra ngoài biên
                            next_value[i][j] = next_value[i + 1][j]
                            next_value[i + 1][j] = 0
                        else:
                            return None
                    elif stt == 2:  # Trạng thái kề 3 - trái
                        if j - 1 >= 0: #Kiểm tra Có thể di chuyển qua trái nếu không ra ngoài biên
                            next_value[i][j] = next_value[i][j - 1]
                            next_value[i][j - 1] = 0
                        else:
                            return None
                    elif stt == 3:  # Trạng thái kề 4 - phải
                        if j + 1 <= 2: #Kiểm tra Có thể di chuyển qua phải nếu không ra ngoài biên
                            next_value[i][j] = next_value[i][j + 1]
                            next_value[i][j + 1] = 0
                        else:
                            return None
                    return Puzzle(current, next_value)  # Trả về trạng thái kề thứ stt nếu có tồn tại
        return None  # Trả về None nếu không tìm thấy trạng thái kề thứ stt


    def in_Open(self, puzzle):
        # Kiểm tra xem trạng thái có trong OPEN hay không
        for _, task in self.OPEN.queue:  # Duyệt qua tất cả trạng thái trong OPEN
            if task.compare_v_puzzle(puzzle):  # So sánh ma trận
                return True, task
        return False, None
    
    def in_Close(self, puzzle):
        # Kiểm tra xem trạng thái có trong CLOSED hay không
        for p in self.CLOSED:
            if p.compare_v_puzzle(puzzle):  # So sánh ma trận
                return True, p
        return False, None

    def steps(self): #Trả về 0 nếu số puzzle trong CLOSED > max_steps
        if len(self.CLOSED) - 1 > self.max_steps:
            return 0
        else:
            return self.path()

    def path(self):
       
        if not self.CLOSED:
            return
        goal_state = self.CLOSED[-1]  # Lấy trạng thái cuối cùng trong CLOSED (trạng thái đích)
        solution_path = [] # Danh sách để chứa các trạng thái từ init đến goal
        # Truy vết lại từ goal_state về trạng thái khởi đầu
        current_puzzle = goal_state
        while current_puzzle:
            solution_path.append(current_puzzle)
            current_puzzle = current_puzzle.parent  # Lấy trạng thái cha (parent)
        # Đảo ngược danh sách solution_path để in từ init đến goal
        solution_path.reverse()
        return len(solution_path) - 1
            
    
        

    def flat_To_Value_Puzzle(self, value):
        matrix_3x3 = []

        # Chia danh sách `value` thành các hàng con với mỗi hàng có 3 phần tử
        for i in range(0, len(value), 3):
            row = value[i:i+3]  # Lấy 3 phần tử liên tiếp từ danh sách value
            matrix_3x3.append(row)  # Thêm hàng này vào ma trận

        return matrix_3x3
    

