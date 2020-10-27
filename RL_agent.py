from Piece import Piece
from Board import Board
from Player import Player
from Game import Game
import numpy as np
import pickle
import random
import torch
from torch import nn,optim
from torchvision import models
from collections import deque
import copy
from heuristics import space_heuristic

import torch
import torch.nn as nn
import torch.nn.functional as F

class Q_learner(nn.Module):
    
    
    """
    FILL THIS IN LATER
    """
    
    def __init__(self,bs):
        """
        In the constructor we instantiate some nn.Linear modules and assign them as
        member variables.
        """
        super(Q_learner, self).__init__()
        
        self.feat = ResNet(BasicBlock,[2,2,2,2],num_classes = bs**2)

        start_num = self.feat.linear.out_features
        
        self.max_score = 89

        self.regress = nn.Linear(start_num,1,bias=True)
        init_val = 0.05
        nn.init.uniform_(self.regress.weight.data,-init_val,init_val)
        nn.init.uniform_(self.regress.bias.data,-init_val,init_val)
           
        self.loss_fn = nn.MSELoss()
        
        self.device = None
        
    def forward(self,state,targets = None):
        """
        Estimates value for input state
        """
        
        out = self.feat(state)
        out = self.regress(out)
        out = F.relu(out)
                      
        if self.training:
            loss = self.loss_fn(out,targets)
            return out,loss
        
        return out
    
    
'''ResNet in PyTorch.
For Pre-activation ResNet, see 'preact_resnet.py'.
Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
'''
class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion *
                               planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10):
        super(ResNet, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=1)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=1)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=1)
        self.linear = nn.Linear(512*block.expansion*4, 1)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out








def play_game(model):
    """
    Plays agent against benchmarking heuristic algorithm and random algorithm
    """
    game = Game(5,2,10)
    
    turns_since_last_move = 0
    while turns_since_last_move < 2:
        if game.turn == 1:
            move = game.player_list[0].make_move(game.game_board,game.pieces, 'space_heuristic')
            game.turn = game.turn % len(game.player_list) + 1

        else:
            states,moves = game.enumerate_current_moves()
        
            if len(moves) == 0:
                move = False
                game.turn = game.turn % len(game.player_list) + 1
            else:        
                # for each move, estimate value using model
                batched_moves = batch_moves(states,game.turn).cuda()
                    
                with torch.no_grad():
                    model.eval()
                    move_values = model(batched_moves)
                    move_values = move_values.cpu()
            
                move_val,move_idx = torch.max(move_values,dim = 0)
                game.make_move(moves[move_idx])
            
        if move == False:
            turns_since_last_move += 1
        else:
            turns_since_last_move = 0
        
        game.game_board.display2()
        
    score = game.score()
    print("Final score: heuristic {}, RL agent {}".format(score[0],score[1]))

        
def batch_moves(moves,cur_player):
    tf_moves = []
    for move in moves:
        move = torch.from_numpy(move.board)
        me = torch.eq(move,cur_player).int().float()
        you = torch.eq(move,1-cur_player).int().float()
        board = torch.eq(move,0).int().float()
        
        move = torch.stack([me,you,board])
        tf_moves.append(move)
    
    batched_moves = torch.stack(tf_moves)
    return batched_moves

def training_batch(inputs,turns):
    """
    input is batch_size x board_dim x board_dim
    turns is batchsize 
    """    
    turns = torch.tensor(turns)
    inputs = torch.stack(inputs)
    
    turns = turns.unsqueeze(1).unsqueeze(1).repeat(1,inputs.shape[1],inputs.shape[1])
    me = torch.eq(inputs,turns).int().float()
    you = torch.eq(inputs,1.0-turns).int().float()
    board = torch.eq(inputs,0).int().float()
    
    batch = torch.stack([me,you,board]).permute(1,0,2,3)
    return batch


