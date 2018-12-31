from Piece import Piece
from Board import Board
from Player import Player
import numpy as np
import copy
import pickle

#Game class:
#maintains 4 player objects in a structure

#when initialized, creates a board, piecelist (common to all players), players, and a turn-marker
class Game():
    def __init__(self,piece_size,num_players,board_size):
        self.game_board = Board(board_size)
        
        #loads piece shapes from file
        f = open('blokus_pieces_lim_5.pkl', 'rb')
        all_pieces = pickle.load(f)
        f.close()
        
        self.pieces = []
        for piece in all_pieces:
            if piece.size <= piece_size:
                temp = Piece(piece_size,piece)
                self.pieces.append(temp.get_orientations())
               
        self.player_list = []
        for i in range (1,num_players+1):
            new_player = Player(i,piece_size,self.game_board,self.pieces)
            self.player_list.append(new_player)
            
        self.turn = 1
        

#run()
#queries each player for a move, then makes move
#logs each move
# keeps track of when game is over
# saves game log at end of game
