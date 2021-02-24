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

    


