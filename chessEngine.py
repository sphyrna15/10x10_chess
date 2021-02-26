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



class Move(): # handles squares to execute moves and keeps track of them

    # chess notation dictionary, see part 2 ca 25min

    def __init__(self, start_sq, end_sq, board):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.moved_piece = board[self.startRow, self.startCol]
        self.captured_piece = board[self.endRow, self.endRow]

