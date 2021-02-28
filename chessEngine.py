"""
This class will be responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state. It will also keep the move log.
"""

import numpy as np

class GameState():
    def __init__(self):
        
        self.board = np.array([ 
            ["be", "bc", "bh", "ba", "bm", "bm", "ba", "bh", "bc", "be"],
            ["br", "bn", "bu", "bb", "bq", "bk", "bb", "bu", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wu", "wb", "wq", "wk", "wb", "wu", "wn", "wr"],
            ["we", "wc", "wh", "wa", "wm", "wm", "wa", "wh", "wc", "we"]])

        self.moveLog = []
        self.whiteToMove = True
        # dictionary to keep track of piece function names 
        self.moveFunctions = {'p': self.pawnMoves, 'r': self.rookMoves, 'n': self.knightMoves, 'u': self.unicornMoves, 
                            'b': self.bishopMoves, 'q': self.queenMoves, 'k': self.kingMoves, 'e': self.eagleMoves, 
                            'c': self.cardinalMoves, 'h': self.hammerMoves, 'a': self.arrowMoves, 'm': self.ministerMoves}
    
    # Will not work for casteling, en passant capture and pawn promotion
    def makeMove(self, move):
        self.board[move.startRow, move.startCol] = "--" #leave behind blank space
        self.board[move.endRow, move.endCol] = move.moved_piece #move piece to new location
        self.moveLog.append(move) #track move
        self.whiteToMove = not self.whiteToMove #switch players

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() #gets last element and removes
            self.board[move.startRow, move.startCol] = move.moved_piece #put moved piece back at start
            self.board[move.endRow, move.endCol] = move.captured_piece #put catured piece back in place
            self.whiteToMove = not self.whiteToMove

    
    # Get All actually Valid Moves for the player (considering checks)
    def getValidMoves(self):
        return self.getPossibleMoves()
    

    # Get All Possible moves for a player (not considering checks)
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of colums (correct implementation for 2dim list)

                turn = self.board[r,c][0] # colour of piece on square - need to check it?
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r,c][1]
                    self.moveFunctions[piece](r, c, moves) #calls appropriate move functions current pos

        return moves
    



    """
    Generate all possible moves for each piece
    """
    def pawnMoves(self, r, c, moves):
        if self.whiteToMove: #handle white pawn moves first
            if self.board[r-1, c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                if self.board[r-2, c] == "--" and r == 7: # base row 2 square pawn advance
                    moves.append(Move((r,c), (r-2,c), self.board))
            # white pawn captures:
            if c-1 >= 0: #left capture
                if self.board[r-1, c-1][0] == 'b': #black piece to capture
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 9: #right capture
                if self.board[r-1, c+1][0] == 'b': 
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        
        if not self.whiteToMove: # black pawn moves
            if self.board[r+1, c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if self.board[r+2, c] == "--" and r == 2: #base row 2 square pawn advance
                    moves.append(Move((r,c), (r+2,c), self.board))
            #black bawn captures:
            if c-1 >= 0: #left capture
                if self.board[r+1, c-1][0] == 'w': #white piece to capture
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 <= 9: #right capture
                if self.board[r+1, c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
            
        # still need to handle en passant and promotion
        



    def rookMoves(self, r, c, moves):
        """ movement down """
        row = r + 1 #iteration variable
        while row < 10:
            # black rook captures white piece:
            bcapt = (self.board[row, c][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, c][0] == 'b' and self.whiteToMove) 
            if self.board[row, c] == "--": # check if empty square to move
                moves.append(Move((r,c), (row, c), self.board))
            elif wcapt or bcapt:
                moves.append(Move((r,c), (row,c), self.board))
                break
            else: # if none of the above - one of our pieces blocks the way
                break
            row += 1
        """ movement up """
        row = r - 1 # new iteration variable
        while row >= 0:
            # black rook captures white piece:
            bcapt = (self.board[row, c][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, c][0] == 'b' and self.whiteToMove)
            if self.board[row, c] == "--": # check if empty square to move
                moves.append(Move((r,c), (row, c), self.board))
            elif wcapt or bcapt:
                moves.append(Move((r,c), (row,c), self.board))
                break
            else: # if none of the above - one of our pieces blocks the way
                break
            row -= 1
        """ movement to the right """
        col = c + 1 # interation variable
        while col < 10:
            # black rook captures white piece:
            bcapt = (self.board[r, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[r, col][0] == 'b' and self.whiteToMove)
            if self.board[r, col] == "--": #empty square to move to
                moves.append(Move((r,c), (r,col), self.board))
            elif wcapt or bcapt:
                moves.append(Move((r,c), (r,col), self.board))
                break
            else:
                break
            col += 1
        """ movement to the left """
        col = c - 1 #new iteration variable
        while col >= 0:
            # black rook captures white piece:
            bcapt = (self.board[r, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[r, col][0] == 'b' and self.whiteToMove)
            if self.board[r, col] == "--": #empty square to move to
                moves.append(Move((r,c), (r,col), self.board))
            elif wcapt or bcapt:
                moves.append(Move((r,c), (r,col), self.board))
                break
            else:
                break
            col -= 1
    
    """ function to find possible moves from move reach list (for knights etc.) """
    def moveListSeach(self, r, c, moves, moveList):
        for square in moveList:
            if square[0] in range(10) and square[1] in range(10):
                # white piece
                if self.whiteToMove:
                    if self.board[square][0] != 'w':
                        moves.append(Move((r,c), square, self.board))
                    if self.board[square][0] != 'w':
                        moves.append(Move((r,c), square, self.board))
                # black piece
                else:
                    if self.board[square][0] != 'b':
                        moves.append(Move((r,c), square, self.board))
                    if self.board[square][0] != 'b':
                        moves.append(Move((r,c), square, self.board))

    
    def knightMoves(self, r, c, moves):
        # list possible locations for knight to jump to - reach:
        reach = [(r+2, c-1), (r+2, c+1), (r-2, c-1), (r-2, c+1), 
                (r+1, c+2), (r-1, c+2), (r+1, c-2), (r-1, c-2)]
        self.moveListSeach(r, c, moves, reach)


    def bishopMoves(self, r, c, moves):
        """ move up to the right """
        row = r+1 ; col = c+1 #iteration variables
        while row in range(10) and col in range(10):
            # black bishop captures white piece:
            bcapt = (self.board[row, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, col][0] == 'b' and self.whiteToMove)
            if self.board[row,col] == "--": # empty squares ok to move
                moves.append(Move((r,c), (row,col), self.board))
                row += 1 ; col+= 1
                continue
            elif bcapt or wcapt:
                moves.append(Move((r,c), (row,col), self.board))
                break
            else:
                break
        """ move up to the left """
        row = r+1 ; col = c-1 #iteration variables
        while row in range(10) and col in range(10):
            # black bishop captures white piece:
            bcapt = (self.board[row, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, col][0] == 'b' and self.whiteToMove)
            if self.board[row,col] == "--": # empty squares ok to move
                moves.append(Move((r,c), (row,col), self.board))
                row += 1 ; col-= 1
                continue
            elif bcapt or wcapt:
                moves.append(Move((r,c), (row,col), self.board))
                break
            else:
                break
        """ move down to the right """
        row = r-1 ; col = c+1 #iteration variables
        while row in range(10) and col in range(10):
            # black bishop captures white piece:
            bcapt = (self.board[row, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, col][0] == 'b' and self.whiteToMove)
            if self.board[row,col] == "--": # empty squares ok to move
                moves.append(Move((r,c), (row,col), self.board))
                row -= 1 ; col += 1
                continue
            elif bcapt or wcapt:
                moves.append(Move((r,c), (row,col), self.board))
                break
            else:
                break
        """ move down to the left """
        row = r-1 ; col = c-1 #iteration variables
        while row in range(10) and col in range(10):
            # black bishop captures white piece:
            bcapt = (self.board[row, col][0] == 'w' and not self.whiteToMove)
            # white rook captures black piece:
            wcapt = (self.board[row, col][0] == 'b' and self.whiteToMove)
            if self.board[row,col] == "--": # empty squares ok to move
                moves.append(Move((r,c), (row,col), self.board))
                row -= 1 ; col -= 1
                continue
            elif bcapt or wcapt:
                moves.append(Move((r,c), (row,col), self.board))
                break
            else:
                break



    def queenMoves(self, r, c, moves):
        # queen moves like a bishop + rook:
        self.bishopMoves(r, c, moves)
        self.rookMoves(r, c, moves)

    def kingMoves(self, r, c, moves):
        # list with square the king can reach
        reach = [(r+1, c), (r+1,c+1), (r+1,c-1), (r,c+1), (r,c-1),
                (r-1,c), (r-1,c+1), (r-1,c-1)]
        self.moveListSeach(r, c, moves, reach)
        

    def unicornMoves(self, r, c, moves):
        # can do all knight moves plus extra:
        self.knightMoves(r, c, moves)

        #extra moves:
        extras = [(r+3, c), (r-3, c), (r, c+3), (r, c-3)]
        self.moveListSeach(r, c, moves, extras)


    def eagleMoves(self, r, c, moves):
        # define reach of eagle - move 3 forward + 1 or 2 sideways
        reach = [(r+3, c+1), (r+3, c-1), (r+3, c+2), (r+3, c-2), #up
                (r-3, c+1), (r-3, c-1), (r-3, c+2), (r-3, c-2),  #down
                (r+1, c+3), (r-1, c+3), (r+2, c+3), (r-2, c+3),  #right
                (r+1, c-3), (r-1, c-3), (r+2, c-3), (r-2, c-3)]  #left
        # same logic as for king, knight and unicorn
        self.moveListSeach(r, c, moves, reach)

    """ cardinal and minister movement search function """
    def movingSearch(self, r, c, moves, updateIdx):
        row, col = updateIdx(r,c) # function that decides movement (index updates)
        skipped = False
        while row in range(10) and col in range(10):
            wskip = self.board[row,col][0] == 'w' and self.whiteToMove # white piece to skip
            bskip = self.board[row,col][0] == 'b' and not self.whiteToMove # black piece to skip
            if self.board[row, col] == "--":
                moves.append(Move((r,c), (row,col), self.board))
                row, col = updateIdx(row, col)
            elif (wskip or bskip) and not skipped: #piece possible to be skipped in the way
                row, col = updateIdx(row, col) #skip piece
                skipped = True # allow only one piece to be skipped
            else:
                break
    
    """ cardinal and minister capturing move search functions """
    def capturingSearch(self, r, c, moves, updateIdx):
        row, col = updateIdx(r,c)
        while row in range(10) and col in range(10):
            wcapt = self.board[row,col][0] == 'b' and self.whiteToMove #white capturing black
            bcapt = self.board[row,col][0] == 'w' and not self.whiteToMove
            if self.board[row,col] == "--":
                row, col = updateIdx(row, col) #just skip empty pieces
            elif wcapt or bcapt: #capture possible
                moves.append(Move((r,c), (row,col), self.board))
                row, col = updateIdx(row,col)
                break
            else: #one of our own blocks the way
                break
    

    def cardinalMoves(self, r, c, moves):
        # moves like a bishop, captrues like a rook
        # can skip one of its own pieces while moving
        """ moving """
        # down right
        updateIdx = lambda r, c : (r+1, c+1)
        self.movingSearch(r, c, moves, updateIdx)
        # down left
        updateIdx = lambda r, c : (r+1, c-1)
        self.movingSearch(r, c, moves, updateIdx)  
        # up right
        updateIdx = lambda r, c : (r-1, c+1)
        self.movingSearch(r, c, moves, updateIdx) 
        # up left
        updateIdx = lambda r, c : (r-1, c-1)
        self.movingSearch(r, c, moves, updateIdx)
        """ capturing """
        # capture down
        updateIdx = lambda r, c : (r+1, c)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture down
        updateIdx = lambda r, c : (r-1, c)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture left
        updateIdx = lambda r, c : (r, c-1)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture right
        updateIdx = lambda r, c : (r, c+1)
        self.capturingSearch(r, c, moves, updateIdx)
    

    def ministerMoves(self, r, c, moves):
        # moves like a rook, captures like a bishop
        # can skip one of its own pieces while moving
        """ moving """
        # up
        updateIdx = lambda r, c : (r+1, c)
        self.movingSearch(r, c, moves, updateIdx)
        # down
        updateIdx = lambda r, c : (r-1, c)
        self.movingSearch(r, c, moves, updateIdx)  
        # right
        updateIdx = lambda r, c : (r, c+1)
        self.movingSearch(r, c, moves, updateIdx) 
        # left
        updateIdx = lambda r, c : (r, c-1)
        self.movingSearch(r, c, moves, updateIdx)
        """ capturing """
        # capture down right
        updateIdx = lambda r, c : (r+1, c+1)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture up right
        updateIdx = lambda r, c : (r-1, c+1)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture down left
        updateIdx = lambda r, c : (r+1, c-1)
        self.capturingSearch(r, c, moves, updateIdx)
        # capture up left
        updateIdx = lambda r, c : (r-1, c-1)
        self.capturingSearch(r, c, moves, updateIdx)
        

    def arrowMoves(self, r, c, moves):
        # arrows move like a bishop and can capture all pieces
        # on adjacent diagonals to the movement direction
        """ moving / capturing down right """
        row = r+1 ; col = c+1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row, col), self.board))
                # check where we can continue to look
                if row+1 in range(10):
                    # determine where white and black can capture
                    wcaptdown = (self.board[row+1,col][0] == 'b') and self.whiteToMove #capture on lower diag
                    bcaptdown = (self.board[row+1,col][0] == 'w') and not self.whiteToMove #black captures diag down
                    if wcaptdown or bcaptdown: #captures on lower diagonal possible
                        moves.append(Move((r,c), (row+1, col), self.board))
                if col+1 in range(10):
                    # determine where white and black can capture
                    wcaptup = (self.board[row,col+1][0] == 'b') and self.whiteToMove #capture on higher diag
                    bcaptup = (self.board[row,col+1][0] == 'w') and not self.whiteToMove #black captures diag up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row,col+1), self.board))
                row += 1 ; col += 1 #update index
            else: # cannot move to that square - thus also not capture
                break
        """ moving / capturing down left """
        row = r+1 ; col = c-1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row, col), self.board))
                # check where we can continue to look
                if row+1 in range(10):
                    # determine where white and black can capture
                    wcaptdown = (self.board[row+1,col][0] == 'b') and self.whiteToMove #capture on lower diag
                    bcaptdown = (self.board[row+1,col][0] == 'w') and not self.whiteToMove #black captures diag down
                    if wcaptdown or bcaptdown: #captures on lower diagonal possible
                        moves.append(Move((r,c), (row+1, col), self.board))
                if col-1 in range(10):
                    # determine where white and black can capture
                    wcaptup = (self.board[row,col-1][0] == 'b') and self.whiteToMove #capture on higher diag
                    bcaptup = (self.board[row,col-1][0] == 'w') and not self.whiteToMove #black captures diag up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row,col-1), self.board))
                row += 1 ; col -= 1 #update index
            else: # cannot move to that square - thus also not capture
                break
        """ moving / capturing up right """
        row = r-1 ; col = c+1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row, col), self.board))
                # check where we can continue to look
                if r-1 in range(10):
                    # determine where white and black can capture
                    wcaptup = (self.board[row-1,col][0] == 'b') and self.whiteToMove #capture on higher diag
                    bcaptup = (self.board[row-1,col][0] == 'w') and not self.whiteToMove #black captures diag up
                    if wcaptup or bcaptup: #captures on upper diagonal possible
                        moves.append(Move((r,c), (row-1, col), self.board))
                if col+1 in range(10):
                    # determine where white and black can capture
                    wcaptdown = (self.board[row,col+1][0] == 'b') and self.whiteToMove #capture on lower diag
                    bcaptdown = (self.board[row,col+1][0] == 'w') and not self.whiteToMove #black captures diag down
                    if wcaptdown or bcaptdown:
                        moves.append(Move((r,c), (row,col+1), self.board))
                row -= 1 ; col += 1 #update index
            else: # cannot move to that square - thus also not capture
                break
        """ moving / capturing up left """
        row = r-1 ; col = c-1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row, col), self.board))
                # check where we can continue to look
                if r-1 in range(10):
                    # determine where white and black can capture
                    wcaptup = (self.board[row-1,col][0] == 'b') and self.whiteToMove #capture on higher diag
                    bcaptup = (self.board[row-1,col][0] == 'w') and not self.whiteToMove #black captures diag up
                    if wcaptup or bcaptup: #captures on upper diagonal possible
                        moves.append(Move((r,c), (row-1, col), self.board))
                if col-1 in range(10):
                    # determine where white and black can capture
                    wcaptdown = (self.board[row,col-1][0] == 'b') and self.whiteToMove #capture on lower diag
                    bcaptdown = (self.board[row,col-1][0] == 'w') and not self.whiteToMove #black captures diag down
                    if wcaptdown or bcaptdown:
                        moves.append(Move((r,c), (row,col-1), self.board))
                row -= 1 ; col -= 1 #update index
            else: # cannot move to that square - thus also not capture
                break
    

    def hammerMoves(self, r, c, moves):
        pass
    




class Move(): # handles squares to execute moves and keeps track of them

    # chess notation dictionary, see part 2 ca 25min

    def __init__(self, start_sq, end_sq, board):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.moved_piece = board[self.startRow, self.startCol]
        self.captured_piece = board[self.endRow, self.endCol]
        #HASH function to create unique ID for each move
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
 
    # Overriding equals method to allow two move objects to be compared
    def __eq__(self, other):
        if isinstance(other, Move): #make sure it is also instance of Move class
            return self.moveID == other.moveID
        return False



