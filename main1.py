import pygame 
import math
import queue
class point:
    def __init__(self, x,y,old=None):
        self.x = x
        self.y = y
        self.G = 0
        self.H = 0
        self.old = old
#thư viện pygame
    def __gt__(self, other):
        if self.G + self.H >= other.G + other.H:
            return True
        else:
            return False
class smallbox:
    basecolor = (255,255,255)
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self,win):
        pygame.draw.rect(win,(0,0,0),(self.x,self.y,5,5))
        pygame.draw.rect (win,self.basecolor,(self.x+1,self.y+1,3,3))
    def change(self,state): #khai báo các màu cho bài toán mê cung
        if state == "obs":
            self.basecolor=(34, 59, 245) #màu của chướng ngại vật xanh blue
        elif state == "sou":
            self.basecolor = (162, 50, 168) #màu của điểm xuất phát tím
        elif state == "dis":
            self.basecolor = (255,0,0) #màu ô cần tìm đỏ
        elif state == "check":
            self.basecolor = (245, 245, 34) #màu của các ô đã được duyệt vàng
        elif state == "road":
            self.basecolor = (224, 123, 57) # màu của tuyến đường tốt nhất da cam
        elif state == "uncheck":
            self.basecolor = (0,255,0) #màu của mấy ô đang chờ duyệt màu xanh lá cây
class Cell:
    def __init__(self, value):
        self.value = value
    def change(self,state):
        self.value = state
class makeMatrix: #thủ tục để tạo ra 1 mảng ma trận ban đầu
    def __init__(self,size):
        self.matrix=[]
        self.size = size
        self.start = point(0,0)
        self.end = None
        self.n = size[0]//5
        self.m = size[1]//5
        self.E= [[0 for _ in range(200)] for _ in range (200)]
        self.sets= queue.PriorityQueue()
        self.isFind = True
        for i in range(0, size[0]+5,5):
            b=[]
            for j in range(0,size[1]+5,5):
                b.append(smallbox(i,j))
            self.matrix.append(b) #A*
    def drawEnd (self, mousepos): #hàm này để vẽ ra điểm kết thúc tức điểm chúng ta cần tìm
        x = mousePos[0] //5
        y = mousePos[1] //5
        self.matrix[x][y].change("dis")
        self.matrix[x][y].draw(win)
        self.start = point(x,y)
        self.E[x][y] = 0
        t = [1,0,-1]
        for i in range (0,3):
            for j in range(0, 3):
                self.E[x + t[i]][y + t[j]].change("dis")
                self.matrix[x + t[i]][y + t[j]].draw(win)
    def drawStart(self, mousepos): # hàm để vẽ ra điểm kết thúc ức điểm chúng ta cần tìm
        x=mousepos[0] //5
        y=mousepos[1] //5
        self.matrix[x][y].change("sou")
        self.matrix[x][y].draw(win)
        self.start = point(x,y)
        self.E[x][y] = 0
        t = [1,0,-1]
        for i in range (0,3):
            for j in range(0, 3):
                self.E[x + t[i]][y + t[j]].change("sou")
                self.matrix[x + t[i]][y + t[j]].draw(win)
        self.sets.put(self.start)
    def drawSE(self): # vẽ ra điểm đầu tien xuất phát tại mê cung
        self.matrix[self.start.x][self.start.y].draw(win)
        x = self.start.x
        y = self.start.y
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range (0, 3):
                self.matrix[x + t[i]][y + t[j]]. change("sou")
                self.matrix[x + t[i]][y + t[j]].draw(win)
    def draw(self, win , mouse,mousePos): #hàm để vexc chướng ngại vật cho mê cung thông qua chuột phải
        if mouse[0]:
            x=mousePos[0]//5
            y= mousePos[1]//5
            self.matrix[x][y].change("obs")
            self.matrix[x][y].draw(win)
            self.E[x][y]=-1
            t=[1,0,-1]
            for i in range (0,3):
                for j in range (0, 3):
                    self.E[x+t[i]][y+t[j]] = -1
                    self.matrix[x+t[i]][y + t[j]].change("obs")
                    self.matrix[x + t[i]][y + t[j]].draw(win)
    def drawF(self,win):
        for i in range (0, self.size[0]//5+1):
            for j in range(0, self.size[1]//5 +1):
                self.matrix[i][j].draw(win)
    def solve (self, win): #nơi chứa thuật toán A* chính
        self.drawSE()
        t = [1,0,-1]
        for i in range (0,3):
            for j in range (0,3):
                self.E[self.end.x + t[i]][self.end.y + t[j]] =0
                self.matrix[self.end.x + t[i]][self.end.y + t[j]].change("dis")
                self.matrix[self.end.x + t[i]][self.end.y + t[j]].draw(win)
                self.E[self.end.x][self.end.y]=0
        if self.isFind==False:
            return
        #print(self.isFind)
        p1=[0,0,1,-1]
        p2=[1,-1,0,0]
        k=self.sets.get()
        self.matrix[k.x][k.y].change("check") # duyệt qua các ô thì các ô sẽ chuyển sang màu vàng
        self.matrix[k.x][k.y].draw(win)
        for i in range(4):
            x=k.x + p1[i]
            y=k.y +p2[i]
            if x<0 or x>=self.n:
                continue
            if y<0 or y>=self.m:
                continue
            if self.E[x][y]==-1:
                continue
            temp=point(x,y,k)
            temp.G=k.G+1
            temp.H=math.sqrt(pow(x-self.end.x,2)+pow(y+self.end.y,2))
            self.E[x][y]=-1
            self.sets.put(temp)
            self.matrix[x][y].change("uncheck") #các ô đang trong trạng thái chờ duyệt
            self.matrix[x][y].draw(win)
            if temp.H == 0:
                self.isFind=False
                while temp is not None:
                    self.matrix[temp.x][temp.y].change('road' ) # vẽ ra tuyến đường tốt nhất
                    self.matrix[temp.x][temp.y].draw(win)
                    temp=temp.old
                self.matrix[self.start.x][self.start.y].draw(win)
                self.matrix[x][y].change("dis") #tọa đồ các điểm cần tìm
                self.matrix[x][y].draw(win)
size=(1000,1000) #khai báo giao diện và chạy chương trình
win=pygame.display.set_mode(size)
isRun = True
clock=pygame.time.Clock()
M=makeMatrix(size)
M.drawF(win)
bf=False
while isRun:
    #win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRun=False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: #gán nút các cho phép chạy thuật toán
        bf = True
    
    mouse= pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    if keys[pygame.K_s]: # gán nút s cho phép vẽ ra vị trí bắt đầu cần tìm theo vị trí chuột
        M.drawStart(mousePos)
    if keys[pygame.K_d]: # gán nút s cho phép vẽ ra vị trí bắt đầu cần tìm theo vị trí chuột
        M.drawEnd(mousePos)
            
    M.draw(win,mouse,mousePos)
    if bf:
        M.solve(win)
    pygame.display.flip()
