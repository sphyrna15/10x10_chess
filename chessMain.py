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
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages() #load images only once before while loop

    running = True
    selected_sq = () # no square selected initially, tuple (row, col)
    player_clicks = [] # keep track of clicks, max two tuples [(r1, c1), (r2, c2)]
    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
        
            # mouse event handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) coordinates of mouse
                col = location[0] // sq_size # // double divide to get integers
                row = location[1] // sq_size
                if selected_sq == (row, col): #user clicks same square twice
                    selected_sq = ()
                    player_clicks = []
                else:
                    selected_sq = (row, col)
                    player_clicks.append(selected_sq) #append both 1st and 2nd click
                if len(player_clicks) == 2: #2nd click
                    move = chessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i]) # make move if it is valid
                            moveMade = True
                            print("White to Move? - " + str(gs.whiteToMove))
                            selected_sq = () # reset selected player squares
                            player_clicks = []
                            break
                    if not moveMade:
                        player_clicks = [selected_sq]
                
            # key event handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # 'z' Key to undo move
                    gs.undoMove()
                    selected_sq = () # reset selections
                    player_clicks = []
                    moveMade = True

        if moveMade: #only generate new valid move list if a valid move was actually made
            validMoves = gs.getValidMoves()
            moveMade = False

        # draw game
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
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


#draw pieces on top of board
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            #specials = ["we", "wc", "wh", "wa", "wm", "wu", "bu", "be", "bc", "bh", "ba", "bm"]
            piece = board[r,c]
            if piece != "--": # not empty square
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    


if __name__ == "__main__":
    main()