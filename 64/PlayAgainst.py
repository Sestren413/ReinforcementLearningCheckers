import Board
import NN
import Agent
import ast

WHITE = 1
BLACK = 2

def take_move():
    command = input('-->')
    if command == 'moves':
        moves = board.getmoves(WHITE)
        Board.printmoves(moves)
        command = input('-->')
    tuple = ast.literal_eval('('+command+')')
    return board.move(WHITE,tuple)

board = Board.Board()
nn = NN.NeuralNet()
nn.load('game.net')
#white = Agent.Agent(WHITE,nn,board)
black = Agent.Agent(BLACK,nn,board)

black.new_game()
board.reset()
state = 0
iteration = 0
annotations = True
while(iteration < 1000):
    if annotations:
        print('white next')
        print(board)
    state = take_move()
    if state!=0:
        break
    if annotations:
        print('black next')
        print(board)
    state = black.move()
    if state!=0:
        break
    iteration = iteration + 1
if annotations:
    print('end state',state)
    print(board)
    print(iteration,'moves')
