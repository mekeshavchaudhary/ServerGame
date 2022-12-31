

from random import randint

the_cookie = '🍪'
def setup(rows, cols, switches):
    print(switches)
    b_x = int(switches[2])
    b_y = int(switches[3])
    game_borad = [[switches[1] for i in range(int(cols))]for i in range(int(rows))]
    # checking the validity & placing the blue cheese
    if 0<=b_x<=int(cols) and  0<=b_y<=int(rows) :
        game_borad[switches[2]][switches[3]] = "#"
    else:
        raise Exception("Blue cheese out of bounds")
    # for i in game_borad:
    #     print(i)

    cpu_trun = False
    if(randint(0, 10)%2==0):
        cpu_trun = True
    return game_borad,cpu_trun

def parseArgs(argv):
    #This is my function
    argv = argv.split(' ')
    index = 0
    for elem in argv:
        match elem:
            case '-a':
                ai_enabled = True
            case '-s':
                show_score = True
            case '-c':
                index+=1
                cookie_character = argv[index]
                the_cookie = cookie_character
            case '-b':
                blue_cheese_coords = argv[index]
                break
        index+=1
    board_rows = argv[-3]
    board_columns = argv[-2]
    opts = {
        '-a' : True,
        '-c' : cookie_character,
        '-b' : blue_cheese_coords,
        '-s' : True
    }
    return board_rows, board_columns, opts
    

def renderBoard(board, score1, score2, showScore=False):
    #drawing the board
    for r in board:
        print()
        print("-"*40)
        for i in r:
            print(f" {i} |",end='')
    if showScore:
        print()
        print("-"*40)
        print()
        print("-"*40)
        print("|\t\tPLAYER 1 :: "+str(score1)+"\t\t|")
        print("|\t\tPLAYER 2 :: "+str(score2)+"\t\t|")
        print("-"*40)

def calcAI(board, rows, cols):
    # find the possible move that does not have the blue cheese in the way
    #the random approach

    # eat(board, f"{str(move_x)},{str(move_y)}")
    # The Diagonal Approach - Starting the diagonals from the top left corner gives maximum number of points So AI will be starting from there
    
    tc = 0
    diags = []
    allDiagFin = False
    if allDiagFin == False:
        for i in range(int(rows)):
            asd = False
            if board[i][i] == '#' or board[i][i] == 'X':
                continue
            else:
                asd = True
                pp=True
                for c in range(i, len(board[0])):
                    #UP->DOWN
                    if(board[c][i]=='#'):
                        pp=False
                    break 
                for c in range(i, len(board)):
                    #LEFT->RIGHT
                    if(board[i][i]=='#'):
                        pp=False
                    break 
                if pp:
                    return f"{i},{i}"
            if not asd:
                allDiagFin = True
    else:
        while(True):
            move_x = randint(1,int(cols)-1)
            move_y = randint(1,int(rows)-1)
            if(board[move_x][move_y]=='#'):
                continue
            else:
                break
        # print(diags)
                
    return f"{move_x},{move_y}"

def eat(board, move):
    #Check if the move is valid
    mv_x = move.split(',')[0]
    mv_y = move.split(',')[1]
    mv_x=int(mv_x)
    mv_y=int(mv_y)
    cookie_chomped = 0
    if(0<=mv_y<=len(board) and 0<=mv_x<=len(board[0])):
        #move is valid
        #check if it hits the cheese
        for i in range(mv_x, len(board[0])):
            #UP->DOWN
            if(board[i][mv_y]=='#'):
                return 0
            board[i][mv_y] = 'X'
            cookie_chomped+=1
        for i in range(mv_y, len(board)):
            #LEFT->RIGHT
            if(board[mv_x][i]=='#'):
                return 0
            board[mv_x][i] = 'X'
            cookie_chomped+=1
        renderBoard(board, 0,0,True)
        return cookie_chomped
    return -1

if __name__ == "__main__":
    import sys