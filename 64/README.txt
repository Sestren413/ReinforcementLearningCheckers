A listing of what components are where:
Agent.py contains the logic for selecting a move and training its network.

NN.py contains the definition of the network itself.
I used FANN2 for this project so the file just uses the bindings for that.

Board.py contains my code for the simulation of the board.
The logic for determining which moves are valid is actually here, the agent just requests a list of the available valid moves.

Execute.py actually runs the games.
The code here loads stored networks, determines which players if any will train, and saves the resulting networks.

Bridge.py contains a lot of glue code to let simplecheckers talk to my board simulation.
Because the checkers dll is 32-bit and the rest of my project is 64-bit (and I didn't want to change my project as I don't know if that would affect the neural network library in any way) I have this script run as a subprocess every time I need to ask the external engine for a move. This kills performance relative to self-play and severely reduces the number of games that can be played against the engines in a reasonable timeframe. The rest of the code here just converts between the board format I use and the board format the dll takes.