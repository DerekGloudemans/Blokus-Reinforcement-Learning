from Piece import Piece
from Board import Board
from Player import Player
import numpy as np
import pickle
import random
import torch
from torch import nn,optim
from torchvision import models
from collections import deque

class Q_learner(nn.Module):
    
    
    """
    FILL THIS IN LATER
    """
    
    def __init__(self):
        """
        In the constructor we instantiate some nn.Linear modules and assign them as
        member variables.
        """
        super(Q_learner, self).__init__()
        
        self.feat = models.resnet18(pretrained = False)

        start_num = self.feat.fc.out_features
        
        self.max_score = 89

        self.regress = nn.Linear(start_num,1,bias=True)
        init_val = 0.05
        nn.init.uniform_(self.regress.weight.data,-init_val,init_val)
        nn.init.uniform_(self.regress.bias.data,-init_val,init_val)
           
        self.loss_fn = nn.MSELoss()
        
    def forward(self,state,targets = None):
        """
        Estimates value for input state
        """
        
        out = self.feat(state)
        out = self.regress(out)
        out = torch.tanh(out)
        out = out * self.max_score
        
        if self.training:
            loss = self.loss_fn(out,targets)
            return out,loss
        
        return out
    

def play_game():
    """
    Plays agent against benchmarking heuristic algorithm and random algorithm
    """
    
def attention_weighted_tree_search(model,game,epsilon = 0,rollout_limit = 1000):
    """
    Estimates value of given state by recursively enumerating next states, and selecting
    a state to explore further based on values at current level
    """
    n_visited = 0
    game = copy.deepcopy(game)
    
    while n_visited < rollout_limit:
        moves = game.enumerate_current_moves()
        
        moves = torch.stack(moves)
        with torch.no_grad():
            values = model(moves)
            n_visited += len(values) 
        
        values = values + epsilon
        
        probs = torch.softmax(values)
        
        # randomly select next move
        
        game.make_move(move)

def train(model,epsilon_init = 3,buffer_size = 1000):

    
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    if torch.cuda.device_count() > 1:
        print("Using {} GPUs".format(torch.cuda.device_count()))
        model = nn.DataParallel(model,device_ids = [0,1,2,3])
    else:
        
    torch.cuda.empty_cache()   
    model = model.to(device)
    
    epsilon = epsilon_init
    replay_buffer = deque(maxlen = buffer_size)
    
    optimizer = optim.SGD(model.parameters(), lr=0.001,momentum = 0.9)

    all_losses = []
    steps = 0
    # main training loop
    while True:
        
        if game is None:
            game = Game(5,2,16)
            
        state = game.get_state() ### Needs to be implemented
        
        # add new state value pair to replay buffer
        sv_pair, move = attention_weighted_tree_search(
                model, 
                game,
                epsilon = epsilon, 
                rollout_limit = 1000)
            
        game.make_move() # need to implement a Player class with qlearner backbone that can make moves
        
        replay_buffer.append(sv_pair)
        
        if len(replay_buffer) == buffer_size:
            
            with torch.set_grad_enabled(True):
                q_learner.train()
                
                # randomly sample from buffer
                idxs = [i for i in range(bufer_size)]
                idxs.shuffle()
                batch_idx = idxs[:batch_size]
                batch = [replay_buffer[idx][0] for idx in batch_idx]
                batch_vals = [replay_buffer[idx][1] for idx in batch_idx] 
                batch = torch.stack(batch).to(device)
                batch_vals = torch.stack(batch_vals).to(device)
                
                value,loss = model(batch,targets = batch_vals)
                
                loss.backward()
                optimizer.step()
        
                steps += 1
                all_losses.append(loss)
        
        if steps % 10000 == 0:
            play_game(model)
        
            
        