from Piece import Piece
import numpy as np
import copy

# Board class has board and size

class Board:
    def __init__(self,size):
        self.board = np.zeros([size,size])
        self.size = size
    
    