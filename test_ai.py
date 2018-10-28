from decision import *


def test_player_turn(values: List[List[any]]) -> None:
    print('----------')
    print("[ ]['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']")
    i = 0
    for row in values:
        print('[' + str(i) + ']', end='')
        print(row)
        i += 1
    print('----------')
    print('x len: ' + str(len(values[0])))
    print('y len: ' + str(len(values)))
    print('----------')

    print('your turn')
    x = int(input("Enter X: "), 10)
    y = int(input("Enter Y: "), 10)
    values[y][x] = 'W'


def test_ai_turn(values: List[List[any]], ai_intel: Decision) -> None:
    print('----------')
    print("[ ]['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']")
    i = 0
    for row in values:
        print('[' + str(i) + ']', end='')
        print(row)
        i += 1

    print('----------')
    print('x len: ' + str(len(values[0])))
    print('y len: ' + str(len(values)))
    print('----------')

    print('ai turn')
    ai_intel.min_max(1, values, start=True)
    ai_intel.play_cell.dump()
    print(ai_intel.play_cell.eval('B'))
    values[ai_intel.play_cell.y][ai_intel.play_cell.x] = 'B'


def try_ai():
    ai_intel = Decision('B', 'B', 'W', '.')
    values = [
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........'),
        list('..........')
    ]
    while 666:
        test_player_turn(values)
        test_ai_turn(values, ai_intel)


try_ai()

