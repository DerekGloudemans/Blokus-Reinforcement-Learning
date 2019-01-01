from Piece import Piece
from Board import Board
import pickle
import numpy as np
import copy
import random

# a move will be stored as (player,piece_num,orientation,translation)

class Player:
    
    #initialize
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
        self.init_valid_moves(board,pieces)
        
    # initialize valid move list
    # Note from Mike: Not top priority, but I wonder if some of the code
    # from this function could be easily combined with the update_valid_moves
    # function to avoid duplication?                                                                            
    def init_valid_moves(self,board,pieces):
        all_valid_moves = []
        
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
                                   
        
    # make_move - updates all players' lists of tracked changes, updates available piecelist, returns move to Game, which will call board method to update board
    # a move will be stored as (player,piece_num,orientation,translation)
    def make_move(self,board,pieces,strategy):
        #Step 1 - update valid_moves list
        
        # for item in new corner adjs: search all unplayed piece orientations and add
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
                            
                            #check if move is valid
                            temp = copy.deepcopy(pieces[i][j][0])
                            temp.translate((x,y))
                            if board.check_valid_move(self.num,temp):
                                self.valid_moves.append((self.num,i,j,(x,y)))         

        

        # get list of changed squares
        # check for played piece, check for newly occupied square, and check for adjacents
        check = board.board-self.board_before_previous_play.board
        bad_squares = []
        # all squares that have changed since last turn are no longer playable
        for i in range(0,board.size):
            for j in range(0,board.size):
                if check[i,j] != 0:
                    bad_squares.append((i,j))
                    
        # add adjacents from last move to bad_squares list
        for point in self.update_adjacents_to_last_played:
            bad_squares.append(point)
            
        # check if any piece squares are now occupied or are
        # adjacent to player's own pieces
        for move_index in reversed(range((len(self.valid_moves)))):
            move = self.valid_moves[move_index]
            temp_piece = copy.deepcopy(pieces[move[1]][move[2]][0])
            temp_piece.translate(move[3])
            
            for point in bad_squares:
                
                if point in temp_piece.occupied:
                    del self.valid_moves[move_index]
                    break
                
                
        for i in range (0,len(self.played)):
            if self.played[i] == 1:
                for move_index in reversed(range((len(self.valid_moves)))):
                    move = self.valid_moves[move_index]
                    if move[1] == i:
                        del self.valid_moves[move_index]
                        
        success = False
        while success == False:
            #Step 2 - select a move from valid moves
            if len(self.valid_moves) == 0:
                return False
            else:
                if strategy == 'random':
                    move_idx = random.randint(0,len(self.valid_moves)-1)
                    move = self.valid_moves[move_idx]
                else:
                    return 'That strategy doesnt exist yet.'
            
            #Step 3 - make move
            # call make_move on board
            temp = copy.deepcopy(pieces[move[1]][move[2]][0])
            temp.translate(move[3])
            success = board.play_piece(self.num,temp)
            if success == False:
                self.valid_moves.remove(move)
                print("Attempted to play a failed move")
                board.display2()
        # update played_pieces
        print("Success")
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
        
        return temp