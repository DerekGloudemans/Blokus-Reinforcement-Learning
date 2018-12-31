from Piece import Piece
import numpy as np
import copy
import matplotlib.pyplot as plt
import math
import seaborn as sns

# Board class has board and size
# views moves as a Piece object (already translated) and a player (integer from 1 to 4)

class Board:
    def __init__(self,size):
        self.board = np.zeros([size,size])
        self.size = size

# moves are expressed as a translated (player,piece_num,orientation,translation (x,y))
    def check_valid_move(self, player,test_piece,verbose = False):                
       
        #verify each corner falls within bounds
        corner_adj = False
        for point in test_piece.corners:
            if point[0] < 0 or point[1] < 0 or point[0] >= self.size or point[1] >= self.size:
                if verbose:
                    print("A corner is out of bounds: {}".format(point))
                return False
            
        #verify at least one corner adjacent belongs to player or first move    
        for point in test_piece.diag_adjacents:
            #diagonal adjacency
            if (point[0] >= 0 and point[1] >= 0 and point[0] < self.size and point[1] < self.size):
                if self.board[point[0],point[1]] == player:
                    corner_adj = True
                    break
            # first move
            elif point in [(-1,-1),(-1,self.size),(self.size,-1),(self.size,self.size)]:
                corner_adj = True
                break
        if corner_adj == False: 
            if verbose:
                    print("No adjacent corners.")
            return False
        
        #verify no adjacents occupied by player
        for point in test_piece.adjacents:
            if (point[0] >= 0 and point[1] >= 0 and point[0] < self.size and point[1] < self.size):
                if self.board[point[0],point[1]] == player:
                    if verbose:
                        print("Adjacent to an existing piece: {}".format(point))
                    return False
            
        #verify no occupied spaces already occupied
        for point in test_piece.occupied:
            if self.board[point[0],point[1]] != 0:
                if verbose:
                    print("Point is already occupied: {}".format(point))
                return False
        
        return True
       
    # display board
    def display(self):
        print(self.board)

    # display fancy
    def display2(self):
        sns.heatmap(self.board,cmap = 'Pastel1', linewidths = 1, square = True,cbar = False)
        
    # play_piece
    def play_piece(self,player,piece):
        if self.check_valid_move(player,piece,verbose = True):
            for point in piece.occupied:
                self.board[point[0],point[1]] = player
        else:
            print('invalid move')
            self.display()
            print(piece.occupied)
