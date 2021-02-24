"""
Main driver file responsible for handling user input and displaying the current GameState object
"""

import chessEngine
import pygame as p


width = height = 1000 #512 another option
dimension = 10 #dimension of 10x10 chess
sq_size = height // dimension 
max_fps = 15 #for animations later
images = {}

# FUNCTIONS

""" 
Initialize a global directionary of images. 
this will be calles exactly once in the main
"""
def loadImages():
    
    #load piece images
    pieces = ["wp", "bp", "wr", "br", "wn", "wu", "wb", "wq",
             "wk", "bu", "bb", "bq", "bk", "be", "bc", "bn",
             "bh", "ba", "bm", "we", "wc", "wh", "wa", "wm"]

    for piece in pieces:
        #print(piece)
        images[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (sq_size, sq_size))
        

"""
Main Driver to handle user input and update graphics 
"""
def main():

    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = chessEngine.GameState() #initialize game state
    loadImages() #load images only once before while loop

    running = True
    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()



""" Draw the current Game State, responsible for all the graphics """


def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on board
    # possibly add in highlighting or move suggestions
    drawPieces(screen, gs.board) #draw pieces in appropirate places


#draw board with squares and coloring (REMEMBER: top left quare light)
def drawBoard(screen):
    # dark squares have odd parity, light suqares have even parity
    # thus r + c mod 2 will tell us the color of the square
    colors = [p.Color("white"), p.Color("brown")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


#draw pieces on top of board
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r,c]
            if piece != "--": # not empty square
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    


if __name__ == "__main__":
    main()