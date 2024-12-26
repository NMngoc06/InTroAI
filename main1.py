import pygame
import math
import queue
from collections import deque
import time

class Point:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.G = 0  
        self.H = 0  
        self.parent = parent

    def __gt__(self, other):
        return (self.G + self.H) >= (other.G + other.H)


class SmallBox:
    base_color = (255, 255, 255)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "empty"  # Default state

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, 10, 10))  
        pygame.draw.rect(win, self.base_color, (self.x + 1, self.y + 2, 6, 6))  

    def change(self, state):
        self.state = state
        if state == "obs":
            self.base_color = (34, 59, 245)  
        elif state == "sou":
            self.base_color = (162, 50, 168)
        elif state == "dis":
            self.base_color = (255, 0, 0)  
        elif state == "check":
            self.base_color = (245, 245, 34)  # Màu điểm đã kiểm tra
        elif state == "road":
            self.base_color = (224, 123, 57)  
        elif state == "uncheck":
            self.base_color = (0, 255, 0)  # Màu điểm chờ duyệt
        elif state == "dfs_road":
            self.base_color = (255, 105, 180)  # Hồng
        elif state == "bfs_road":
            self.base_color = (0, 0, 0)  # Đen


class Matrix:
    def __init__(self, size):
        self.matrix = []
        self.size = size
        self.start = None
        self.end = None
        self.n = size[0] // 10  
        self.m = size[1] // 10
        self.E = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.sets = queue.PriorityQueue()
        self.stack = []
        self.queue = deque()
        self.is_find = True
        self.a_star_path = []
        self.dfs_path = []
        self.bfs_path = []
        self.a_star_time = 0
        self.bfs_time = 0
        self.dfs_time = 0

        for i in range(0, size[0] + 10, 10):
            row = []
            for j in range(0, size[1] + 10, 10):
                row.append(SmallBox(i, j))
            self.matrix.append(row)

    def draw_end(self, mouse_pos, win):
        x = mouse_pos[0] // 10
        y = mouse_pos[1] // 10
        self.matrix[x][y].change("dis")
        self.matrix[x][y].draw(win)
        self.end = Point(x, y)

    def draw_start(self, mouse_pos, win):
        x = mouse_pos[0] // 10
        y = mouse_pos[1] // 10
        self.matrix[x][y].change("sou")
        self.matrix[x][y].draw(win)
        self.start = Point(x, y)
        self.sets.put(self.start)

    def draw_obstacles(self, win, mouse, mouse_pos):
        if mouse[0]:
            x = mouse_pos[0] // 10
            y = mouse_pos[1] // 10
            self.matrix[x][y].change("obs")
            self.matrix[x][y].draw(win)
            self.E[x][y] = -1

    def draw_all(self, win):
        for row in self.matrix:
            for box in row:
                box.draw(win)

    def reset_search(self):
        """Reset lại ma trận nhưng giữ nguyên điểm đầu, điểm cuối và chướng ngại vật."""
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j].state not in ["obs", "sou", "dis"]:
                    self.E[i][j] = 0
                    self.matrix[i][j].base_color = SmallBox.base_color
        if self.start:
            self.matrix[self.start.x][self.start.y].change("sou")
        if self.end:
            self.matrix[self.end.x][self.end.y].change("dis")

        self.sets = queue.PriorityQueue()
        self.stack = []
        self.queue = deque()
        self.a_star_path = []
        self.dfs_path = []
        self.bfs_path = []
        self.a_star_time = 0
        self.dfs_time = 0
        self.bfs_time = 0
        
        if self.start:
            self.sets.put(self.start)
            self.stack.append(self.start)
            self.queue.append(self.start)

    def solve_a_star(self, win):
        """Giải thuật A*."""
        start_time = time.time()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while not self.sets.empty():
            current = self.sets.get()

            if current.x == self.end.x and current.y == self.end.y:
                while current:
                    if self.matrix[current.x][current.y].state not in ["sou", "dis"]:
                        self.matrix[current.x][current.y].change("road")
                        self.a_star_path.append((current.x, current.y))
                    self.matrix[current.x][current.y].draw(win)
                    current = current.parent
                return

            self.matrix[current.x][current.y].change("check")
            self.matrix[current.x][current.y].draw(win)
            pygame.display.flip()

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < self.n and 0 <= ny < self.m and self.E[nx][ny] == 0:
                    neighbor = Point(nx, ny, current)
                    neighbor.G = current.G + 1
                    "neighbor.H = math.sqrt((nx - self.end.x) ** 2 + (ny - self.end.y) ** 2)"
                    neighbor.H = abs(nx - self.end.x) + abs(ny - self.end.y)
                    self.sets.put(neighbor)
                    self.E[nx][ny] = -1
                    self.matrix[nx][ny].change("uncheck")
                    self.matrix[nx][ny].draw(win)
            end_time = time.time()
            self.a_star_time = end_time - start_time 

    def solve_dfs(self, win):
        """Giải thuật DFS."""
        start_time = time.time()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while self.stack:
            current = self.stack.pop()

            if current.x == self.end.x and current.y == self.end.y:
                while current:
                    if self.matrix[current.x][current.y].state not in ["sou", "dis"]:
                        self.matrix[current.x][current.y].change("dfs_road")
                        self.dfs_path.append((current.x, current.y))
                    self.matrix[current.x][current.y].draw(win)
                    current = current.parent
                return

            self.matrix[current.x][current.y].change("check")
            self.matrix[current.x][current.y].draw(win)
            pygame.display.flip()

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < self.n and 0 <= ny < self.m and self.E[nx][ny] == 0:
                    neighbor = Point(nx, ny, current)
                    self.stack.append(neighbor)
                    self.E[nx][ny] = -1
                    self.matrix[nx][ny].change("uncheck")
                    self.matrix[nx][ny].draw(win)
            end_time = time.time()
            self.dfs_time = end_time - start_time 

    def solve_bfs(self, win):
        """Giải thuật BFS."""
        start_time = time.time()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while self.queue:
            current = self.queue.popleft()

            if current.x == self.end.x and current.y == self.end.y:
                while current:
                    if self.matrix[current.x][current.y].state not in ["sou", "dis"]:
                        self.matrix[current.x][current.y].change("bfs_road")
                        self.bfs_path.append((current.x, current.y))
                    self.matrix[current.x][current.y].draw(win)
                    current = current.parent
                return

            self.matrix[current.x][current.y].change("check")
            self.matrix[current.x][current.y].draw(win)
            pygame.display.flip()

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < self.n and 0 <= ny < self.m and self.E[nx][ny] == 0:
                    neighbor = Point(nx, ny, current)
                    self.queue.append(neighbor)
                    self.E[nx][ny] = -1
                    self.matrix[nx][ny].change("uncheck")
                    self.matrix[nx][ny].draw(win)
            end_time = time.time()
            self.bfs_time = end_time - start_time 

    def show_paths(self, win):
        """Hiển thị lại các đường đi của các thuật toán."""
        for x, y in self.a_star_path:
            self.matrix[x][y].change("road")
            self.matrix[x][y].draw(win)

        for x, y in self.dfs_path:
            self.matrix[x][y].change("dfs_road")
            self.matrix[x][y].draw(win)

        for x, y in self.bfs_path:
            self.matrix[x][y].change("bfs_road")
            self.matrix[x][y].draw(win)

    def calculate_lengths_and_display(self, win):
        """Tính toán và hiển thị độ dài quãng đường của các thuật toán."""
        font = pygame.font.Font(None, 30)

        a_star_length = len(self.a_star_path)
        dfs_length = len(self.dfs_path)
        bfs_length = len(self.bfs_path)

        texts = [
            f"A* Path Length: {a_star_length} | Time: {self.a_star_time:.4f}s",
            f"DFS Path Length: {dfs_length} | Time: {self.dfs_time:.4f}s",
            f"BFS Path Length: {bfs_length} | Time: {self.bfs_time:.4f}s"
        ]
        start_y = 20
        pygame.draw.rect(win, (255, 255, 255), (10, 10, 400, len(texts) * 30 + 10))

        for i, text in enumerate(texts):
            render = font.render(text, True, (0, 0, 0))
            win.blit(render, (15, 15 + i * 30))

