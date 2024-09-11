import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

#colors use RGB, 8bit per a color => 2^8 - 1=255
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        #coordinates are in pixels => *width
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbours = []
        self.total_rows = total_rows
        
    #is functions return True/False    
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    # make functions change a color  
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    #draws a rectangle 
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    
    def update_neighbors(self, grid):
        self.neighbors = []
        #if our row isn't the last row and there is no barrier below, then there is an empty square below 
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #down
            self.neighbors.append(grid[self.row + 1][self.col])
        #if we aren't at row 0 and there is no barrier above us, then there is an empty square above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #up
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #right
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #left
            self.neighbors.append(grid[self.row][self.col - 1])
            
            
    #comparison of two spots
    def __lt__(self, other):
        #lt stands for "less than"
        return False
    

'''
A heuristic function calculates an approximate cost to a problem
It's easy and quick to calculate
Example: finding a shortest driving distance to a point => 
=> heuristic cost would be a straight line distance to the point
f() = g() + h()
The term admissible means, that a specific heuristic func. never overestimates the true cost
'''
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #abs = absolute / here it is an absolute distance
    return abs(x1 - x2) + abs(y1 - y2)
    
    
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
    
    
    
'''
MAIN ALGORITHM
--Hash is an integer which identifies a particular value 
--example: hash('A*') -> 111 and f = 'A*' -> hash(f) -> 111

count - tracks how many neighbors we have 

We start from puting the start node into open_set

came_from keeps track of where we came from, so we can find the best path in the end

g_score track the current shortest distance from the start to this node to the end node
we initialize them from infinity to start and set g_score of start to be 0

f_score keeps track of the predicted distance from this node to the end node 
'''
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    #g_score of each spot is inf. 
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    #f_score of each spot is inf. 
    f_score = {spot: float('inf') for row in grid for spot in row} 
    #make an estimate of how far the start node is from the end node
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    '''
    keeps track of all of the items in the priority queue 
    we can check if anything is in it
    helps to see us if anything is in our open set, since it is a queue
    '''
    open_set_hash = {start} 
    
    #while open_set is empty check that we are't quiting the game
    #if it isn't, then we end the game
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #the priority queue is an efficient way of getting the smallest element everytime from it 
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        #take the current shortest distance to the closest node 
        #and +1 since we look at the closest neighbor of this node      
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            #if we found a shorter way, then we update the path 
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current 
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        
        if current!=start:
            current.make_closed()
    #if we didn't find the path        
    return False
     
    
    
    
    #creates empty rectangles on our window / grid = клетка ("тетрадная") 
def make_grid(rows, width):
    grid = []
    #what the gap between rows is / what is the width of each cube
    gap = width // rows
    #create a 2D list 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

#draws grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        #draw a horizontal line for each row
        # (0, i*gap)-start of the line / (width, i*gap)-end of the line
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        #shift along x axis and draw each vertical line 
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))
        

def draw(win, grid, rows, width):
    #paint all over the canvas with one color
    win.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
     
    draw_grid(win, rows, width)
    #python takes what we have just drawn and projects it onto a display
    pygame.display.update()
    

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    #figures out where do we click
    row = y // gap
    col = x // gap 
    
    return row, col

#all of the collision checks and the main algorithm
def main(win, width):
    ROWS = 50 
    grid = make_grid(ROWS, width)
    #tracks the positions of start and end
    start = None
    end = None
    #tracks if we have finished the algorithm or not 
    run = True
    started = False
    while run:
        #in the beginning of each while loop...
        #loops over all of the events which happened and checks what they are
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if started:
                #when algorithm is started, then you cannot press anything except the exit
                continue
                
            if pygame.mouse.get_pressed()[0]: #left mouse
                pos = pygame.mouse.get_pos()
                #where did we click
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot!=end:
                    start = spot
                    start.make_start()
                
                elif not end and spot!=start:
                    end = spot
                    end.make_end()
                    
                elif spot!=end and spot!=start:
                    spot.make_barrier()
        
            elif pygame.mouse.get_pressed()[2]: #right mose 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                #press on the spot with right mouse => reset it to be white
                spot.reset()
                if spot==start:
                    start = None
                elif spot==end:
                    end = None
            
            #when we press the key down, this key is space and the algorithm hasn't been started
            #then for all the spots in the row we update the neighbors
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    #when we start, we call the algorithm func.
                    #we pass into it: a func. that is equal to the function call, grid, start and end
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                
    pygame.quit()
    
main(WIN, WIDTH)