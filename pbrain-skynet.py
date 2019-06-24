import random
import sys
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x,y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x,y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x,y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def createBoard():
    myBoard = [[0 for i in range(19)] for j in range(19)]
    for x in range(19):
        for y in range(19):
            if board[x][y] == 1:
                myBoard[x][y] = -1
            if board[x][y] == 2:
                myBoard[x][y] = -2
    return myBoard


def checkPart(part, x, y, myBoard):
    nb_allies = part.count(-1)
    nb_enemies = part.count(-2)
    if nb_allies > 0 and nb_enemies > 0:
        return myBoard
    for i in range(5):
        if myBoard[x + i][y] >= 0:
            if nb_allies > nb_enemies:
                if nb_allies == 4:
                    myBoard[x + i][y] += 50000
                else:
                    myBoard[x + i][y] += nb_allies
            else:
                if nb_enemies == 4:
                    myBoard[x + i][y] += 5000
                if nb_enemies == 3:
                    myBoard[x + i][y] += 500
                else:
                    myBoard[x + i][y] += nb_enemies
    return myBoard


def checkVerti():
    myBoard = createBoard()
    for y in range(19):
        for x in range(15):
            part = []
            for i in range(5):
                part.append(myBoard[x + i][y])
            myBoard = checkPart(part, x, y, myBoard)
    return myBoard


def check_horizontal(x, y, map_value):
    global board
    rowinable = True
    j, k = 0, 0
    for i in range(0, 5):
        if board[x][y+i] == 1:
            j += 1
        elif board[x][y+i] == 2:
            k += 1
        i += 1
    if j >= 1 and k >= 1:
            rowinable = False
    if rowinable:
        for i in range(0, 5):
            if k == 4 or j == 4:
                if board[x][y+i] == 0:
                    if k == 4:
                        map_value[x][y+i] += 5000
                    if j == 4:
                        map_value[x][y + i] += 50000
            if k == 3 or j == 3:
                if board[x][y+i] == 0:
                    if k == 3:
                        map_value[x][y+i] += 500
                    else:
                        map_value[x][y+i] += 3
            if k == 2 or j == 2:
                if board[x][y+i] == 0:
                    map_value[x][y+i] += 2
            if k == 1 or j == 1:
                if board[x][y+i] == 0:
                    map_value[x][y+i] += 1
    return map_value


def thinkHori():
    global board
    map_value = createBoard()
    for x in range(0, 19):
        for y in range(0, 15):
            map_value = check_horizontal(x, y, map_value)
    return map_value


def partify(part, myBoard, x, y):
    nb_allies = part.count(-1)
    nb_enemies = part.count(-2)
    if nb_allies > 0 and nb_enemies > 0:
        return myBoard
    for i in range(5):
        if myBoard[x + i][y + i] >= 0:
            if nb_allies > nb_enemies:
                if nb_allies == 4:
                    myBoard[x + i][y + i] += 50000
                else:
                    myBoard[x + i][y + i] += nb_allies
            else:
                if nb_enemies == 4:
                    myBoard[x + i][y + i] += 5000
                if nb_enemies == 3:
                    myBoard[x + i][y + i] += 500
                else:
                    myBoard[x + i][y + i] += nb_enemies
    return myBoard


def partifyOp(part, myBoard, x, y):
    nb_allies = part.count(-1)
    nb_enemies = part.count(-2)
    if nb_allies > 0 and nb_enemies > 0:
        return myBoard
    for i in range(5):
        if myBoard[x - i][y + i] >= 0:
            if nb_allies > nb_enemies:
                if nb_allies == 4:
                    myBoard[x - i][y + i] += 50000
                else:
                    myBoard[x - i][y + i] += nb_allies
            else:
                if nb_enemies == 4:
                    myBoard[x - i][y + i] += 5000
                if nb_enemies == 3:
                    myBoard[x - i][y + i] += 500
                else:
                    myBoard[x - i][y + i] += nb_enemies
    return myBoard


def getPart(x, y, myBoard):
    for i in range(0, x - 3):
        part = []
        part2 = []
        k = 0
        for j in range(i, i + 5):
            part.append(myBoard[k + i][y + k + i])
            part2.append(myBoard[y + k + i][k + i])
            k += 1
        myBoard = partify(part, myBoard, i, y + i)
        if x != 18:
            myBoard = partify(part2, myBoard, y + i, i)
    return myBoard


def getPartOp(x, myBoard):
    for i in range(0, x - 3):
        part = []
        k = 0
        for j in range(i, i + 5):
            part.append(myBoard[x - k - i][k + i])
            k += 1
        myBoard = partifyOp(part, myBoard, x - i, i)
    return myBoard


def getPartRev(x, y, myBoard):
    for i in range(0, 19 - y - 4):
        part = []
        k = 0
        for j in range(i, i + 5):
            part.append(myBoard[x - i - k][y + k + i])
            k += 1
        myBoard = partifyOp(part, myBoard, x - i, y + i)
    return myBoard


def checkDiagTopRight():
    myBoard = createBoard()
    for x in range(4, 19):
        myBoard = getPart(x, 19 - (x + 1), myBoard)
    for x in range(4, 19):
        myBoard = getPartOp(x, myBoard)
    for y in range(1, 15):
        myBoard = getPartRev(18, y, myBoard)
    return myBoard


def addBoard(board1, board2, board3):
    for x in range(19):
        for y in range(19):
            board1[x][y] += board2[x][y] + board3[x][y]
    return board1


def getIndexMax(board, maxValue):
    allValue = []
    for x in range(19):
        for y in range(19):
            values = []
            if board[x][y] == maxValue:
                values.append(x)
                values.append(y)
                allValue.append(values)
    return allValue


def printBoard(myBoard):
    for i in range(19):
        for j in range(19):
            if myBoard[i][j] == -1 or myBoard[i][j] == -2:
                sys.stdout.write("9")
            else:
                sys.stdout.write(str(myBoard[i][j]))
            sys.stdout.write(" ")
        sys.stdout.write('\n')


def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    while True:
        myBoard = addBoard(thinkHori(), checkVerti(), checkDiagTopRight())
        max_value = max(list(map(max, myBoard)))
        values = getIndexMax(myBoard, max_value)
        index = random.randint(0, len(values) - 1)
        x = values[index][0]
        y = values[index][1]
        i += 1
        if pp.terminateAI:
            return
        if isFree(x,y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "/tmp/pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE,"w") as f:
	pass
# define a function for writing messages to the file
def logDebug(msg):
	with open(DEBUG_LOGFILE,"a") as f:
		f.write(msg+"\n")
		f.flush()
# define a function to get exception traceback
def logTraceBack():
	import traceback
	with open(DEBUG_LOGFILE,"a") as f:
		traceback.print_exc(file=f)
		f.flush()
	raise
# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
	logDebug("some message 1")
	try:
		logDebug("some message 2")
		1. / 0. # some code raising an exception
		logDebug("some message 3") # not logged, as it is after error
	except:
		logTraceBack()
"""
######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about


if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()