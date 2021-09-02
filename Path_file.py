import pygame
import math
from queue import PriorityQueue
from queue import Queue
LENGTH = 800
rows=100
WIN = pygame.display.set_mode((LENGTH, LENGTH))
Light_BLUE=(0,255,255)     #visited colour
GREEN=(0,255,0)   #nodes that are in queue in A*Algorithm
RED=(255,0,0)    #Start Point
BLACK=(0,0,0)     # Walls
WHITE=(255,255,255) #Empty Cells
DARK_BLUE=(0,0,255) #End Point
PURPLE=(255,0,255)  #path COlour
GREY=(128,128,128)   #Grid colour


class node:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col
        self.width=width
        self.total_rows=total_rows
        self.x=row*width
        self.y=col*width
        self.color=WHITE
        self.neighbours=[]

    def get_pos(self):
        return self.row,self.col

    def is_visited(self):
        return self.color==Light_BLUE

    def is_wall(self):
        return self.color== BLACK

    def is_border(self):
        return self.color==GREEN

    def is_start(self):
        return self.color==RED

    def is_end(self):
        return self.color==DARK_BLUE

    def reset(self):
        self.color = WHITE
        self.neighbours=[]

    def make_visited(self):
        self.color=Light_BLUE

    def make_wall(self):
        self.color=BLACK

    def make_border(self):
        self.color=GREEN

    def make_start(self):
        self.color=RED

    def make_end(self):
        self.color=DARK_BLUE
    def make_path(self):
        self.color=PURPLE
    def make_empty(self):
        self.color=WHITE
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def neighbour(self,grid):
        if self.row+1<self.total_rows and not grid[self.row+1][self.col].is_wall():
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row-1>=0 and not grid[self.row-1][self.col].is_wall():
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col+1<self.total_rows and not grid[self.row][self.col+1].is_wall():
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col-1>=0 and not grid[self.row][self.col-1].is_wall():
            self.neighbours.append(grid[self.row][self.col-1])
    def __lt__(self, other):
        return False


def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)
def make_grid(rows,width):     #total rows required , width of screen
    grid=[]
    gap= width //rows
    for i in range(rows):
        rw=[]
        for j in range(rows):
            nd= node(i,j,gap,rows)
            rw.append(nd)
        grid.append(rw)
    return grid
def draw_grid(win,width,rows):
    gap= width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
    for j in range(rows):
        pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))



def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for nd in row:
            nd.draw(win)
    draw_grid(win, width, rows)
    pygame.display.update()

def get_clicled_pos(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

def algorithm(draw,grid,start,end):
    qu=PriorityQueue()
    qu.put((0,start))
    par={}
    g_score={}
    f_score={}
    for rws in grid:
        for nd in rws:
            g_score[nd]= float("inf")
            f_score[nd]=float("inf")
    g_score[start]=0
    f_score[start]=h(start.get_pos(),end.get_pos())
    while not qu.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        current = qu.get()[1]
        current.make_visited()
        if current==end:
            while current!=start:
                current=par[current]
                current.make_path()
                draw()
            start.make_start()
            end.make_end()
            return True
        for neighbour in current.neighbours:
            temp_g_score = g_score[current]+1
            if g_score[neighbour]>temp_g_score:
                g_score[neighbour]=temp_g_score
                par[neighbour]=current
                f_score[neighbour]=temp_g_score+h(neighbour.get_pos(),end.get_pos())
                if not neighbour.is_visited():
                    qu.put((f_score[neighbour],neighbour))
                    neighbour.make_border()
        draw()
        if current!=start:
            current.make_visited()
    return False
def bfs(draw,grid,start,end):
    qu=Queue()
    qu.put(start)
    par={}
    while not qu.empty():
        draw()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        current= qu.get()
        if current==end:
            while current!=start:
                current=par[current]
                current.make_path()
                draw()
            start.make_start()
            end.make_end()
            return True
        for neighbour in current.neighbours:
            if neighbour.is_visited():
                continue
            qu.put(neighbour)
            neighbour.make_border()
            par[neighbour]=current
        current.make_visited()
    return False
def main(win,width,rws):
    ROWS=rws
    grid=make_grid(ROWS,width)
    start =None  #starting position
    end=None  #ending Position
    run = True
    completed=False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if pygame.mouse.get_pressed()[0] and not completed:  #left click it will select the node as start or end or wall
                pos=pygame.mouse.get_pos()
                row,col=get_clicled_pos(pos,ROWS,width)
                nd=grid[row][col]
                if not start and nd!=end :
                    start=nd
                    start.make_start()
                elif not end and nd!=start:
                    end=nd
                    end.make_end()
                elif nd!=start and nd!=end:
                    nd.make_wall()
            elif pygame.mouse.get_pressed()[2] and not completed:  #right click it will reset the node
                pos=pygame.mouse.get_pos()
                row,col=get_clicled_pos(pos,ROWS,width)
                nd=grid[row][col]
                if nd.is_end():
                    end=None
                if nd.is_start():
                    start=None
                nd.make_empty()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a and not completed:
                    for rows in grid:
                        for nd in rows:
                            nd.neighbour(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    completed=True
                if event.key==pygame.K_b and not completed:
                    for rows in grid:
                        for nd in rows:
                            nd.neighbour(grid)
                    bfs(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    completed=True
                if event.key==pygame.K_r:
                    start=None
                    end=None
                    for rw in grid:
                        for nd in rw:
                            nd.reset()
                    completed=False


    pygame.quit()

main(WIN,LENGTH,rows)