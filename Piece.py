from Board import Board
from Player import Player
from Game import Game

import numpy as np
import copy

# Implement piece as a list of coordinates
class Piece:
    
    # Constructor
    def __init__(self, size_in, p_array):
        self.size = size_in
        
        self.occupied = []
        for i in range (0,len(p_array)):
            for j in range(0,len(p_array)):
                if p_array[i,j] == 1:
                    self.occupied.append((i,j))
        
        self.corners = self.get_corners()
        self.adjacents = self.get_adjacents()
        self.diag_adjacents = self.get_diag_adjacents()
    
    #### Utilpieceity functions for translating piece
    
    #flips piece along major diagonal    
    def flip(self):   
         self.occupied[:] = [(-point[1],-point[0]) for point in self.occupied]
         self.corners[:] = [(-point[1],-point[0]) for point in self.corners]
         self.adjacents[:] = [(-point[1],-point[0]) for point in self.adjacents]
         self.diag_adjacents[:] = [(-point[1],-point[0]) for point in self.diag_adjacents]
         self.shift_min()
         return self
    
     # rotates piece by 90 degrees times input
    def rotate(self,quarter_rotations = 1):
        if quarter_rotations % 4 == 0:
            x = 0
            y = 1
            xs = 1
            ys = 1
        elif quarter_rotations == 1:
            x = 1
            y = 0
            xs = -1
            ys = 1
        elif quarter_rotations % 4 == 2:
            x = 0
            y = 1
            xs = -1
            ys = -1
        else:
            x = 1
            y = 0
            xs = 1
            ys = -1
        
        self.occupied[:] = [(xs*point[x],ys*point[y]) for point in self.occupied]
        self.corners[:] = [(xs*point[x],ys*point[y]) for point in self.corners]
        self.adjacents[:] = [(xs*point[x],ys*point[y]) for point in self.adjacents]
        self.diag_adjacents[:] = [(xs*point[x],ys*point[y]) for point in self.diag_adjacents]
        self.shift_min()
        return self
    
    # shift is a 2D tuple
    # warning - not protected against index overflow
    def translate(self, shift):
        self.occupied[:] = [(point[0]+shift[0],point[1]+shift[1]) for point in self.occupied]
        self.corners[:] = [(point[0]+shift[0],point[1]+shift[1]) for point in self.corners]
        self.adjacents[:] = [(point[0]+shift[0],point[1]+shift[1]) for point in self.adjacents]
        self.diag_adjacents[:] = [(point[0]+shift[0],point[1]+shift[1]) for point in self.diag_adjacents]
        return self
    
    def shift_min(self):
        #find min coordinates
        min_x = 0
        min_y = 0
        for point in self.occupied:
            if point[0] < min_x:
                min_x = point[0]
            if point[1] < min_y:
                min_y = point[1]
                
        #shift so all ocupied points coordinates are positive or 0
        self.occupied[:] = [(point[0]-min_x,point[1]-min_y) for point in self.occupied]
        self.corners[:] = [(point[0]-min_x,point[1]-min_y) for point in self.corners]
        self.adjacents[:] = [(point[0]-min_x,point[1]-min_y) for point in self.adjacents]
        self.diag_adjacents[:] = [(point[0]-min_x,point[1]-min_y) for point in self.diag_adjacents]
 
    
    #### Utility functions for getting specific points (used by constructor)    
    
    # returns a list of 2D tuples for adjacent spaces
    def get_adjacents(self):
        #store all 1-block translations
        aug_list = []
        for point in self.occupied:
            aug_list.append((point[0],point[1] + 1 ))
            aug_list.append((point[0],point[1] - 1 ))
            aug_list.append((point[0] - 1,point[1] ))
            aug_list.append((point[0] + 1,point[1] ))
        
        final_list = [] 
        for point in aug_list:
            if point not in self.occupied and point not in final_list:
               final_list.append(point)
      
        return final_list
    
    #returns a list of 2D tuples for diagonal adjacent squares                  
    def get_diag_adjacents(self):
        #store all 1-block diagonal translations
        aug_list = []
        for point in self.occupied:
            aug_list.append((point[0]+1,point[1]+1))
            aug_list.append((point[0]+1,point[1]-1))
            aug_list.append((point[0]-1,point[1]+1))
            aug_list.append((point[0]-1,point[1]-1))
    
        final_list = [] 
        for point in aug_list:
            if point not in self.occupied and point not in final_list and point not in self.adjacents:
               final_list.append(point)
      
        return final_list
    
    #returns a list of 2D tuples for corner squares 
    def get_corners(self):
        final_list = []
        for point in self.occupied:
            if (not ((point[0]+1,point[1]) in self.occupied and (point[0]-1,point[1]) in self.occupied)) \
            and (not ((point[0],point[1]+1) in self.occupied and (point[0],point[1]-1) in self.occupied)):
                    final_list.append(point)
        return final_list
    
    #### Utility functions for checking piece equality or similarity
    
    # checks for translational, rotational and flip symmetry 
    def is_same(self, other_piece):
        for i in range (0,4):
            if self.is_translation(other_piece.rotate(i)):
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
                return True
            else:
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
        self.flip()
        for i in range (0,4):
            if self.is_translation(other_piece.rotate(i)):
                # so piece orientations remain the same afterwards
                self.flip()
                other_piece.rotate(-i)
                return True
            else:
                # so piece orientations remain the same afterwards
                other_piece.rotate(-i)
        return False
   
    # checks for translational symmetry to another piece
    def is_translation(self,other_piece):
        a = self.piece_array()
        for i in range(0,len(a)):
            for j in range(0,len(a)):
                if np.array_equal(a, np.roll(other_piece.piece_array(),(i,j),(0,1))):
                    return True
        return False
    
    #### Other utility functions
    
    #creates a numpy array representation of piece
    def piece_array(self):
        out = np.zeros([self.size,self.size])
        for point in self.occupied:
            out[point[0],point[1]] = 1
        return out    
    
    # prints numpy representation of piece
    def show(self):
        print(self.piece_array())
        
    # returns a list of all unique orientations of the piece
    def get_orientations(self):
        #create list of all possible orientations
        orientations = []
        flipped = copy.deepcopy(self)
        flipped.flip()
        for i in range (0,4):
            orientations.append((copy.deepcopy(self.rotate(i)),False,i))
            orientations.append((copy.deepcopy(flipped.rotate(i)),True,i))
        
        #check for duplicates
        unique_orientations = []
        for item in orientations:
            unique = True
            for item2 in unique_orientations:
                if item[0].is_translation(item2[0]):
                    unique = False
            if unique:
                unique_orientations.append(item)
        
        return unique_orientations 