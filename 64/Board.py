import numpy as np

WHITE = 1
BLACK = 2

def cstring(pieces):
    string = ''
    for idx,p in enumerate(pieces):
        if idx%8 < 4:
            string += '◼'
        if p == 0:
            string += '◻'
        elif p == 1:
            string += '\u26C0'
        elif p == 2:
            string += '\u26C1'
        elif p == 3:
            string += '\u26C2'
        elif p == 4:
            string += '\u26C3'
        else:
            string += '?'
        if idx%8 > 3:
            string += '◼'
        if idx%4 == 3:
            string += '\n'
    return string

def cstring2(pieces):
    string = ''
    for idx,p in enumerate(pieces):
        if idx%8 < 4:
            string += '◼'
        if p == 0:
            string += '◻'
        elif p == 1:
            string += 'w'
        elif p == 2:
            string += 'W'
        elif p == 3:
            string += 'b'
        elif p == 4:
            string += 'B'
        else:
            string += '?'
        if idx%8 > 3:
            string += '◼'
        if idx%4 == 3:
            string += '\n'
    return string

def reference():
    print('◼0◼1◼2◼3\n4◼5◼6◼7◼\n◼8◼9◼0◼1\n2◼3◼4◼5◼\n◼6◼7◼8◼9\n0◼1◼2◼3◼\n◼4◼5◼6◼7\n8◼9◼0◼1◼\n')

def cflip(pieces):
    flip = np.copy(pieces[::-1])
    np.place(flip,flip == 3,6)
    np.place(flip,flip == 4,7)
    np.place(flip,flip == 1,3)
    np.place(flip,flip == 2,4)
    np.place(flip,flip == 6,1)
    np.place(flip,flip == 7,2)
    return flip

def printmoves(afterstates):
    for r in afterstates:
        print(r[0],' ',r[1],'\n',cstring(r[2]),sep='')

