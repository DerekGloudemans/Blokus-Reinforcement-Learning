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
        self.played = np.zeros([len(pieces)])        
        
        # keep a list of places you need to check for changes to valid moves - game manager will append to this
        self.update_new_corner_adjs = []
        self.update_adjacents_to_last_played = []
        self.board_before_previous_play = copy.deepcopy(board)
        
        # maintain a list of valid moves
        self.valid_moves = self.init_valid_moves(board,pieces)
    
    # initialize valid move list
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
                        all_valid_moves.append((self.num,i,j,(x,y)))
        return all_valid_moves
                   
        
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
                    
        for move in self.valid_moves:
            #check if piece has already been played
            if self.played[move[1]] == 1:
                self.valid_moves.remove(move)
            else:
                temp_piece = pieces[move[1]][move[2]][0]
                # check if any piece squares are now occupied
                for point in bad_squares:
                    if point in temp_piece.occupied:
                        self.valid_moves.remove(move)
                        break
        
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
        board.play_piece(self.num,temp)
        
        # update played_pieces
        self.played[move[1]] = 1
        
        # remove from valid_moves all move with this piece
        for item in self.valid_moves:
            if item[1] == move[1]:
                self.valid_moves.remove(item)
                
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