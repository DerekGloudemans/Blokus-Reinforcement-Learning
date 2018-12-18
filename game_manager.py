import numpy as np

# Blokus Game Manager
# Create a playable representation of the game Blokus with necessary functions 
# for human and AI players to interact with the game

# Piecelist Object
# A list of lists, where each list represents all possible orientations for a single piece

# Piece Object
# represents offset coordinates from base location of a piece
# must be able to translate, rotate and flip pieces



# A size_limit x size_limit numpy array
# coords is a list of x,y tuples
# 1 represents the piece squares, 0 otherwise
class Piece:
    def __init__(self, size_limit, point_list):
        self.coords = np.zeros([size_limit, size_limit])
        
        error = False
        for point in point_list:
            # Checks for out-of-range points
            if point[0] >= size_limit or point[1] >= size_limit:
                error = True
                break
            else:
                self.coords[point[0],point[1]] = 1
        if error:
            print("Error creating piece. Point out of valid range.")
            self.coords = np.zeros([size_limit,size_limit])
    
    def rotate(self,quarter_rotations = 1):
        self.coords = np.rot90(self.coords,quarter_rotations)
        
    def flip(self):   
        self.coords = np.transpose(self.coords)
    
    def is_translation(self,other_piece):
        for i in range(0,len(self.coords)):
            for j in range(0,len(self.coords)):
                if np.array_equal(self.coords, np.roll(other_piece.coords,(i,j),(0,1))):
                    return True
        return False
    
# Board Object
# represents the game and all played pieces; fully describes the state as seen by players
# possibly also contains the piecelists for the 4 players
# implements logicl behind valid moves

# Game Object
# manages the board, players, and turns, and returns final score of game at the end of the game

