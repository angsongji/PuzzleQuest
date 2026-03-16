import copy

class Puzzle:
    def __init__(self, parent, value):
        """
        Hàm khởi tạo trạng thái với 2 tham số
        - parent: trạng thái cha của trạng thái hiện tại
        - value: giá trị của trạng thái hiện tại (ma trận 3x3)
        - value có giá trị là mảng lồng mảng như giá trị goal bên dưới
        """
        self.goal = [
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        ]
        self.parent = parent if parent is not None else None  # Cha của trạng thái hiện tại
        self.v_puzzle = value if value is not None else [[0] * 3 for _ in range(3)]  # Giá trị của trạng thái hiện tại
        self.g_puzzle = 0 if parent is None else parent.g_puzzle + 1  # Giá trị g của trạng thái
        self.h_puzzle = self.h_cost()  # Giá trị h của trạng thái
        self.f_puzzle = self.g_puzzle + self.h_puzzle  # Giá trị f của trạng thái

    def is_goal(self):
        """
        Hàm kiểm tra trạng thái hiện tại có phải là trạng thái đích hay không
        """
        return self.v_puzzle == self.goal

    def h_cost(self):
        """
        Hàm tính giá trị h cho puzzle = số sự khác nhau giữa trạng thái hiện tại và trạng thái đích
        """
        different = 0 #Khởi tạo số sự khác nhau = 0 hay h = 0
        for i in range(3):
            for j in range(3): #Vòng lặp qua giá trị của mỗi hàng trong puzzle
                if self.v_puzzle[i][j] != 0 and self.v_puzzle[i][j] != self.goal[i][j]: 
                    #Nếu giá trị đang xét không phải là ô trống và giá trị đó khác giá trị ở vị trí tương ứng trong goal
                    different += 1 #Cập nhật số sự khác nhau thêm 1
        return different #Sau khi kết thúc vòng lặp trả về số sự khác nhau

    def copy_v_puzzle(self):
        #Hàm sao chép giá trị của trạng thái hiện tại và trả về trạng thái mới (bản sao)
        new_value = copy.deepcopy(self.v_puzzle)  
        return Puzzle(self.parent, new_value)
    

    def compare_v_puzzle(self, puzzle):
        #Hàm kiểm tra giá trị của puzzle hiện tại, với puzzle nào đó có cùng giá trị?
        return self.v_puzzle == puzzle.v_puzzle

    def __lt__(self, other):
        '''
        Hàm __lt__ được gọi khi Python cần so sánh hai đối tượng của lớp này bằng toán tử <
        Ví dụ, nếu bạn viết obj1 < obj2, Python sẽ gọi obj1.__lt__(obj2) để thực hiện so sánh.
        Hàng đợi ưu tiên (như queue.PriorityQueue hoặc heapq trong Python) sử dụng toán tử < để sắp xếp các phần tử.
        '''
        return self.f_puzzle < other.f_puzzle  # So sánh dựa trên f_puzzle
