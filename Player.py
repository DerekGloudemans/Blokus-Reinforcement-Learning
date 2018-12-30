from Piece import Piece
from Board import Board
from Game import Game
import pickle
import numpy as np
import copy

# a move will be stored as (player,piece_num,orientation,translation)

class Player:
    
    #initialize
    def __init__(self,player_num,size_in,board_size,board,pieces):
        
        self.num = player_num
       
        # maintains a vector of played pieces (1 = played)
        self.played = np.zeros([1,len(pieces)])
    
        # keep track of valid corners to play on (initialize to board corner only)
        if player_num == 1:
            self.valid_corners = [(0,0)]
        elif player_num == 2:
            self.valid_corners = [(board_size-1,board_size-1)]
        elif player_num == 3:
            self.valid_corners = [(0,board_size-1)]
        else :
            self.valid_corners = [(board_size-1,0)]
        
        # keep a list of places you need to check for changes to valid moves - game manager will append to this
        self.changes = []
        
        # maintain a list of valid moves
        self.valid_moves = []
        self.valid_moves = self.get_valid_moves(board)
    
    def get_valid_moves(self,board,pieces):
        if self.valid_moves == []: #first turn
        
            all_valid_moves = []
            
            # each i represents 1 piece
            for i in range (0,len(pieces)):
                #each j represents 1 orientation
                for j in range (0,pieces[i]):
                    #each k represents 1 corner of the piece
                    for k in range (0, len(pieces[i][j].corners)):
                        #each m represents one valid corner pplacement  on board for player
                        for m in range (0, len(self.valid_corners)):
                            #find translation necessary to put piece corner into valid corner
                            x = self.valid_corners[m][0] - pieces[i][j].corners[k][0]
                            y = self.valid_corners[m][1] - pieces[i][j].corners[k][1]
                            
                            #check if move is valid
                            temp = copy.deepcopy(pieces[i][j])
                            temp.translate(x,y)
                            if board.check_valid_move(self.num,temp):
                                all_valid_moves.append((self.num,i,j,(x,y)))
            return all_valid_moves
        
        else: #valid moves list already exists
            return []
        
        
    # update_valid_moves
    # make_move - updates all players' lists of tracked changes, updates available piecelist, returns move to Game, which will call board method to update board
    # get_score