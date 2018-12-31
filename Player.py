from Piece import Piece
from Board import Board
import pickle
import numpy as np
import copy

# a move will be stored as (player,piece_num,orientation,translation)

class Player:
    
    #initialize
    def __init__(self,player_num,size_in,board,pieces):
        
        self.num = player_num
       
        # maintains a vector of played pieces (1 = played)
        self.played = np.zeros([1,len(pieces)])
    
        # keep track of valid corners to play on (initialize to board corner only)
        if player_num == 1:
            self.valid_corners = [(0,0)]
        elif player_num == 2:
            self.valid_corners = [(board.size-1,board.size-1)]
        elif player_num == 3:
            self.valid_corners = [(0,board.size-1)]
        else :
            self.valid_corners = [(board.size-1,0)]
        
        # keep a list of places you need to check for changes to valid moves - game manager will append to this
        self.update_new_corner_adjs = []
        self.update_removals = []
        
        # maintain a list of valid moves
        self.valid_moves = self.init_valid_moves(board,pieces)
    
    # initialize valid move list
    def init_valid_moves(self,board,pieces):
        all_valid_moves = []
        
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
                    #each m represents one valid corner placement  on board for player
                    for item in self.valid_corners:
                        #find translation necessary to put piece corner into valid corner
                        x = item[0] - pieces[i][j][0].corners[k][0]
                        y = item[1] - pieces[i][j][0].corners[k][1]
                        
                        #check if move is valid
                        temp = copy.deepcopy(pieces[i][j][0])
                        temp.translate((x,y))
                        if board.check_valid_move(self.num,temp):
                            all_valid_moves.append((self.num,i,j,(x,y)))
        return all_valid_moves
        
        
    # update_valid_moves
    def update_valid_moves(self,board,pieces):
        
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
                        for item in self.update_new_corner_adj:
                            #find translation necessary to put piece corner into valid corner
                            x = item[0] - pieces[i][j][0].corners[k][0]
                            y = item[1] - pieces[i][j][0].corners[k][1]
                            
                            #check if move is valid
                            temp = copy.deepcopy(pieces[i][j])
                            temp.translate((x,y))
                            if board.check_valid_move(self.num,temp):
                                self.valid_moves.append((self.num,i,j,(x,y)))              
        
        # for item in removed_squares: search all valid_moves for moves that occupy this square and remove
        for move in self.valid_moves:
            temp_piece = pieces[move[1]][move[2]][0]
            for point in temp_piece.occupied:
                if point in self.update_removals:
                    self.valid_moves.remove(move)
                    
        # also check if square was a valid_corner and remove
        for point in self.update_removals:
            if point in self.valid_corners:
                self.valid_corners.remove(point)
                
        #reset update lists
        self.update_new_corner_adjs = []
        self.update_removals = []
        
    
    # make_move - updates all players' lists of tracked changes, updates available piecelist, returns move to Game, which will call board method to update board
    # a move will be stored as (player,piece_num,orientation,translation)
    def make_move(self,move,board,pieces):
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
                
        # add new corner_adjs to update_list
        for point in temp.corner_adjs:
            self.update_new_corner_adjs.append(point)
            
        # add occupieds and adjacents to update_list
        for point in temp.occupied:
            self.update_removals.append(point)
        for point in temp.adjacents:
            self.update_removals.append(point)
            
        #def select_move():