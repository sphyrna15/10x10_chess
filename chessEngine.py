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
        self.whiteKingLocation = (8, 5) #Location of the white king
        self.blackKingLocation = (1, 5) #Location of the black king
        # dictionary to keep track of piece function names 
        self.moveFunctions = {'p': self.pawnMoves, 'r': self.rookMoves, 'n': self.knightMoves, 'u': self.unicornMoves, 
                            'b': self.bishopMoves, 'q': self.queenMoves, 'k': self.kingMoves, 'e': self.eagleMoves, 
                            'c': self.cardinalMoves, 'h': self.hammerMoves, 'a': self.arrowMoves, 'm': self.ministerMoves}
        self.isStaleMate = False
        self.isCheckMate = False
        self.enpassantSquare = () #track fields where enpassant is possible
    
    # Will not work for casteling, en passant capture and pawn promotion
    def makeMove(self, move):
        self.board[move.startRow, move.startCol] = "--" #leave behind blank space
        self.board[move.endRow, move.endCol] = move.moved_piece #move piece to new location
        self.moveLog.append(move) #track move
        self.whiteToMove = not self.whiteToMove #switch players
        #if king moved, update king location
        if move.moved_piece == 'wk':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.moved_piece == 'bk':
            self.blackKingLocation = (move.endRow, move.endCol)
        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow, move.endCol] = move.moved_piece[0] + 'q'
        # en passant capture
        if move.isEnPassant:
            self.board[move.startRow, move.endCol] = "--"

        # update enpassant variable - if moved piece is 2pawn advance - enpassant possible
        if move.moved_piece[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            #this is the square where en passant is possible
            self.enpassantSquare = ((move.startRow+move.endRow)//2, move.endCol)
        else:
            self.enpassantSquare = ()

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() #gets last element and removes
            self.board[move.startRow, move.startCol] = move.moved_piece #put moved piece back at start
            self.board[move.endRow, move.endCol] = move.captured_piece #put catured piece back in place
            self.whiteToMove = not self.whiteToMove
            #if king moved, update king location
            if move.moved_piece == 'wk':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.moved_piece == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassant
            if move.isEnPassant:
                self.board[move.endRow, move.endCol] = "--"
                self.board[move.startRow, move.endCol] = move.captured_piece
                self.enpassantSquare = (move.endRow, move.endCol)
            #undo 2square pawn advance
            if move.moved_piece[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantSquare = ()

        

    
    """ Get All actually Valid Moves for the player (considering checks) """
    def getValidMoves(self):
        # generate all possible moves, make them all,
        # then generate all opponent moves and check if they attack king
        temp_enpasssant = self.enpassantSquare #temporary en passant store for undo moves
        moves =  self.getPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i]) #make the move
            oppMoves = self.getPossibleMoves() #get all opponents moves
            self.whiteToMove = not self.whiteToMove # again switch turns
            if self.inCheck():
                moves.remove(moves[i]) #remove move that ends in check
            self.whiteToMove = not self.whiteToMove #switch back
            self.undoMove() # undo the move made
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.isCheckMate = True
                print('CHECKMATE')
            else:
                self.isStaleMate = True 
                print('STALEMATE')
        else: #reset checkmate, stalemate
            self.isCheckMate = False
            self.isStaleMate = False

        self.enpassantSquare = temp_enpasssant #fix undo enpassant undo issue    
        return moves

    """ Determine if the King is in Check """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareAttacked(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareAttacked(self.blackKingLocation[0], self.blackKingLocation[1])

    """ is an piece attacking the piece on (r,c)? """
    def squareAttacked(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponents view
        oppMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square attacked
                return True
        return False

    
    """ Get All Possible moves for a player (not considering checks) """
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
                if r == 7 and self.board[r-2, c] == "--": # base row 2 square pawn advance
                    moves.append(Move((r,c), (r-2,c), self.board))
            # white pawn captures:
            if c-1 >= 0: #left capture
                if self.board[r-1, c-1][0] == 'b': #black piece to capture
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1, c-1) == self.enpassantSquare: #tell move that it is enpassant
                    moves.append(Move((r,c), (r-1,c-1), self.board, enPassant=True))
            if c+1 <= 9: #right capture
                if self.board[r-1, c+1][0] == 'b': 
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1, c+1) == self.enpassantSquare: #tell move that it is enpassant
                    moves.append(Move((r,c), (r-1,c+1), self.board, enPassant=True))
        
        if not self.whiteToMove: # black pawn moves
            if self.board[r+1, c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 2 and self.board[r+2, c] == "--": #base row 2 square pawn advance
                    moves.append(Move((r,c), (r+2,c), self.board))
            #black bawn captures:
            if c-1 >= 0: #left capture
                if self.board[r+1, c-1][0] == 'w': #white piece to capture
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1, c-1) == self.enpassantSquare: #tell move that it is enpassant
                    moves.append(Move((r,c), (r+1,c-1), self.board, enPassant=True))
            if c+1 <= 9: #right capture
                if self.board[r+1, c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
                elif (r+1, c+1) == self.enpassantSquare: #tell move that it is enpassant
                    moves.append(Move((r,c), (r+1,c+1), self.board, enPassant=True))
        



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
        # the hammer moves like a rook and can capture on all rows and collums
        # adjacent to its direction of travel
        """ moving / capturing down """
        row = r+1 ; col = c
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row,col), self.board))
                # check where we can continue to look:
                if col-1 in range(10):
                    wcaptleft = (self.board[row,col-1][0] == 'b') and self.whiteToMove #white captures left
                    bcaptleft = (self.board[row,col-1][0] == 'w') and not self.whiteToMove #black captures left
                    if wcaptleft or bcaptleft:
                        moves.append(Move((r,c), (row,col-1), self.board))
                if col+1 in range(10):
                    wcaptright = (self.board[row,col+1][0] == 'b') and self.whiteToMove #white captures right
                    bcaptright = (self.board[row,col+1][0] == 'w') and not self.whiteToMove #black captures right
                    if wcaptright or bcaptright:
                        moves.append(Move((r,c), (row,col+1), self.board))
                row += 1
            else: # cannot move further
                break
        """ moving / capturing up """
        row = r-1 ; col = c
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row,col), self.board))
                # check where we can continue to look:
                if col-1 in range(10):
                    wcaptleft = (self.board[row,col-1][0] == 'b') and self.whiteToMove #white captures left
                    bcaptleft = (self.board[row,col-1][0] == 'w') and not self.whiteToMove #black captures left
                    if wcaptleft or bcaptleft:
                        moves.append(Move((r,c), (row,col-1), self.board))
                if col+1 in range(10):
                    wcaptright = (self.board[row,col+1][0] == 'b') and self.whiteToMove #white captures right
                    bcaptright = (self.board[row,col+1][0] == 'w') and not self.whiteToMove #black captures right
                    if wcaptright or bcaptright:
                        moves.append(Move((r,c), (row,col+1), self.board))
                row -= 1
            else: # cannot move further
                break
        """ moving / capturing to the right """
        row = r ; col = c+1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row,col), self.board))
                # check where we can continue to look
                if row-1 in range(10):
                    wcaptup = (self.board[row-1,col][0] == 'b') and self.whiteToMove #white captures up
                    bcaptup = (self.board[row-1,col][0] == 'w') and not self.whiteToMove #black captures up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row-1,col), self.board))
                if row+1 in range(10):
                    wcaptup = (self.board[row+1,col][0] == 'b') and self.whiteToMove #white captures up
                    bcaptup = (self.board[row+1,col][0] == 'w') and not self.whiteToMove #black captures up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row+1,col), self.board))
                col += 1
            else: # cannot move further
                break
        """ moving / capturing to the left """
        row = r ; col = c-1
        while row in range(10) and col in range(10):
            if self.board[row,col] == "--":
                moves.append(Move((r,c), (row,col), self.board))
                # check where we can continue to look
                if row-1 in range(10):
                    wcaptup = (self.board[row-1,col][0] == 'b') and self.whiteToMove #white captures up
                    bcaptup = (self.board[row-1,col][0] == 'w') and not self.whiteToMove #black captures up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row-1,col), self.board))
                if row+1 in range(10):
                    wcaptup = (self.board[row+1,col][0] == 'b') and self.whiteToMove #white captures up
                    bcaptup = (self.board[row+1,col][0] == 'w') and not self.whiteToMove #black captures up
                    if wcaptup or bcaptup:
                        moves.append(Move((r,c), (row+1,col), self.board))
                col -= 1
            else: # cannot move further
                break
                


    




