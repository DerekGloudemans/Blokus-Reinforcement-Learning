import numpy as np
import pickle
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import time
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
        orientations = []
        flipped = copy.deepcopy(self)
        flipped.flip()
        for i in range (0,4):
            orientations.append((copy.deepcopy(self.rotate(i)),False,i))
            orientations.append((copy.deepcopy(flipped.rotate(i)),True,i))
        
        #check for duplicates
        unique_orientations = []
        for item in orientations:
            unique = True
            for item2 in unique_orientations:
                if item[0].is_translation(item2[0]):
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
        orientations = []
        for piece in self.pieces:
            piece_orientations = piece.get_orientations()
            orientations.append(piece_orientations)
        return orientations
 
    
############################### Game Object ##################################
# represents the game and all played pieces
# Contains the piecelists for the 4 players
# Keeps track of turn
class Game:
    def __init__ (self, num_players, dimension, size_limit):
        self.board_limit = dimension
        self.piece_limit = size_limit
        self.board = np.zeros([dimension,dimension])
        self.players = num_players
        self.turn = 1
        self.tilesets = []
        for i in range(0,num_players+1):
            self.tilesets.append(Piecelist(size_limit))
        plt.figure()
        self.visualize()
    
    def get_valid_moves(self,player):
        all_piece_orientations = self.tilesets[player].all_orientations()
        valid_moves = []
        # for each piece in player's tileset
        for piece_list in all_piece_orientations:
            #for each unique orientation
            for item in piece_list:
                # for each valid tile placement
                for i in range (-self.piece_limit,len(self.board)+self.piece_limit):
                    for j in range (-self.piece_limit,len(self.board)+self.piece_limit):
                        if self.check_valid_move(player,item[0],(i,j)):
                            valid_moves.append([item[0], (i,j)])
        return valid_moves
    
    def check_valid_move(self,player,piece,location, verbose=False):
        
        pointlist = piece.get_pointlist()
        #translate pointlist to board coordinates
        new_list = []
        for point in pointlist:
            new_list.append ((point[0]+location[0],point[1]+location[1]))
            
        #verify that piece falls within board bounds
        for point in new_list:
            if point[0] >= self.board_limit or point[0] < 0 \
            or point[1] >= self.board_limit or point[1] < 0:
                if verbose: print("Piece falls beyond board limits. {} {} {}".format(point[0],point[1],self.board_limit))
                return False
        #verify that all squares occupied by piece are not yet occupied
        for point in new_list:
            if self.board[point[0],point[1]] != 0:
                if verbose: print("One or more squares already occupied.")
                return False
        
        #verify that move occupies a corner square
        if np.prod(self.board - player) != 0: # player hasn't played yet
            if (0,0) not in new_list and (0,self.board_limit-1) not in new_list \
            and (self.board_limit-1,0) not in new_list and (self.board_limit-1,self.board_limit-1) not in new_list:
                if verbose: print("First move must occupy a corner square.")
                return False
        
        #verify that piece is diagonal from another piece of the player
        else:
            piece_diags = piece.get_diag_adjacents()
            diag = False
            for item in piece_diags:
                #checks for square outside of board limits, ignore these
                if item[0]+location[0] >= 0 and item[0]+location[0] < self.board_limit \
                and item[1]+location[1] >= 0 and item[1]+location[1] < self.board_limit:
                    # checks for a diagonal that is occupied by player
                    if self.board[item[0]+location[0],item[1]+location[1]] == player: 
                        diag = True
                        if verbose: print('Diagonal Square - {} {}'.format(item[0] + location[0],item[1] + location[1]))
                        break # possibly bad form
            if not diag:
                if verbose: print("Piece must be diagonal from a previously played piece.")
                return False
        
        #verify that there are no adjacencies
        piece_adjs = piece.get_adjacents()
        for item in piece_adjs:
            #checks for square outside board limits, ignore these
            if item[0]+location[0] >= 0 and item[0]+location[0] < self.board_limit \
            and item[1]+location[1] >= 0 and item[1]+location[1] < self.board_limit:
                #checks for an adjacent occupied by player
                if self.board[item[0]+location[0] ,item[1]+location[1]] == player:
                    if verbose: print("Piece may not be adjacent to a previously played piece.")
                    return False
        return True

    #location must be a 2D tuple
    def make_move(self,player,piece_num,flip,rotations,location):
        #get piece, rotate and flip according to 
        piece = self.tilesets[player].pieces[piece_num]
        if flip:
            piece = copy.deepcopy(piece).flip()
        piece = copy.deepcopy(piece).rotate(rotations)
        
        #verify move is valid
        if self.check_valid_move(player,piece,location):
            
            # update squares on board with new piece
            occupied_points = piece.get_pointlist()
            for point in occupied_points:
                self.board[point[0]+location[0],point[1]+location[1]] = player
            
            #remove piece from player's piecelist
            self.tilesets[player].remove_piece(piece_num)
            self.visualize()
            return True
        
        #if move invalid, show attempted move but do not change board
        else:
