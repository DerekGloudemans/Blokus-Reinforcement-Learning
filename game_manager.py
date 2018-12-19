import numpy as np
import pickle
import copy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#%matplotlib in command line
#%matplotlib inline

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
# Game Object
# manages the board, players, and turns, and returns final score of game at the end of the game
class Game:
    def __init__ (self, num_players, dimension, size_limit):
        self.limit = size_limit
        self.board = np.zeros([dimension,dimension])
        self.players = num_players
        self.turn = 0
        self.tilesets = []
        for i in range(0,num_players):
            self.tilesets.append(Piecelist(size_limit))
    
    def get_valid_moves(self,player):
        all_piece_orientations = self.tilesets[player].all_orientations()
        valid_moves = []
        # for each piece in player's tileset
        for piece_list in all_piece_orientations:
            #for each unique orientation
            for item in piece_list:
                # for each valid tile placement
                for i in range (-self.limit,len(self.board)+self.limit):
                    for j in range (-self.limit,len(self.board)+self.limit):
                        if self.check_valid_move(player,item,(i,j)):
                            valid_moves.append([item, (i,j)])
        return valid_moves
    
    def check_valid_move(self,player,piece,location, verbose=False):
        
        pointlist = piece.get_pointlist()
        #translate pointlist to board coordinates
        new_list = []
        for point in pointlist:
            new_list.append ((point[0]+location[0],point[1]+location[1]))
            
        #verify that piece falls within board bounds
        for point in new_list:
            if point[0] >= self.limit or point[0] < 0 \
            or point[1] >= self.limit or point[1] < 0:
                if verbose: print("Piece falls beyond board limits.")
                return False
        #verify that all squares occupied by piece are not yet occupied
        for point in new_list:
            if self.board[point[0],point[1]] != 0:
                if verbose: print("One or more squares already occupied.")
                return False
        
        #verify that move occupies a corner square
        if np.prod(self.board - player) != 0: # player hasn't played yet
            if (0,0) not in new_list and (0,self.limit-1) not in new_list \
            and (self.limit-1,0) not in new_list and (self.limit-1,self.limit-1) not in new_list:
                if verbose: print("First move must occupy a corner square.")
                return False
        
        #verify that piece is diagonal from another piece of the player
        else:
            piece_diags = piece.get_diag_adjacents()
            diag = False
            for item in piece_diags:
                #checks for square outside of board limits, ignore these
                if item[0]+location[0] >= 0 and item[0]+location[0] < self.limit \
                and item[1]+location[0] >= 0 and item[1]+location[1] < self.limit:
                    # checks for a diagonal that is occupied by player
                    if self.board[item[0]+location[0],item[1]+location[1]] == player: 
                        diag = True
                        break # possibly bad form
            if not diag:
                if verbose: print("Piece must be diagonal from a previously played piece.")
                return False
        
        #verify that there are no adjacencies
        piece_adjs = piece.get_adjacents()
        for item in piece_adjs:
            #checks for square outside board limits, ignore these
            if item[0]+location[0] >= 0 and item[0]+location[0] < self.limit \
            and item[1]+location[0] >= 0 and item[1]+location[1] < self.limit:
                #checks for an adjacent occupied by player
                if self.board[item[0] ,item[1]] == player:
                    if verbose: print("Piece may not be adjacent to a previously played piece.")
                    return False
        return True

    #location must be a 2D tuple
    def make_move(self,player,piece,location):
        if self.check_valid_move(player,piece,location):
        
            occupied_points = piece.get_pointlist()
            for point in occupied_points:
                self.board[point[0]+location[0],point[1]+location[1]] = player
            print(self.board)
            return 1
        else:
            x = copy.deepcopy(self.board)
            occupied_points = piece.get_pointlist()
            for point in occupied_points:
                x[point[0]+location[0],point[1]+location[1]] = 8
            print(x)
            print("Invalid move.")
            return 0
     
    def score(self):
        scores = []
        for i in range(0,self.players):
            scores.append(np.sum(self.board == i+1).sum())    
        return scores
    
    def visualizer(self):
        plt.figure()
        sns.set(style="white")
        sns.heatmap(self.board,cmap = 'Pastel2', vmin = 0, vmax = 4, center = 2 ,linewidths = 0.5,cbar = False,square= True)
        plt.show()