def attention_weighted_tree_search(model,game,epsilon = 0,rollout_limit = 1000,one_player_left = False):
    """
    Estimates value of given state by recursively enumerating next states, and selecting
    a state to explore further based on values at current level
    
    model - CNN-based model for state value estimation
    game - A blokus Game object
    epsilon - this is added to the score estimate for each possible move (a higher epsilon
    is equivalent to increasing the random exploration of the agent, useful during early training stages)
    rolout_limit - the maximum number of states that will be explored before selecting a move
    
    returns:
    (state,value) - board state and value for that state as estimated by rollout
    move - integer move which can be passed to game to make the corresponding selected move
    """
    
    # need to make this recursive so that we can actually score things
    n_visited = 0
    game = copy.deepcopy(game)
    turn = game.turn -1
    
    # get all moves for current player
    states,moves = game.enumerate_current_moves()
    
    if len(moves) == 0:
        if one_player_left:
            score = game.score()
            turn = game.turn - 1
            if score[turn] > score[1-turn]:
                score = 1.0
            else:
                score = 0.0
            # score = score[turn] -score[1-turn]
            # score = score/1.0
            return None,score,None
        else:
            game.turn = game.turn % len(game.player_list) + 1
            return attention_weighted_tree_search(model,game,epsilon = epsilon, rollout_limit = rollout_limit - n_visited,one_player_left = True)
    
    else:        
        # for each move, estimate value using model
        batched_moves = batch_moves(states,turn+1).cuda()
            
        with torch.no_grad():
            model.eval()
            move_values = model(batched_moves)
            move_values = move_values.cpu()
            n_visited += len(move_values) 
        
        if rollout_limit - n_visited > 0:
            
        
            # add random exploration epsilon
            values = move_values + epsilon
            probs = torch.softmax(values,dim = 0).cpu()
            
            # randomly select a move
            cdf = probs.clone()
            rand = torch.rand(1)
            i = 0
            for i in range(1,len(cdf)):
                cdf[i] = cdf[i] + cdf[i-1]
                if rand < cdf[i]:
                    break
            
            # make move i, the first move for which the cdf is over i
            try:
                game.make_move(moves[i])
            except:
                pass
            #game.game_board.display2()

            if one_player_left:
                #switch so it is the same players turn again!
                game.turn = game.turn % len(game.player_list) + 1

            _,val,_ = attention_weighted_tree_search(model,game,epsilon = epsilon, rollout_limit = rollout_limit - n_visited,one_player_left = one_player_left)
        
            # since this value was estimated for opposite player, use negative of value
            try:
                move_values[i] = -val
            except:
                pass
        # lastly, select maximum value move and make it
        move_val,move_idx = torch.max(move_values,dim = 0)

        return states[move_idx],move_val,moves[move_idx]




def init_replay_buffer(game,buffer_size = 10000):
    game = copy.deepcopy(game)
    
    # get all moves for current player
    states,moves = game.enumerate_current_moves()
    
    if len(states) > 0:
        idx = np.random.randint(0,len(states))
        
        val = space_heuristic(1,game.game_board)
        return game.game_board,val,moves[idx]
    
    else:
        score = game.score()
        turn = game.turn-1
        
        val =  score[turn] - score[1-turn]
        return None,val,None

   
            
        
