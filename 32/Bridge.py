from ctypes import *
import numpy as np

def cflip(pieces):
    flip = np.copy(pieces[::-1])
    np.place(flip,flip == 3,6)
    np.place(flip,flip == 4,7)
    np.place(flip,flip == 1,3)
    np.place(flip,flip == 2,4)
    np.place(flip,flip == 6,1)
    np.place(flip,flip == 7,2)
    return flip

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

checkersdll = windll.LoadLibrary("F:/CheckerBoard/engines/simplech.dll")

OCCUPIED = 0
WHITE = 1
BLACK = 2
MAN = 4
KING = 8
FREE = 16

myboard = np.array([3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],dtype=np.int8)
updatedboard = np.array([3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],dtype=np.int8)
print(cstring(myboard))

print(WHITE|MAN,WHITE|KING,BLACK|MAN,BLACK|KING)
lookup = [(6,0),(4,0),(2,0),(0,0),(7,1),(5,1),(3,1),(1,1),(6,2),(4,2),(2,2),(0,2),(7,3),(5,3),(3,3),(1,3),(6,4),(4,4),(2,4),(0,4),(7,5),(5,5),(3,5),(1,5),(6,6),(4,6),(2,6),(0,6),(7,7),(5,7),(3,7),(1,7)]
reverselookup = [[ 3,-1, 2,-1, 1,-1, 0,-1],
                 [-1, 7,-1, 6,-1, 5,-1, 4],
                 [11,-1,10,-1, 9,-1, 8,-1],
                 [-1,15,-1,14,-1,13,-1,12],
                 [19,-1,18,-1,17,-1,16,-1],
                 [-1,23,-1,22,-1,21,-1,20],
                 [27,-1,26,-1,25,-1,24,-1],
                 [-1,31,-1,30,-1,29,-1,28]]
BoardArray = (c_int * 8) * 8

board = BoardArray()

for position in range(32):
    if myboard[position] == 0:
        board[lookup[position][0]][lookup[position][1]] = FREE
    elif myboard[position] == 1:
        board[lookup[position][0]][lookup[position][1]] = WHITE|MAN
    elif myboard[position] == 2:
        board[lookup[position][0]][lookup[position][1]] = WHITE|KING
    elif myboard[position] == 3:
        board[lookup[position][0]][lookup[position][1]] = BLACK|MAN
    elif myboard[position] == 4:
        board[lookup[position][0]][lookup[position][1]] = BLACK|KING

for position in range(8):
    strn=''
    for row in range(8):
        strn = strn + str(board[row][position])
    print(strn)

Time = c_double
time = Time(1.0)

Color = c_int
color = (BLACK)

String = c_char_p
string = String(b'')

playval = Color(0)
a = addressof(playval)
playnow = cast(a,POINTER(c_int))
print(a)
print(playnow)
print(playnow.contents)


print(string)
print(playnow)

result = checkersdll.getmove(board,color,time,string,playnow,None,None,None)

board2 = board

print(result)
for position in range(8):
    strn=''
    for row in range(8):
        strn = strn + str(board2[row][position])
    print(strn)

next = 0
for x in range(8):
    for y in range(8):
        place = reverselookup[x][y]
        if place > -1:
            brep = board[y][x]
            if brep == 5:
                next = 1
            elif brep == 9:
                next = 2
            elif brep == 6:
                next = 3
            elif brep == 10:
                next = 4
            else:
                next = 0
            print(brep,place,next)
            updatedboard[place] = next

print(myboard)
print(updatedboard)