pygame.init()
size = (1000, 1000)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinding Visualizer")
clock = pygame.time.Clock()

matrix = Matrix(size)
matrix.draw_all(win)

running = True
start_set = False
end_set = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if keys[pygame.K_s] and not start_set:  # Đặt điểm bắt đầu
        matrix.draw_start(mouse_pos, win)
        start_set = True

    if keys[pygame.K_e] and not end_set:  # Đặt điểm đích
        matrix.draw_end(mouse_pos, win)
        end_set = True

    if mouse[0]:  # Vẽ chướng ngại vật
        matrix.draw_obstacles(win, mouse, mouse_pos)

    if keys[pygame.K_r]:  # Reset
        matrix.reset_search()

    if keys[pygame.K_a]:  # Chạy A*
        matrix.reset_search()
        matrix.solve_a_star(win)

    if keys[pygame.K_d]:  # Chạy DFS
        matrix.reset_search()
        matrix.solve_dfs(win)

    if keys[pygame.K_b]:  # Chạy BFS
        matrix.reset_search()
        matrix.solve_bfs(win)

    if keys[pygame.K_SPACE]:  # Chạy tất cả thuật toán
        matrix.reset_search()
        matrix.solve_a_star(win)  # Chạy A*
        matrix.solve_dfs(win)     # Chạy DFS
        matrix.solve_bfs(win)     # Chạy BFS
        # Hiển thị lại các đường đi của A*, DFS và BFS
        matrix.show_paths(win)

    # Hiển thị độ dài quãng đường trên cửa sổ
    matrix.draw_all(win)
    matrix.calculate_lengths_and_display(win)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
