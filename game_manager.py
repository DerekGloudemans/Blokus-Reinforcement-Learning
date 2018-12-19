import numpy as np
import pickle
import copy
# Blokus Game Manager
# Create a playable representation of the game Blokus with necessary functions 
# for human and AI players to interact with the game

############################### Piece Object ##################################
# attributes - self.coords- represents a piece as a numpy array
class Piece:
    # point_list - a list of 2D tuples
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
    
    # returns a list of all unique orientations of the piece
    def get_orientations(self):
        #create list of all possible orientations
        all_orientations = []
        flipped = copy.deepcopy(self)
        flipped.flip()
        for i in range (0,4):
            all_orientations.append(copy.deepcopy(self.rotate(i)))
            all_orientations.append(copy.deepcopy(flipped.rotate(i)))
        
        #check for duplicates
        unique_orientations = []
        for item in all_orientations:
            unique = True
            for item2 in unique_orientations:
                if item.is_translation(item2):
                    unique = False
            if unique:
                unique_orientations.append(item)
        
        return unique_orientations 
            
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


############################# Piecelist Object ################################
# upon initialization, fills with all valid pieces of limit size or less
# for now, it is implemented manaully with support for size up to 5
# A list of lists, where each list represents all possible orientations for a single piece
class Piecelist:
    def __init__ (self, size_limit):
        # loads pieces from pickled file 
        f = open('blokus_pieces_lim_5.pkl', 'rb')
        all_pieces = pickle.load(f)
        f.close()
        
        # selects all below size limit and resizes to size limit
        self.pieces = []
        for piece in all_pieces:
            if len(piece.coords) <= size_limit:
                new_piece = Piece(size_limit,piece.get_pointlist())
                self.pieces.append(new_piece)
    
    # displays all pieces in a heretofore unknown yet incredibly convenient format
    def display_all(self):
        for i in range(0,len(self.pieces)):
            print('\nPiece {}:'.format(i))
            self.pieces[i].show()
    
    # removes the "piece_num"th piece from the list
    def remove_piece(self,piece_num):
        del self.pieces[piece_num]
    
    # returns a list of lists, where each list corresponds to all unique 
    # (non-translational) orientations of a piece, each represented as a piece
    def all_orientations(self):
        all_orientations = []
        for piece in self.pieces:
            piece_orientations = piece.get_orientations()
            all_orientations.append(piece_orientations)
        return all_orientations
 
    
############################### Board Object ##################################
# represents the game and all played pieces; fully describes the state as seen by players
# possibly also contains the piecelists for the 4 players
# implements logicl behind valid moves
class Board:
    def __init__(self,dimension):
        self.squares = np.zeros([dimension,dimension])
        self.limit = dimension
        
    def check_valid_move(self,piece,location):
        #verify that piece falls within board bounds
        #verify that all squares occupied by piece are not yet occupied
        #verify that if a piece has not yet been played, one corner square is occupied by piece
        #verify that if a piece has been played, diagonal connection
        #verify that there are no adjacencies
        return True

    #location must be a 2D tuple
    def make_move(self,player,piece,location):
        if self.check_valid_move(piece,location):
        
            occupied_points = piece.get_pointlist()
            for point in occupied_points:
                self.squares[point[0]+location[0],point[1]+location[1]] = player
            
            return 1
        else:
            print("Invalid move.")
            return 0

# Game Object
# manages the board, players, and turns, and returns final score of game at the end of the game

