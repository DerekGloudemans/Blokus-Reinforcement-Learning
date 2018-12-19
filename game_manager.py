import numpy as np
import Pickle as pickle
# Blokus Game Manager
# Create a playable representation of the game Blokus with necessary functions 
# for human and AI players to interact with the game

############################# Piecelist Object ################################
# upon initialization, fills with all valid pieces of limit size or less
# for now, it is implemented manaully with support for size up to 5
# A list of lists, where each list represents all possible orientations for a single piece
class Piecelist:
    def __init__ (self, size_limit):
        f = open('blokus_pieces_lim_5.pkl', 'rb')
        new = pickle.load(f)

############################### Piece Object ##################################
# attributes - self.coords- represents a piece as a numpy array
class Piece:
    # point_list - a list of x,y tuples
    # size_limit - largest size for a piece in a game
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
    
    #flips piece along major diagonal    
    def flip(self):   
        self.coords = np.transpose(self.coords)
        return self
    
    # returns a list of 2D tuples for adjacent spaces
    def get_adjacents(self):
        piece_list = self.get_pointlist()
       
        #store all 1-block translations
        aug_list = []
        for point in piece_list:
            aug_list.append((point[0],point[1] + 1 ))
            aug_list.append((point[0],point[1] - 1 ))
            aug_list.append((point[0] - 1,point[1] ))
            aug_list.append((point[0] + 1,point[1] ))
        
        final_list = [] 
        for point in aug_list:
            if point not in piece_list and point not in final_list:
               final_list.append(point)
      
        return final_list
    
    #returns a list of 2D tuples for diagonal adjacent squares                  
    def get_diag_adjacents(self):
        piece_list = self.get_pointlist()
        adj_list = self.get_adjacents()
        #store all 1-block diagonal translations
        aug_list = []
        for point in piece_list:
            aug_list.append((point[0]+1,point[1]+1))
            aug_list.append((point[0]+1,point[1]-1))
            aug_list.append((point[0]-1,point[1]+1))
            aug_list.append((point[0]-1,point[1]-1))
    
        final_list = [] 
        for point in aug_list:
            if point not in piece_list and point not in final_list and point not in adj_list:
               final_list.append(point)
      
        return final_list
    
    # returns a list of 2D tuple points representing the piece
    def get_pointlist(self):
        point_list = []
        for i in range (0,len(self.coords)):
            for j in range (0,len(self.coords)):
                if self.coords[i,j] == 1:
                    point_list.append((i,j))
        return point_list
    
    # checks for translational, rotational and flip symmetry 
    def is_same(self, other_piece):
        for i in range (0,4):
            if self.is_translation(other_piece.rotate(i)):
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
                return True
            else:
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
        self.flip()
        for i in range (0,4):
            if self.is_translation(other_piece.rotate(i)):
                # so piece orientations remain the same afterwards
                self.flip()
                other_piece.rotate(-i)
                return True
            else:
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
        return False
    
    # checks for translational symmetry to another piece
    def is_translation(self,other_piece):
        for i in range(0,len(self.coords)):
            for j in range(0,len(self.coords)):
                if np.array_equal(self.coords, np.roll(other_piece.coords,(i,j),(0,1))):
                    return True
        return False
    
    # rotates piece by 90 degrees times input
    def rotate(self,quarter_rotations = 1):
        self.coords = np.rot90(self.coords,quarter_rotations)
        return self
    
    # prints numpy representation of piece
    def show(self):
        print(self.coords)


    
# Board Object
# represents the game and all played pieces; fully describes the state as seen by players
# possibly also contains the piecelists for the 4 players
# implements logicl behind valid moves

# Game Object
# manages the board, players, and turns, and returns final score of game at the end of the game

piece1 = Piece(4,list1)
piece2 = Piece(4,list2)
piece3 = Piece(4,testlist)