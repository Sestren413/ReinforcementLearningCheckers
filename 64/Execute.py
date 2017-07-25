import NN
import Board
import Agent
import subprocess
import pickle

WHITE = 1
BLACK = 2

board = Board.Board()
nnw = NN.NeuralNet()
nnw.load('1kEEand10kself.net')
nnb = NN.NeuralNet()
nnb.new_net()
white = Agent.Agent(WHITE,nnw,board)
black = Agent.Agent(BLACK,nnb,board)

def externalmove(player,boardstate,time):
    proc = subprocess.Popen(['py','-3.5-32','Bridge.py'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return proc.communicate(pickle.dumps((boardstate,player,time)))

def run_game(iteration_cap,annotations):
    white.new_game()
    black.new_game()
    #white.randomize_net()
    black.randomize_net()
    board.reset()
    state = 0
    iteration = 0
    while(iteration < iteration_cap):
        if annotations:
            print('white next')
            print(board)
        state = white.move(annotations)
        if state!=0:
            break
        if annotations:
            print('black next')
            print(board)
        state = black.move(annotations)
        if state!=0:
            break
        iteration = iteration + 1
    if annotations:
        print('end state',state)
        print(board)
        print(iteration,'moves')
    return state

def run_game_vs_external(iteration_cap,annotations,time):
    white.new_game()
    #white.randomize_net()
    board.reset()
    state = 0
    iteration = 0
    declare = -1
    while(iteration < iteration_cap):
        if annotations:
            print('white next')
            print(board)
        state = white.move(annotations)
        if state!=0:
            declare = WHITE
            break
        if annotations:
            print('black next')
            print(board)
        rawreply,err = externalmove(BLACK,board.getstate(),time)
        reply = pickle.loads(rawreply)
        board.directupdate(reply[1])
        if reply[0] == 1:
            state = 2
        elif reply[0] == 2:
            state = 1
        elif reply[0] == 0:
            state = 3
        else:
            state = 0
        if state!=0:
            declare = BLACK
            break
        iteration = iteration + 1
    if annotations:
        print('end state',state)
        print(board)
        print(iteration,'moves')
        print(declare,'called game')
    return state

def train(w,b,result):
    if result == 1:
        if w:
            white.train(1)
        if b:
            black.train(-1)
    elif result == 2:
        if w:
            white.train(-1)
        if b:
            black.train(1)
    else:
        if w:
            white.train(0)
        if b:
            black.train(0)

def run_games(num_games):
    learning = 0
    wwin = 0
    bwin = 0
    draw = 0
    over = 0
    while learning <num_games:
        print('game',learning)
        result = run_game(1000,False)
        if result == WHITE:
            wwin = wwin + 1
            print('white',wwin,bwin,draw,over)
        if result == BLACK:
            bwin = bwin + 1
            print('black',wwin,bwin,draw,over)
        if result == 3:
            draw = draw + 1
            print('draw',wwin,bwin,draw,over)
        if result == 0:
            over = over + 1
            print('overtime',wwin,bwin,draw,over)
        #train(True,True,result)
        learning = learning + 1

    print('white:',wwin)
    print('black:',bwin)
    print('draw:',draw)
    #nnw.save('1kEEand10kself.net')

def run_games_e(num_games):
    learning = 0
    wwin = 0
    bwin = 0
    draw = 0
    over = 0
    while learning < num_games:
        print('game',learning)
        result = run_game_vs_external(1000,False,0.01)
        if result == WHITE:
            wwin = wwin + 1
            print('white',wwin,bwin,draw,over)
        if result == BLACK:
            bwin = bwin + 1
            print('black',wwin,bwin,draw,over)
        if result == 3:
            draw = draw + 1
            print('draw',wwin,bwin,draw,over)
        if result == 0:
            over = over + 1
            print('overtime',wwin,bwin,draw,over)
        train(True,False,result)
        learning = learning + 1

    print('white:',wwin)
    print('black:',bwin)
    print('draw:',draw)
    #nnw.save('1000vEasyExternal.net')

run_games(100)

#run_games_e(50)