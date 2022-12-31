'''
Driver code for the chomp game. See API documentation.

Usage: python3 driver.py [-a] [-s] [-c char] [-b row,col] rows cols

Press ctrl + c to quit.

OPTIONS
    Required
        rows
            Sets the number of rows of the game board.
        cols
            Sets the number of columns of the game board.
    Optional
        -a
            Enable AI opponent.
        -s
            Displays score of each player (number of cookies eaten).
        -c CHAR
            Sets the character representing a cookie as CHAR.
        -b ROW,COL
            Sets the blue cheese at coordinate (ROW,COL).
'''
import time
import sys
import signal
import chomp

#signal handler
def signal_handler(signum, frame):  
	print("\nExiting...")
	exit(0)

#register signal handler with interrupt signal(ctrl + c)
signal.signal(signal.SIGINT, signal_handler)

gameBoard = []
row = col = 0
showScore = False
aiEnabled = False
aiTurn = False

#parse command line args
try:
	row, col, opts = chomp.parseArgs(' '.join(sys.argv[1:])+' ')
except Exception as e:
	print("Usage: python3 driver.py [-a] [-s] [-c char] [-b row,col] rows cols")
	print(e)
	exit(0)

#[0] = ai enabled, [1] = cookie char, [2] = cheese row, [3] = cheese column
switches = []

if "-a" in opts:
	aiEnabled = True
	switches.append(True)
else:
	switches.append(False)
if "-c" in opts:
	switches.append(opts["-c"])
else:
	switches.append("c")
if "-b" in opts:
	cheeseCoords = opts["-b"].split(",")
	switches.append(int(cheeseCoords[0]))
	switches.append(int(cheeseCoords[1]))
if "-s" in opts:
	showScore = True
try:
	gameBoard, aiTurn = chomp.setup(row, col, switches)
except Exception as e:
	print("Usage: python3 driver.py [-a] [-s] [-c char] [-b row,col] rows cols")
	print(e)
	exit(0)
	
p0Score = 0
p1Score = 0

nturns = 0
chomp.renderBoard(gameBoard, p0Score, p1Score, showScore)

while True:
	if aiEnabled and aiTurn:
		move = chomp.calcAI(gameBoard, len(gameBoard), len(gameBoard[0]))
		print("I will chomp...")
		time.sleep(1.5)
		print(move)
	else:
		move = input("Player %d's turn_ " %(nturns%2))
	score = chomp.eat(gameBoard, move)
	if score < 0:
		print("Invalid move, try again: ")
		continue
	elif score == 0:
		break
		
	if nturns%2:
		p1Score += score
	else:
		p0Score += score

	chomp.renderBoard(gameBoard, p0Score, p1Score, showScore)
	nturns += 1
	if aiEnabled:
		aiTurn = not aiTurn

if nturns%2:
	print("Player 0 wins with %d cookies!" %p0Score)
else:
	print("Player 1 wins with %d cookies!" %p1Score)
