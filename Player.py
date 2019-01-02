from Piece import Piece
from Board import Board
import numpy as np
import copy
import random
from heuristics import space_heuristic

# Player class - stores information necessary to make a valid move for a player
# self.num - player number used by Game
# self.played - 1D np array with 1 if piece at that index in Game.pieces is played, 0 otherwise
# self.update_new_corner_adjs - list of 2D (x,y) integer tuples 
    # where corner_adjacents are added when a move is made
# self.update_adjacents_to_last_played - list of @d (x,y) integer tuples 
    # where adjacent squares to a played piece are stored
# self.board_before_previous_play - Board object used to determine changed squares
# self.valid_moves - list of valid moves, where moves are a tuple
    # a move will be stored as (player_num,piece_num,orientation,translation)
class Player:
    
    # Constructor
    # player_num - integer, assigned by Game object
    # size_in - max piece size (5)
    # board - Board object (generally an empty board)
    # pieces - list of lists of Piece objects , as specified in Game.pieces
    def __init__(self,player_num,size_in,board,pieces):
    
        self.num = player_num
       
        # maintains a vector of played pieces (1 = played)
        self.played = np.ones([len(pieces)])
        # MIKE Changed this; should be 21 pieces
        self.played[0:21] = 0
        
        # keep a list of places you need to check for changes to valid moves - game manager will append to this
        self.update_new_corner_adjs = []
        self.update_adjacents_to_last_played = []
        self.board_before_previous_play = copy.deepcopy(board)
        
        # maintain a list of valid moves
        self.valid_moves = []
        self.init_valid_moves(board,pieces)
   
    
    # init_valid_moves() - initializes valid_moves list for first turn
    # board - Board object
    # pieces - list of lists of Piece objects
    
    # Note from Mike: Not top priority, but I wonder if some of the code
    # from this function could be easily combined with the update_valid_moves
    # function to avoid duplication?                                                                            
    def init_valid_moves(self,board,pieces):
        all_valid_moves = []
        
        # selects one valid corner for each player, so each plays in a different corner
        if self.num == 1:
            corner = (0,0)
        elif self.num == 2:
            corner = (board.size-1,board.size-1)
        elif self.num == 3:
            corner = (0,board.size-1)
        else :
            corner = (board.size-1,0)
        
        # each i represents 1 piece
        for i in range (0,len(pieces)):
            #each j represents 1 orientation
            if self.played[i] == 0:
                for j in range (0,8):
                    if j >= len(pieces[i]):
                        break
                    #each k represents 1 corner of the piece
                    for k in range (0, 8):
                        if k >= len(pieces[i][j][0].corners):
                            break
    
                        #find translation necessary to put piece corner into valid corner
                        x = corner[0] - pieces[i][j][0].corners[k][0]
                        y = corner[1] - pieces[i][j][0].corners[k][1]
                        
                        #check if move is valid
                        temp = copy.deepcopy(pieces[i][j][0])
                        temp.translate((x,y))
                        if board.check_valid_move(self.num,temp):
                            # Note from Mike: It may actually be helpful to create a Move class
                            # not because this is a bad format as it is, but because it would
                            # improve understandability                                                   
                            all_valid_moves.append((self.num,i,j,(x,y)))
        self.valid_moves =  all_valid_moves
                                   
        
    # make_move() -  updates valid_moves, selects a move using specified strategy
        # makes move on input Board object, and returns move
    # board - Board object
    # pieces - list of lists of Piece objects
    # strategy - string keyword ('random')
    # returns move - stored as (player,piece_num,orientation,translation)
    def make_move(self,board,pieces,strategy):
        #Step 1 - update valid_moves list
        
        # for item in new corner adjacencies (resulting from last played piece)
        # search all unplayed piece orientations onto new corner adjacency
        # each i represents 1 piece
        for i in range (0,len(pieces)):
            if self.played[i] == 0:
                #each j represents 1 orientation
                for j in range (0,8):
                    if j >= len(pieces[i]):
                        break
                    #each k represents 1 corner of the piece
                    for k in range (0, 8):
                        if k >= len(pieces[i][j][0].corners):
                            break
                        #each m represents one valid corner placement  on board for player
                        for item in self.update_new_corner_adjs:
                            #find translation necessary to put piece corner into valid corner
                            x = item[0] - pieces[i][j][0].corners[k][0]
                            y = item[1] - pieces[i][j][0].corners[k][1]
                            
                            #check if move is valid, if so append to valid_moves
                            # temp is a copy of Piece object stored in Game.pieces
                            temp = copy.deepcopy(pieces[i][j][0])
                            temp.translate((x,y))
                            if board.check_valid_move(self.num,temp):
                                self.valid_moves.append((self.num,i,j,(x,y)))         

        
        
        # get list of changed squares since before last move
        check = board.board-self.board_before_previous_play.board
        # all squares that have changed since last turn are no longer usable
        bad_squares = []
        for i in range(0,board.size):
            for j in range(0,board.size):
                if check[i,j] != 0:
                    bad_squares.append((i,j))
                    
        # squares adjacent to player's last piece played are no longer usable
        for point in self.update_adjacents_to_last_played:
            bad_squares.append(point)
            
        # for each move, check if any unusable squares are occupied, and remove if so
        # note list is checked in reverse order so that removing a move does not
        # alter list indexing
        for move_index in reversed(range((len(self.valid_moves)))):
            move = self.valid_moves[move_index]
            temp_piece = copy.deepcopy(pieces[move[1]][move[2]][0])
            temp_piece.translate(move[3])
            
            for point in bad_squares:
                if point in temp_piece.occupied:
                    del self.valid_moves[move_index]
                    break
        
        ## NOTE: I replaced this block with the following block, but left it in case
        ## it caused an error        
