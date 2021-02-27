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
            ["--", "--", "wr", "--", "--", "--", "--", "br", "--", "--"],
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
                    self.moveFunctions[piece](r, c, moves) #calls appropriate move functions

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
        """ movement to right """
        row = r+1 #iteration variable
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
        """ movement to left """
        row = r-1 # new iteration variable
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
        """ movement down """
        col = c+1 # interation variable
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
        """ movement up """
        col = c-1 #new iteration variable
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
             
    
    def knightMoves(self, r, c, moves):
        pass

    def bishopMoves(self, r, c, moves):
        pass

    def queenMoves(self, r, c, moves):
        pass

    def kingMoves(self, r, c, moves):
        pass

    def unicornMoves(self, r, c, moves):
        pass

    def eagleMoves(self, r, c, moves):
        pass

    def cardinalMoves(self, r, c, moves):
        pass

    def arrowMoves(self, r, c, moves):
        pass

    def hammerMoves(self, r, c, moves):
        pass

    def ministerMoves(self, r, c, moves):
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



