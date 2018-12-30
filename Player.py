from Piece import Piece
from Board import Board
from Game import Game
import pickle
import numpy as np
import copy

class Player:
    
    #initialize
    def __init__(self,player_num,size_in,board_size,board):
        
        self.num = player_num
        
        #loads piece shapes from file
        f = open('blokus_pieces_lim_5.pkl', 'rb')
        all_pieces = pickle.load(f)
        f.close()
        # selects all below size limit and resizes to size limit
        self.pieces = []
        for piece in all_pieces:
            if piece.size <= size_in:
                temp = Piece(size_in,piece)
                self.pieces.append(temp.get_orientations())
       
        # maintains a vector of played pieces (1 = played)
        self.played = np.zeros([1,len(self.pieces)])
    
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
        self.valid_moves = self.get_valid_moves(board)
    
    def get_valid_moves(self,board):
        #for each piece and orientation in piecelist
        #for each corner
        #match to each valid corner on board, test if valid move
        return []
    
    # update_valid_moves
    # make_move - updates all players' lists of tracked changes, updates available piecelist, returns move to Game, which will call board method to update board
    # get_score