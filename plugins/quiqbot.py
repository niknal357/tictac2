# mod_type: bot
# bot_name: Quiqbot
# version: 1.0.0
import random
try:
    import ujson as json
except:
    import json

INFLATED_OFFSETS = [(-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2),
                    (2, 2), (-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

ALLDIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0),
           (1, 0), (-1, -1), (0, -1), (1, -1)]


def bot(grid, playing_as):
    opponent = 'x'
    if playing_as == 'x':
        opponent = 'o'
    lines = [
        to_line_3('---xx_xx-'),
        to_line_3('--xxx_x--'),
        to_line_3('-xxxx_---'),
        to_line_3('--xoo_oo-'),
        to_line_3('-xooo_o--'),
        to_line_3('xoooo_---'),
        to_line_3('noooo_---'),
        to_line_3('x-ooo_o--'),
        to_line_3('--ooo_o--'),
        to_line_3('-_xxx_---'),
        to_line_3('--_xx_x_-'),
        to_line_3('-_ooo_---'),
        to_line_3('--_oo_o_-'),
        to_line_3('---oo_o_-'),
        to_line_3('--_oo_o--'),
    ]
    for line_to_defo in lines:
        for pos in get_possible_positions(grid):
            lines_to_check = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        dir = (x, y)
                        lines_to_check.append(get_line_3(
                            grid, (pos[0]-dir[0]*5, pos[1]-dir[1]*5), 9, dir, playing_as == 'o'))
            for line in lines_to_check:
                if intersect_lines(line_to_defo, line):
                    yield pos
    quiq = Quiqfinder(grid, playing_as)
    if quiq != None:
        print('self quiq')
        yield quiq
    yield
    quiq = Quiqfinder(grid, opponent)
    if quiq != None:
        print('opponent quiq')
        yield quiq
    yield
    yield random.choice(get_inflated_pos(grid))


def get_of_grid_3(grid, pos):
    if pos[0] < 0 or pos[0] > len(grid)-1 or pos[1] < 0 or pos[1] > len(grid[0])-1:
        return 'n'
    else:
        return grid[pos[0]][pos[1]]


def invertDir(dir):
    return (-dir[0], -dir[1])


def dirToStr(dir):
    return str(dir[0])+'x'+str(dir[1])


def Quiqfinder(grid, placing_as):
    patterns = [
        #      placing: V
        to_line_3('-_xxx_o--'),
        to_line_3('--_xx_xo-'),
        to_line_3('---_x_xxo'),
        to_line_3('-oxxx__--'),
        to_line_3('-x_xx_o--'),
        to_line_3('--x_x_xo-'),
        to_line_3('---x__xxo'),
        to_line_3('oxxx__---'),
        to_line_3('-xx_x_o--'),
        to_line_3('--xx__xo-'),
        to_line_3('-oxx__x--'),
        to_line_3('oxx_x_---'),
        to_line_3('-__xx___-'),
        to_line_3('--__x_x__'),
        to_line_3('-_x_x__--'),
        to_line_3('--_x__x_-'),
        to_line_3('-_xx___--'),
        # to_line_3('_x_x___--'),
        # to_line_3('--_x___x_'),
        # to_line_3('_xx____--'),
        # to_line_3('_x__x__--'),
        # to_line_3('-_x___x_-'),
    ]
    # x_s = list(range(len(grid)))
    # y_s = list(range(len(grid[0])))
    # random.shuffle(x_s)
    # random.shuffle(y_s)
    # for x in x_s:
    #    for y in y_s:
    for pos in get_inflated_pos(grid):
        x, y = pos
        matched = {}
        for dir in ALLDIRS:
            matched[dirToStr(dir)] = None
        cnt = 0
        for dir in ALLDIRS:
            line = get_line_3(
                grid, (x-dir[0]*5, y-dir[1]*5), 9, dir, placing_as == 'o')
            for i, pattern in enumerate(patterns):
                if matched[dirToStr(invertDir(dir))] != i:
                    if intersect_lines(pattern, line):
                        matched[dirToStr(dir)] = i
                        cnt += 1
                        if cnt >= 2:
                            return (x, y)
    return None


def to_line_3(string):
    out = []
    for char in string:
        out.append(char)
    return out


def get_line_3(grid, pos, dist, dir, invert=False):
    out = []
    for i in range(dist):
        curpos = (pos[0]+dir[0]*i, pos[1]+dir[1]*i)
        item = get_of_grid_3(grid, curpos)
        if invert:
            if item == 'x':
                out.append('o')
            elif item == 'o':
                out.append('x')
            else:
                out.append(item)
        else:
            out.append(item)
    return out


def intersect_lines(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != '-' and l2[i] != '-' and l1[i] != l2[i]:
            return False
    return True


def get_inflated_pos(grid):
    out = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if get_of_grid_3(grid, (x, y)) != '_':
                continue
            for offset in INFLATED_OFFSETS:
                x_offset = offset[0]
                y_offset = offset[1]
                # print(x+x_offset, y+y_offset)
                if get_of_grid_3(grid, (x+x_offset, y+y_offset)) in ['x', 'o']:
                    out.append((x, y))
                    break
            # for x_offset in range(-2, 3):
            #    for y_offset in range(-2, 3):
            #        if x_offset == 0 and y_offset == 0:
            #            continue
            #        if get_of_grid_3(grid, (x+x_offset, y+y_offset)) in ['x', 'o']:
            #            out.append((x, y))
            #            done = True
            #            break
            #    if done:
            #        break
    # print(out)
    if len(out) == 0:
        out.append((len(grid)//2, len(grid[0])//2))
    return out


def get_possible_positions(grid):
    possible_positions = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != '_':
                left_good = False
                right_good = False
                up_good = False
                down_good = False
                if x < len(grid)-1:
                    right_good = True
                if x > 0:
                    left_good = True
                if y < len(grid[0])-1:
                    down_good = True
                if y > 0:
                    up_good = True
                if up_good and left_good and grid[x-1][y-1] == '_':
                    if (x-1, y-1) not in possible_positions:
                        possible_positions.append((x-1, y-1))
                if up_good and grid[x][y-1] == '_':
                    if (x, y-1) not in possible_positions:
                        possible_positions.append((x, y-1))
                if right_good and up_good and grid[x+1][y-1] == '_':
                    if (x+1, y-1) not in possible_positions:
                        possible_positions.append((x+1, y-1))
                if left_good and grid[x-1][y] == '_':
                    if (x-1, y) not in possible_positions:
                        possible_positions.append((x-1, y))
                if right_good and grid[x+1][y] == '_':
                    if (x+1, y) not in possible_positions:
                        possible_positions.append((x+1, y))
                if down_good and left_good and grid[x-1][y+1] == '_':
                    if (x+1, y+1) not in possible_positions:
                        possible_positions.append((x-1, y+1))
                if down_good and grid[x][y+1] == '_':
                    if (x, y+1) not in possible_positions:
                        possible_positions.append((x, y+1))
                if right_good and down_good and grid[x+1][y+1] == '_':
                    if (x+1, y+1) not in possible_positions:
                        possible_positions.append((x+1, y+1))
    if len(possible_positions) == 0:
        return [(len(grid)//2, len(grid[0])//2)]
    return possible_positions