class Board:
#   Piece IDS:
#   0 - empty space
#   1 - white man
#   2 - white king
#   3 - black man
#   4 - black king
# using internal representation in the style of Portable Draughts Notation
# that is, the 32 valid squares listed in sequence left-to-right top-to-bottom

    def __init__(self):
        self.reset()

    def reset(self):
        self.pieces = np.array([3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],dtype=np.int8)
        self.old = [np.copy(self.pieces)]

    def getstate(self):
        return self.pieces

    def getmoves(self,playerid): # returns a list of all valid moves and the resulting afterstates
        assert playerid in [WHITE,BLACK]
        jumps = self.checkjumps(playerid,self.pieces,0)
        if jumps:
            return jumps
        return self.checkmoves(playerid)

    def checkmoves(self,playerid):
        result = []
        for idx,p in enumerate(self.pieces): # identify potential destinations
            if (playerid == WHITE and p in [1,2]) or (playerid == BLACK and p in [3,4]): # only consider player's pieces
                row = int(idx/4)
                if idx%8 < 4:   # row of form ◼◻◼◻◼◻◼◻
                    potential = [idx+4,idx+5,idx-4,idx-3]
                else:           # row of form ◻◼◻◼◻◼◻◼
                    potential = [idx + 4,idx + 3,idx - 4,idx - 5]
                for dest in potential:
                    drow = int(dest/4)
                    if (dest >= 0 and dest <= 31) and (drow == row+1 or drow == row-1) and (p in [2,4] or (p == 1 and dest < idx) or (p == 3 and dest > idx)) and (self.pieces[dest] == 0):
                        afterstate = np.copy(self.pieces)
                        afterstate[idx] = 0
                        afterstate[dest] = p
                        move = ((idx,dest),-1,afterstate)
                        result.append(move)
        return result

    def checkjumps(self,playerid,pieces,depth):
        result = []
        #print('Checking jumps for depth ',depth,'\n',cstring(pieces),sep='')
        for idx,p in enumerate(pieces): # identify potential destinations
            if (playerid == WHITE and p in [1,2]) or (playerid == BLACK and p in [3,4]): # only consider player's pieces
                row = int(idx / 4)
                if idx % 8 < 4: # row of form ◼◻◼◻◼◻◼◻
                    potential = [(idx + 4,idx+7),(idx + 5,idx+9),(idx - 4,idx-9),(idx - 3,idx-7)]
                else:           # row of form ◻◼◻◼◻◼◻◼
                    potential = [(idx + 4,idx+9),(idx + 3,idx+7),(idx - 4,idx-7),(idx - 5,idx-9)]
                for dest in potential:
                    drow = int(dest[0] / 4)
                    drow2 = int(dest[1] / 4)
                    if (dest[1] >= 0 and dest[1] <= 31) and (drow == row+1 or drow == row-1) and (drow2 == row+2 or drow2 == row-2) and (p in [2,4] or (p == 1 and dest[0] < idx) or (p == 3 and dest[0] > idx)) and (pieces[dest[1]] == 0) and ((playerid == BLACK and pieces[dest[0]] in [1,2]) or (playerid == WHITE and pieces[dest[0]] in [3,4])):
                        afterstate = np.copy(pieces)
                        afterstate[idx] = 0
                        afterstate[dest[0]] = 0
                        afterstate[dest[1]] = p
                        #print(idx,' ',dest[1],' ',depth,'\n',cstring(afterstate),sep='')
                        move = [((idx,dest[0],dest[1]),depth,afterstate)]
                        recurse = self.chainjumps(playerid,afterstate,depth+1,dest[1])
                        if recurse:
                            for ridx,r in enumerate(recurse):
                                recurse[ridx] = ((idx,dest[0])+r[0],r[1],r[2])
                            result += recurse
                        else:
                            result += move
        return result

    def chainjumps(self,playerid,pieces,depth,piece):
        result = []
        #print('Checking jumps for depth ',depth,'\n',cstring(pieces),sep='')
        idx = piece
        p = pieces[piece]

        row = int(idx / 4)
        if idx % 8 < 4: # row of form ◼◻◼◻◼◻◼◻
            potential = [(idx + 4,idx+7),(idx + 5,idx+9),(idx - 4,idx-9),(idx - 3,idx-7)]
        else:           # row of form ◻◼◻◼◻◼◻◼
            potential = [(idx + 4,idx+9),(idx + 3,idx+7),(idx - 4,idx-7),(idx - 5,idx-9)]
        for dest in potential:
            drow = int(dest[0] / 4)
            drow2 = int(dest[1] / 4)
            if (dest[1] >= 0 and dest[1] <= 31) and (drow == row+1 or drow == row-1) and (drow2 == row+2 or drow2 == row-2) and (p in [2,4] or (p == 1 and dest[0] < idx) or (p == 3 and dest[0] > idx)) and (pieces[dest[1]] == 0) and ((playerid == BLACK and pieces[dest[0]] in [1,2]) or (playerid == WHITE and pieces[dest[0]] in [3,4])):
                afterstate = np.copy(pieces)
                afterstate[idx] = 0
                afterstate[dest[0]] = 0
                afterstate[dest[1]] = p
                #print(idx,' ',dest[1],' ',depth,'\n',cstring(afterstate),sep='')
                move = [((idx,dest[0],dest[1]),depth,afterstate)]
                recurse = self.chainjumps(playerid,afterstate,depth+1,dest[1])
                if recurse:
                    for ridx,r in enumerate(recurse):
                        recurse[ridx] = ((idx,dest[0])+r[0],r[1],r[2])
                    result += recurse
                else:
                    result += move
        return result

    # move checks validity of request
    # but it does not check to see if men are jumping backwards
    # these checks are just to catch bugs so I don't figure its too big a deal
    def move(self,playerid,move):
        if False:
            try:
                place = -1
                # move request follows format
                if len(move) != 2:
                    assert len(move)%2 == 1

                # move request is moving own piece
                if playerid == WHITE:
                    assert self.pieces[move[0]] in [1,2]
                else:
                    assert self.pieces[move[0]] in [3,4]

                # move request is legal
                if len(move) == 2:
                    assert self.pieces[move[1]] == 0 #empty destination
                else:
                    for place in range(len(move)):
                        if place%2 == 1:# jumping over hostile piece
                            if playerid == WHITE:
                                assert self.pieces[move[place]] in [3,4]
                            else:
                                assert self.pieces[move[place]] in [1,2]
                        if place%2 == 0 and place != 0:# jumping into empty space
                            assert self.pieces[move[place]] == 0
            except AssertionError:
                reference()
                print(cstring(self.pieces))
                print(playerid,move,place)
                exit(1)

        # execute move
        if len(move) == 2:
            self.pieces[move[1]] = self.pieces[move[0]]
            self.pieces[move[0]] = 0
        else:
            self.pieces[move[-1]] = self.pieces[move[0]]
            self.pieces[move[0]] = 0
            for place in range(len(move)):
                if place%2 == 1:# remove jumped
                    self.pieces[move[place]] = 0

        # promote kings
        for idx,p in enumerate(self.pieces):
            if idx in [0,1,2,3] and p == 1:
                self.pieces[idx] = 2
            if idx in [28,29,30,31] and p == 3:
                self.pieces[idx] = 4

        # check victory
        end = 0
        whitetest = np.in1d([1,2],self.pieces,invert=True)
        blacktest = np.in1d([3,4],self.pieces,invert=True)
        if(whitetest[0] and whitetest[1]):# no white pieces
            end = BLACK # black wins
        if(blacktest[0] and blacktest[1]):# no black pieces
            end = WHITE # white wins

        # check stalemate
        for old_pieces in self.old:
            if np.array_equal(old_pieces,self.pieces):
                #print(self.pieces)
                #print(self.old)
                end = 3
        else:
            self.old.append(np.copy(self.pieces))
            self.old = self.old[-16:]# just keep 16 previous states for memory reasons

        return end

    def directupdate(self,newboard):
        self.pieces = newboard

    def setspace(self,loc,piece):
        self.pieces[loc] = piece

    def __str__(self):
        return cstring2(self.pieces)