if __name__ == "__main__":
    
    # board size
    buffer_size = 1000
    batch_size = 64
    epsilon = 3
    bs = 8
    all_losses = deque(maxlen = 500)
    step = 0
    game = Game(5,2,bs)
    neither = False
    
    
    model = Q_learner(bs)
    
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    if torch.cuda.device_count() > 1:
        print("Using {} GPUs".format(torch.cuda.device_count()))
        model = nn.DataParallel(model,device_ids = [0,1,2,3])
    else:
        print("Using 1 GPU")
        
    torch.cuda.empty_cache()   
    model = model.to(device)
    model.device = device
    

    replay_buffer = deque(maxlen = buffer_size)
    # with open("heuristic_buffer.cpkl","rb") as f:
    #     replay_buffer = pickle.load(f)
    
    
    optimizer = optim.SGD(model.parameters(), lr=0.1e-4,momentum = 0.2)

   
    
    
    
    # main training loop
    while True:    
                      
        
        if True: # generate new moves online
            # add new state value pair to replay buffer
            turn = game.turn
            state,val,move = attention_weighted_tree_search(
                    model, 
                    game,
                    epsilon = epsilon, 
                    rollout_limit = 1000)
    
            #state,val,move = init_replay_buffer(game,10000)
            
            
            if move is None:
                #### Add lines to keep track of whether neither player can move, or just a single player
                if neither:
                    #game.game_board.display2()
                    game = Game(5,2,bs)
                    neither = False
                else:
                    # switch turns and indicate that if it happens again, the game is over as neither can move
                    neither = True
                    game.turn = game.turn % len(game.player_list) + 1
                
            else:
                game.make_move(move) # need to implement a Player class with qlearner backbone that can make moves
                replay_buffer.append((torch.from_numpy(state.board),val,turn))
                game.game_board.display2()
                print(val)
                
            # print((len(replay_buffer)))    
            # if len(replay_buffer) == buffer_size:
            #     with open("heuristic_buffer.cpkl","wb") as f:
            #         pickle.dump(replay_buffer,f)
            #         break
                
        if len(replay_buffer) == buffer_size:
            
            with torch.set_grad_enabled(True):
                model.train()
                
                # randomly sample from buffer
                idxs = [i for i in range(len(replay_buffer))]
                random.shuffle(idxs)
                batch_idx = idxs[:batch_size]
                batch = [replay_buffer[idx][0] for idx in batch_idx]
                batch_vals = [replay_buffer[idx][1] for idx in batch_idx] 
                turn = [replay_buffer[idx][2] for idx in batch_idx]
                
                batch = training_batch(batch,turn).to(device)
                batch_vals = torch.tensor(batch_vals)
                batch_vals_clip = torch.where(batch_vals > 0.9,torch.zeros(batch_vals.shape)+0.5, batch_vals)
                batch.vals_clip = torch.where(batch_vals < 0.1,torch.zeros(batch_vals.shape)+0.5, batch_vals)
                value,loss = model(batch,targets = batch_vals_clip)
                loss = loss.mean()
                loss.backward()
                optimizer.step()
        
                step += 1
                all_losses.append(loss)
        
                
        
        # print progress               
        if len(replay_buffer) == buffer_size and step % 1 == 0:
            mean_loss = sum(all_losses)/len(all_losses)
            print("Step {} loss: {:03f}    Running Loss: {:03f}".format(step,loss.item(),mean_loss))
        else:
            print("Buffer Size: {}".format(len(replay_buffer)))
          
        if step % 100 == 1:
            play_game(model)
            
        if step % 500 == 1:
            # with open("current_buffer.cpkl","wb") as f:
            #      pickle.dump(replay_buffer,f)
            
            epsilon = epsilon * 0.9
            print("New epsilon: {}".format(epsilon))
            torch.save(model,"q_heur_learner_step_{}.pt".format(step))
         
        if step % 2000 == 1999:
            for param_group in optimizer.param_groups:
                param_group['lr'] = param_group["lr"] * 0.5
                
                
"""
In its current state, this code doesn't really work. I was not even able to successfully train a 
network to mimic the space heuristic. As I left it, I do not think the attention weighted
rollout is implemented quite correctly in that the scores returned near the end of each game are wrong. 
I also think I may not be adding the experiences to the buffer correctly (I may not be correctly storing whose turn it
is and to whom the given score pertains.)
When you pick this project back up again, I think the place to start is fixing these issues.
Then, during training, play a whole game and only append the final n states to the 
replay buffer where n is initially 1 and grows slowly. In effect this is forcing the 
backwards flow of the states to happen slowly so the agent doesn't get bogged down with a bunch
of experiences without meaningful information (ie only state values output by the network which is at 
that point poorly trained."""