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
        
        #loads piece shapes from file  --- Need to create a new pickle since class was redefined
        f = open('blokus_pieces_lim_5.pkl', 'rb')
        all_pieces = pickle.load(f)
        f.close()
        
        self.pieces = []
        for piece in all_pieces:
            if piece.size <= piece_size:
                self.pieces.append(piece.get_orientations())
               
        self.player_list = []
        for i in range (1,num_players+1):
            new_player = Player(i,piece_size,self.game_board,self.pieces)
            self.player_list.append(new_player)
            
        self.turn = 1
        

    def run(self):
        
        # Ends game if no player can make a move
        turns_since_last_move = 0
        while turns_since_last_move < len(self.player_list):
            
            # select player to play
            current_player = self.player_list(self.turn)
            
            # ask player for move, then ask player to make move
            move = current_player.select_move(self.turn,self.board,self.pieces,strategy = 'random')
            
            # if no move could be made, increment counter by 1
            # else reset counter to 0
            if  move == False: #no move available
                turns_since_last_move = turns_since_last_move + 1
            else:
                # make move and save move made to self.board
                update_squares = current_player.make_move(self.turn,self.board,self.pieces)
                
                # append points in play to each player's update lists
                for player in self.player_list:
                    player.update_removals.append(update_squares)
                
                turns_since_last_move = 0
           
            
            # eventually, log each move
            
            # change to next player
            self.turn = self.turn % 4 + 1
        
        return self.score()
    
    #scores game based on number of squares occupied on board
    def score(self):
        scores= []
        for i in range(0,len(self.player_list)):
            scores.append(np.sum(self.board == i+1).sum())    
        return scores
            