from Piece import Piece
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Board - maintains representation of game board
# self.board- a numpy array representation of the board, with a 0 representing
    # an unclaimed square and an integer representing a square claimed by that player
# self.size represents board dimensions

class Board:
    # Constructor
    # size - int representing length and width of board
    def __init__(self,size):
        self.board = np.zeros([size,size])
        self.size = size
    #check_valid_move() - returns True if move is valid for current board state, False otherwise
    # player - int from 1 to number of players
    # piece - translated Piece object
    # verbose - if True, outputs reason why move is not valid
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
       
    # display() - display board as numpy array
    def display(self):
        print(self.board)

    # display2() - displays a slightly nicer representation of board
    def display2(self):
        #plt.figure()
        sns.heatmap(self.board,cmap = 'Accent', linewidths = 1, square = True,cbar = False)
        plt.show()
        plt.pause(0.01)
        
    # play_piece() - update board with player's piece if valid
    # player - int from 1 to number of players
    # piece - translated Piece object
    def play_piece(self,player,piece):
        if self.check_valid_move(player,piece,verbose = True):
            for point in piece.occupied:
                self.board[point[0],point[1]] = player
            return True
        else:
            print('invalid move')
            print(piece.occupied)
            return False
        
        #self.display()
