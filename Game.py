from Piece import Piece
from Board import Board
from Player import Player
import numpy as np
import copy

#Game class:
#maintains 4 player objects in a structure

#when initialized, creates a board, piecelist (common to all players), players, and a turn-marker
    
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

#run()
#queries each player for a move, then makes move
#logs each move
# keeps track of when game is over
# saves game log at end of game
