import Board
import numpy as np

WHITE = 1
BLACK = 2

lambd = .7

class Agent:
    def __init__(self,id,nn,board):
        self.id = id
        self.nn = nn
        self.board = board
        self.new_game()

    def new_game(self):
        self.sequence = []

    #   Piece IDS:
    #   0 - empty space
    #   1 - white man
    #   2 - white king
    #   3 - black man
    #   4 - black king
    def __prep_input(self,array):
        prepped_array = []
        for p in array: #first pass
            if p == 1:
                prepped_array.append(1)
            else:
                prepped_array.append(0)
        for p in array: #second pass
            if p == 2:
                prepped_array.append(1)
            else:
                prepped_array.append(0)
        for p in array: #third pass
            if p == 3:
                prepped_array.append(1)
            else:
                prepped_array.append(0)
        for p in array: #fourth pass
            if p == 4:
                prepped_array.append(1)
            else:
                prepped_array.append(0)
        return prepped_array

    def move(self,annotations):
        availablemoves = self.board.getmoves(self.id)
        if not availablemoves: # no moves loses the game
            if self.id == WHITE:
                return BLACK
            else:
                return WHITE
        valuations = []
        for move in availablemoves:
            if self.id == WHITE:
                valuations.append(self.nn.run(self.__prep_input(move[2])))
            else:
                valuations.append(self.nn.run(self.__prep_input(Board.cflip(move[2]))))
        valuation = np.argmax(valuations)
        nextmove = availablemoves[valuation]
        if self.id == WHITE:
            training = self.__prep_input(nextmove[2])
        else:
            training = self.__prep_input(Board.cflip(nextmove[2]))
        self.sequence.append(training)
        if annotations:
            print(self.id,nextmove[0])
        return self.board.move(self.id,nextmove[0])

    def randomize_net(self):
        self.nn.random()

    def train(self,value):
        state = self.sequence.pop()
        self.nn.train(state,value)
        while self.sequence:
            nextstate = self.sequence.pop()
            value = lambd*value + (1-lambd)*self.nn.run(state)[0]
            self.nn.train(nextstate,value)
            state = nextstate
