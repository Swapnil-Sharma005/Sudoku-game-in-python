import pygame  # pygame module for GUI
from pygame.locals import * 
from pygame import mixer 
import requests 
pygame.init() 

import sys
sys.setrecursionlimit(3000)

window = pygame.display.set_mode((550,550))
BACKGROUND_COLOR = (251,247,245)
window.fill(BACKGROUND_COLOR)
pygame.display.flip()
pygame.display.set_caption("SUDOKU GAME")

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']


grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

global block_size
block_size = 50
value = 0

prepos = [0,0]
clicked = False

mixer.init()
mixer.music.set_volume(0.7)


def Drawing_Grid(window,block_size,grid):
    for i in range(0,10):
        k=2
        if i%3==0:
            k=4
        pygame.draw.line(window,(0,0,0),(block_size + block_size*i,block_size),(block_size + block_size*i,550-block_size),k)
        pygame.draw.line(window,(0,0,0),(block_size,block_size + block_size*i),(550-block_size,block_size + block_size*i),k)
        pygame.display.update()

    font_color = (0,150,250)
    font = pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",25)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]!=0:
                text_object = font.render(str(grid[i][j]),True,font_color)
                window.blit(text_object,((j+1)*50 +15,(i+1)*50))
                pygame.display.update()
    
    #drawing buttons
    Resetbutton.draw_button()
    AutoSolvebutton.draw_button()
    undobutton.draw_button()
    pygame.display.update()

class button():

    width = 100
    height = 30
    
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
    
    def draw_button(self):

        global clicked
        action = False

        pos = pygame.mouse.get_pos() # gets the mouse position

        button_rect = Rect(self.x,self.y,self.width,self.height) # pygame rect object for the button

        # checking mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(window, (95,158,160), button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(window, (176,224,230), button_rect)
        else:
            pygame.draw.rect(window, (0,206,209), button_rect)

        #add text to button
        font = pygame.font.SysFont('Constantia', 13)
        text_img = font.render(self.text, True, (255,255,255))
        text_len = text_img.get_width()
        window.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + (self.height/2-text_img.get_height()/2)))
        
        return action

Resetbutton = button(15+100,10,"Rest")
AutoSolvebutton   = button(125+100,10,"AutoSolve")
undobutton = button(235+100,10,"Undo")

def Reset():
    global grid
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    grid = response.json()['board']
    global grid_original
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    window.fill(BACKGROUND_COLOR)
    Drawing_Grid(window,block_size,grid)
    return 

def isvalidkey(key,pos,grid=grid):

    j = pos[1]
    i = pos[0]
    #check for row:
    for k in range(0,len(grid[0])):
        if grid[i][k] == key and k!=j:
            return False
    #check for column:
    for k in range(0,len(grid)):
        if grid[k][j] == key and k!=i:
            return False
    #check for box:
    boxi = i//3 
    boxj = j//3
    
    for p in range(boxi*3,boxi*3+3):
        for l in range(boxj*3,boxj*3+3):
            if grid[p][l]==key and (p!=i and l!=j ):
                return False
    return True

def emptycell(gird = grid):

    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j]==0:
                return (i,j)
    return False


def Autosolve(grid):

    font = pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",25)
    grid = grid 

    find = emptycell(grid)

    if not find:
        return True
    else:
        i,j = find
    
    values = [1,2,3,4,5,6,7,8,9]
    for k in iter(values):
        if isvalidkey(k,(i,j),grid):
            grid[i][j] = k
            pygame.draw.rect(window, BACKGROUND_COLOR, ((j+1)*50+5, (i+1)*50+5,40 , 40))
            value = font.render(str(k), True, (0,0,0))
            window.blit(value, ( (j+1)*50 +15, (i+1)*50))
            pygame.display.update()

            if Autosolve(grid):
                return True
            
            grid[i][j]=0
            pygame.draw.rect(window, BACKGROUND_COLOR, ((j+1)*50+5, (i+1)*50+5,40 , 40))
            pygame.display.update()

    
    return False 

def user_insert(window,pos,prepos=prepos):
    i = pos[1]//50
    j = pos[0]//50
    
    font = pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",25)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                return
            if event.type == pygame.KEYDOWN:

                if (grid[i-1][j-1] != 0):
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    key = event.key-48
                    if isvalidkey(key,(i-1,j-1),grid):
                       pygame.draw.rect(window, BACKGROUND_COLOR, (j*50+5, i*50+5,40 , 40))
                       value = font.render(str(event.key-48), True, (0,0,0))
                       window.blit(value, ( j*50 +15, i*50))
                       grid[i-1][j-1] = event.key - 48
                       prepos[0] = pos[0]
                       prepos[1] = pos[1]
                       pygame.display.update()
                       return
                    
                    else:
                       pygame.draw.rect(window, BACKGROUND_COLOR, (j*50+5, i*50+5,40 , 40))
                       value = font.render(str(event.key-48), True, (255,0,0))
                       window.blit(value, ( j*50 +15, i*50))
                       mixer.music.load("error sound.wav")
                       mixer.music.play()
                       grid[i-1][j-1] = event.key - 48
                       prepos[0] = pos[0]
                       prepos[1] = pos[1]
                       pygame.display.update()
                       return

            return

def undofun(prepos):
    print(prepos)

    j = prepos[0]//50
    i = prepos[1]//50
    grid[i-1][j-1]=0
    pygame.draw.rect(window, BACKGROUND_COLOR, (j*50+5, i*50+5,40 , 40))
    pygame.display.update()
    return 


def main():  
    
    Drawing_Grid(window,block_size,grid)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                pos = pygame.mouse.get_pos()
                user_insert(window,pos)

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if Resetbutton.draw_button():
                Reset()

            if AutoSolvebutton.draw_button():
                if Autosolve(grid):
                    mixer.music.load("game solve.mp3")
                    mixer.music.play()

            if undobutton.draw_button():
                undofun(prepos)
            
           
       

if __name__ == "__main__":
    main()
