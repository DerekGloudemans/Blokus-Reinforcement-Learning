from Piece import Piece
from Board import Board
from Game import Game

import numpy as np
import copy

class Player:
    
    #initialize
    
    #maintain a piecelist with unique orientations (numbered)
    # keep track of played pieces
    # keep track of valid corners to play on - 
    # keep a list of places you need to check for changes to valid moves - game manager will append to this
    # maintain a list of valid moves
    
    # get_valid_moves
    # update_valid_moves
    # make_move - updates all players' lists of tracked changes, updates available piecelist, returns move to Game, which will call board method to update board
    # get_score