#        # remove all moves for pieces already played
#        for i in range (0,len(self.played)):
#            if self.played[i] == 1:
#                for move_index in reversed(range((len(self.valid_moves)))):
#                    move = self.valid_moves[move_index]
#                    if move[1] == i:
#                        del self.valid_moves[move_index]
        
        # remove all moves for pieces already played
        for move_index in reversed(range((len(self.valid_moves)))):
            move = self.valid_moves[move_index]
            if self.played[move[1]] == 1:
                del self.valid_moves[move_index]
                        
         
        #Step 2 - select a move from valid moves    
        # loop while a valid move has not been selected
        # theoretically, this loop should never execute more than once since
        # all moves in valid_moves should be valid
        success = False
        while success == False:
            
            if len(self.valid_moves) == 0:
                return False
            else:
                if strategy == 'random':
                    # get random index of valid move
                    move_idx = random.randint(0,len(self.valid_moves)-1)
                    move = self.valid_moves[move_idx]
                elif strategy == 'space_heuristic':
                    best_val = 0
                    best_idx = 0
                    for i in range(0,len(self.valid_moves)):
                        move = self.valid_moves[i]
                        temp_board = copy.deepcopy(board)
                        temp_piece = copy.deepcopy(pieces[move[1]][move[2]][0])
                        temp_piece.translate(move[3])
                        temp_board.play_piece(self.num,temp_piece)
                        val = space_heuristic(self.num, temp_board)
                        if val > best_val:
                            best_val = val
                            best_idx = i
                    
                    move = self.valid_moves[best_idx]
                    
                else:
                    return 'That strategy doesnt exist yet.'
            
            #Step 3 - make move
            # call play_piece on Board object
            temp = copy.deepcopy(pieces[move[1]][move[2]][0])
            temp.translate(move[3])
            success = board.play_piece(self.num,temp)
            
            if success == False:
                self.valid_moves.remove(move)
                print("Attempted to play a failed move")
                
        # update played_pieces
        self.played[move[1]] = 1
        
        #reset update lists
        self.update_new_corner_adjs = []
        self.update_adjacents_to_last_played = []  
        
        # add new corner_adjs to update_list
        for point in temp.diag_adjacents:
            self.update_new_corner_adjs.append(point)
            
        # add adjacents to update list    
        for point in temp.adjacents:
            self.update_adjacents_to_last_played.append(point)
        
        return move