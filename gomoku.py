import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import decision as ai

pp.infotext = 'name="pbrain-PARIS-LELEU.HUBERT", author="Cedric Cescutti & Hubert Leleu", version="1.2", country="France"'

MAX_BOARD = 100
BOARD = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
GOMOKU_AI = ai.Decision(1, 1, 2, 0)


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the map")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal map size is {}".format(MAX_BOARD))
        return
    global BOARD
    BOARD = [[0 for i in range(pp.width)] for j in range(pp.height)]
    pp.pipeOut("OK")


def brain_restart():
    for y in range(pp.height):
        for x in range(pp.width):
            BOARD[y][x] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and BOARD[y][x] == 0


def brain_my(x, y):
    if isFree(x, y):
        BOARD[y][x] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        BOARD[y][x] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        BOARD[y][x] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and BOARD[y][x] != 0:
        BOARD[y][x] = 0
        return 0
    return 2


def brain_turn():
    if pp.terminateAI:
        return
    GOMOKU_AI.time_limit = pp.info_timeout_turn
    GOMOKU_AI.min_max(7, BOARD, calculus=13, reduction=2)
    if not isFree(GOMOKU_AI.play_cell.x, GOMOKU_AI.play_cell.y):
        GOMOKU_AI.play_cell = GOMOKU_AI.rescue_cell
    x = GOMOKU_AI.play_cell.x
    y = GOMOKU_AI.play_cell.y
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
        c = str(BOARD[y][x])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

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
