import numpy as np
from Board import Board
import time

# space_heuristic() - returns the decimal ratio of space "controlled" by 
# the given board state determined by means of iterative flooding of neighboring squares
# player_num - int 
# board - Board object (pass a copy of the board)
# NOTE - probably favors player in bottom right due to sequential coloring
def space_heuristic(player_num,board_obj,verbose = False):

    board = board_obj.board
    controlled_by_player_init = sum(sum(board == player_num))
    #loops as long as squares are changing color still
    changes_made = True
    while changes_made:
        
        changes_made = False
        #create copy so changes don't immediately get added
        new_board = np.zeros([board_obj.size,board_obj.size])
        
        #for each square
        for i in range(0,board_obj.size):
            for j in range(0,board_obj.size):
                val = board[i,j]
                # if any player occupies said square
                if val != 0:
                    new_board[i,j] = val
                    
                    #color each unclaimed neighbor in range
                    if i >= 0 and i < len(board) and j >= -1 and j < len(board)-1:
                        if board[i,j+1] == 0:
                            changes_made = True
                            new_board[i,j+1] = val
                    if i >= 0 and i < len(board) and j >= 1 and j < len(board)+1:
                        if board[i,j-1] == 0:
                            changes_made = True
                            new_board[i,j-1] = val 
                    if i >= -1 and i < len(board)-1 and j >= -1 and j < len(board)-1:
                        if board[i+1,j] == 0:
                            changes_made = True
                            new_board[i+1,j] = val
                    if i >= 1 and i < len(board)+1 and j >= -1 and j < len(board)-1:
                        if board[i-1,j] == 0:
                            changes_made = True
                            new_board[i-1,j] = val
                            
        # copies changes to board
        board = new_board
        
        if verbose:
            print(board)
            print("\n")
        
    # return ratio of squares controlled by player plus added bonus for playing larger pieces
    controlled_by_player = sum(sum(board == player_num))
    ret =  (controlled_by_player / float(board_obj.size**2)) + controlled_by_player_init/100.0
    return ret


def space_heuristic_train(player_num,board_obj,verbose = False):

    board = board_obj.board
    controlled_by_player_init = sum(sum(board == player_num))
    #loops as long as squares are changing color still
    changes_made = True
    while changes_made:
        
        changes_made = False
        #create copy so changes don't immediately get added
        new_board = np.zeros([board_obj.size,board_obj.size])
        
        #for each square
        for i in range(0,board_obj.size):
            for j in range(0,board_obj.size):
                val = board[i,j]
                # if any player occupies said square
                if val != 0:
                    new_board[i,j] = val
                    
                    #color each unclaimed neighbor in range
                    if i >= 0 and i < len(board) and j >= -1 and j < len(board)-1:
                        if board[i,j+1] == 0:
                            changes_made = True
                            new_board[i,j+1] = val
                    if i >= 0 and i < len(board) and j >= 1 and j < len(board)+1:
                        if board[i,j-1] == 0:
                            changes_made = True
                            new_board[i,j-1] = val 
                    if i >= -1 and i < len(board)-1 and j >= -1 and j < len(board)-1:
                        if board[i+1,j] == 0:
                            changes_made = True
                            new_board[i+1,j] = val
                    if i >= 1 and i < len(board)+1 and j >= -1 and j < len(board)-1:
                        if board[i-1,j] == 0:
                            changes_made = True
                            new_board[i-1,j] = val
                            
        # copies changes to board
        board = new_board
        
        if verbose:
            print(board)
            print("\n")
        
    # return ratio of squares controlled by player plus added bonus for playing larger pieces
    controlled_by_player = sum(sum(board == player_num))
    
    if player_num == 1:
        other = 2
    else:
        other = 1
    controlled_by_opponent = sum(sum(board == other))
    
    ret =  controlled_by_player - controlled_by_opponent + controlled_by_player_init/100.0
    return ret

def space_heuristic2(player_num,board_obj,verbose = False):

    board = board_obj.board
    controlled_by_player_init = sum(sum(board == player_num))
    #loops as long as squares are changing color still
    changes_made = True
    while changes_made:
        
        changes_made = False
        #create copy so changes don't immediately get added
        new_board = np.zeros([board_obj.size,board_obj.size])
        
        #for each square
        for i in range(0,board_obj.size):
            for j in range(0,board_obj.size):
                val = board[i,j]
                # if any player occupies said square
                if val != 0:
                    new_board[i,j] = val
                    
                    #color each unclaimed neighbor in range
                    if i >= -1 and i < len(board)-1 and j >= -1 and j < len(board)-1:
                        if board[i+1,j+1] == 0:
                            changes_made = True
                            new_board[i+1,j+1] = val
                    if i >= -1 and i < len(board)-1 and j >= 1 and j < len(board)+1:
                        if board[i+1,j-1] == 0:
                            changes_made = True
                            new_board[i+1,j-1] = val 
                    if i >= 1 and i < len(board)+1 and j >= 1 and j < len(board)+1:
                        if board[i-1,j-1] == 0:
                            changes_made = True
                            new_board[i-1,j-1] = val
                    if i >= 1 and i < len(board)+1 and j >= -1 and j < len(board)-1:
                        if board[i-1,j+1] == 0:
                            changes_made = True
                            new_board[i-1,j+1] = val
                            
        # copies changes to board
        board = new_board
        
        if verbose:
            print(board)
            print("\n")
        
    # return ratio of squares controlled by player plus added bonus for playing larger pieces
    controlled_by_player = sum(sum(board == player_num))
    ret =  (controlled_by_player / float(board_obj.size**2)) + controlled_by_player_init/100.0
    return ret

if True: #test block        
    testBoard = Board(20)
    testBoard.board[10,10] = 1  
    testBoard.board[15,15] = 2  
    start = time.time()    
    x = space_heuristic2(1,testBoard)     
    end = time.time()
    
    elapsed = (end-start)
    print("Time elapsed: {} sec".format(elapsed))