class Move(): # handles squares to execute moves and keeps track of them

    # chess notation dictionary, see part 2 ca 25min

    def __init__(self, start_sq, end_sq, board, enPassant = False):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.moved_piece = board[self.startRow, self.startCol]
        self.captured_piece = board[self.endRow, self.endCol]
        #pawn promotion stuff - check if move is pawn promotion
        self.isPawnPromotion = ((self.moved_piece == 'wp' and self.endRow == 0) or (self.moved_piece == 'bp' and self.endRow == 9))
        #check if move is enpassant - conditional input parameter enPassant
        self.isEnPassant = enPassant
        if self.isEnPassant:
            self.captured_piece = 'wp' if self.moved_piece == 'bp' else 'bp'
        #HASH function to create unique ID for each move
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
 
    # Overriding equals method to allow two move objects to be compared
    def __eq__(self, other):
        if isinstance(other, Move): #make sure it is also instance of Move class
            return self.moveID == other.moveID
        return False




"""
# alternative algorithm to check for pins and checks
    def checkPinsAndChecks(self):
        pins = [] #square where allied piece is pinned from + direction
        checks = [] #squares where enemy piece is checking our king from
        check = False
        if self.whiteToMove:
            enemy = 'b' ; ally = 'w'
            startRow = int(self.whiteKingLocation[0])
            startCol = int(self.whiteKingLocation[1])
        else:
            enemy = 'w' ; ally = 'b'
            startRow = int(self.blackKingLocation[0])
            startCol = int(self.blackKingLocation[1])
        # check outward from king for possible checks, pins
        directions = [(-1,0), (0,-1), (1,0), (0,1), (1,-1), (1,1), (-1,-1), (-1,1)]
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1, 10): 
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if endRow in range(10) and endCol in range(10):
                    piece = self.board[endRow, endCol]
                    if piece[0] == ally
                        if possiblePin == ():
                            possiblePin = (endRow, endRow, d[0], d[1])
                        else: #second allied piece - no pin possible in this direciton
                            break
                    elif piece[0] == enemy:
                        figure = piece[1]
                        # 5 possibilities here:
                        # 1 - orthogonally placed rook
                        # 2 - diagonally placed bishop
                        # 3 - 1 square diagonally in front and pawn
                        # 4 any direction queen
                        # 5 any one square away opposite king (prevent kings from getting close)
                        if (j in range(4) and figure == 'r') or \
                            (j in range(4,8) and figure == 'b') or \
                            (i == 1 and figure == 'p' and ((enemy == 'w' and j in range(4,6)) or (enemy == 'b' and j in range(6,8)))) or \
                            (figure == 'q') or (i == 1 and figure == 'k'):
                            if possiblePin == (): #no blocking piece -  check
                                check = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking - pin
                                pins.append(possiblePin)
                                break
                        else: # no applied check
                            break
                else: #off board
                    break
        # check for knight or eagle checks
        knightReach = [(-2,-1), (-2,1), (2,-1), (2,1), (-1,-2), (1,-2), (-1,2), (1,2)]
        eagleReach = [(-3,-2), (-3,2), (-3,-1), (-3,1), (3,-2), (3,2), (3,-1), (3,1), 
                        (-2,-3), (2,-3), (-1,-3), (1,-3), (-2,3), (2,3), (-1,3), (1,3)]
        #enemyReach = knightReach.append(eagleReach)
        for m in knightReach:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            for endRow in range(10) and endCol in range(10):
                piece = seld.board[endRow, endCol]
                if piece[0] == enemy and piece[1] == 'n': 
                    check = True
                    checks.append((endRow, endCol, m[0], m[1]))
        

        return check, pins, checks
        """