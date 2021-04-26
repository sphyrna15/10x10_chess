"""
Main driver file responsible for handling user input and displaying the current GameState object
"""

import chessEngine
import pygame as p


width = height = 1000 #512 another option
dimension = 10 #dimension of 10x10 chess
sq_size = height // dimension 
max_fps = 100 #for animations later
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
    animate = False #flag variable which moves are to be animated

    loadImages() #load images only once before while loop

    running = True
    gameOver = False # Game is over flag
    selected_sq = () # no square selected initially, tuple (row, col)
    player_clicks = [] # keep track of clicks, max two tuples [(r1, c1), (r2, c2)]
    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
        
            # mouse event handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
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
                                animate = True #only animate made moves
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
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # resets the board with 'r' Key
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    selected_sq = ()
                    player_clicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if moveMade: #only generate new valid move list if a valid move was actually made
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock) #animate move
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        # draw game
        drawGameState(screen, gs, validMoves, selected_sq)
        if gs.isCheckMate:
            gameOver = True
            if not gs.whiteToMove:
                drawText(screen, "White wins by Checkmate!")
            else:
                drawText(screen, "Balck wins by Checkmate!")
        if gs.isStaleMate:
            gameOver = True
            drawText(screen, "Stalemate!")
        
        clock.tick(max_fps)
        p.display.flip()



""" Draw the current Game State, responsible for all the graphics """

# Highlight possible moves for piece seleted
def highlightSquares(screen, gs, validMoves, selected_sq):
    if selected_sq != ():
        r, c = selected_sq
        if gs.board[r,c][0] == ('w' if gs.whiteToMove else 'b'): #making sure that selected piece can move
            #highlight selected square
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100) #transparency value (0 transparent, 255 full)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
            # highlight moves from that square
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow, move.endCol] != "--": #captures
                        s.fill(p.Color('red'))
                        screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))
                    else: #empty square
                        s.fill(p.Color('yellow'))
                        screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))



def drawGameState(screen, gs, validMoves, selected_sq):
    drawBoard(screen) #draw squares on board
    highlightSquares(screen, gs, validMoves, selected_sq)
    drawPieces(screen, gs.board) #draw pieces in appropirate places


#draw board with squares and coloring (REMEMBER: top left quare light)
def drawBoard(screen):
    # dark squares have odd parity, light suqares have even parity
    # thus r + c mod 2 will tell us the color of the square
    global colors #make colors global variable to use in animateMove()
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

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Blue'))
    textLocation = p.Rect(0,0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Red'))
    screen.blit(textObject, textLocation.move(2,2))



# Move Animation
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coordinates where animation will move through
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framesPerSquare = 3 ########### frames to move one square - HOW FAST IS THE ANIMATION ############
    frameCount = (abs(dr) + abs(dc)) * framesPerSquare
    for frame in range(frameCount +1):
        #get coordinates for piece to fly through
        coords.append((move.startRow + dr*frame/frameCount, move.startCol + dc*frame/frameCount))
        r, c = (move.startRow + dr*frame/frameCount, move.startCol + dc*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase piece moved from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare) #erase piece
        #draw captured piece into rectangle
        if move.captured_piece != "--":
            screen.blit(images[move.captured_piece], endSquare)
        #draw moving piece
        screen.blit(images[move.moved_piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(90) ######### HOW FAST IS THE ANIMATION ############



    


if __name__ == "__main__":
    main()