#            x = copy.deepcopy(self.board)
#            occupied_points = piece.get_pointlist()
#            #should check for within bounds
#            for point in occupied_points:
#                x[point[0]+location[0],point[1]+location[1]] = 8
#            print(x)
            print("Invalid move.")
            return False
    
    #queries player for move (returns piece number from piecelist, location)
    def ask_move(self,player_type):
        
        player = self.turn
        
        if player_type == 'ai':
            print ('Error')
        if player_type == 'rand':
            print ('Error')
        
        else: #human player
            
            #variables to keep track of piece manipulation
            location1 = int(self.board_limit/2.0)
            location2 = int(self.board_limit/2.0)
            flip = False
            piece_num = 0
            rotations = 0
            
            played = False
            while not played: #move is invalid
                   
                #get current piece and position
                temp = copy.deepcopy(self.board)
                if flip:
                    cur_piece = copy.deepcopy(self.tilesets[player].pieces[piece_num]).flip().rotate(rotations)
                else:
                    cur_piece = copy.deepcopy(self.tilesets[player].pieces[piece_num]).rotate(rotations)
                occupied_points = cur_piece.get_pointlist()
                
                #display current modified board
                for item in occupied_points:
                    #checks for square outside of board limits, ignore these
                    if item[0]+location1 >= 0 and item[0]+location1 < self.board_limit \
                    and item[1]+location2 >= 0 and item[1]+location2 < self.board_limit:
                        temp[item[0]+location1,item[1]+location2] = player+5

                sns.heatmap(temp,cmap = 'Pastel2', vmin = 0, vmax = 4, center = 2 ,linewidths = 0.5,cbar = False,square= True)
                plt.show()      
                time.sleep(1)
                
                key = input('Press a key to maneuver piece.')
                if key == 'a':
                    #move piece left
                    location2 = location2 - 1
                elif key == 's':
                    #move piece down
                    location1 = location1 + 1
                elif key == 'd':
                    #move piece right
                    location2 = location2 + 1
                elif key == 'w':
                    #move piece up:
                    location1 = location1 - 1
                elif key == 'r':
                    #rotate piece 90 degrees
                    rotations = (rotations +1) % 4
                elif key == 'f':
                    #flip piece
                    flip = not flip
                elif key == 'p':
                    #attempt to play piece
                    played = self.make_move(player,piece_num,flip,rotations,(location1,location2))
                elif key == 'm':
                    piece_num = (piece_num + 1) % len(self.tilesets[player].pieces)
                elif key == 'n':
                    piece_num = (piece_num - 1) % len(self.tilesets[player].pieces)
                else:
                    print('Not a valid key. Valid keys are a,s,d,w,f,r,p,n,m')
        
                
        
        
        
        
    def score(self):
        scores = []
        for i in range(0,self.players+1):
            scores.append(np.sum(self.board == i).sum())    
        return scores
    
    def visualize(self):
        
        sns.set(style="white")
        sns.heatmap(self.board,cmap = 'Pastel2', vmin = 0, vmax = 4, center = 2 ,linewidths = 0.5,cbar = False,square= True)
        plt.show()
        
        
###################################### Start body code###########################
num_players = 2
tile_lim = 5
board_size = 10
game = Game(num_players,board_size,tile_lim)

end_count = 0
while end_count < num_players:
    #one turn
    
    #see if current player has any valid moves
    if len(game.get_valid_moves(game.turn)) > 0:
        print('Player {}\'s turn'.format(game.turn))
        game.ask_move('human')
        end_count = 0
    
    else:
        end_count = end_count + 1
           
    # make next player's turn
    game.turn = ((game.turn) % num_players) + 1
    final_scores = game.score()
print (final_scores)