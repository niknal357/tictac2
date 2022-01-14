#mod_type: bot
#bot_name: Bot 8

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
    cp_grid = json.loads(json.dumps(grid))
    possible_positions = get_possible_positions(grid)
    random.shuffle(possible_positions)
    lines = [
        list('---xx_xx-'),
        list('--xxx_x--'),
        list('-xxxx_---'),
        list('--xoo_oo-'),
        list('-xooo_o--'),
        list('xoooo_---'),
        list('noooo_---'),
        list('x-ooo_o--'),
        list('--ooo_o--'),
        list('-_xxx_---'),
        list('--_xx_x_-'),
        list('-_ooo_---'),
        list('--_oo_o_-'),
        list('---oo_o_-'),
        list('--_oo_o--'),
    ]
    for line_to_defo in lines:
        yield 'checking obvious stuff'
        for pos in possible_positions:
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
    yield
    cp_grid = json.loads(json.dumps(grid))
    fork_valgrid = find_forks(grid, 'x')
    maxval = fork_valgrid[0][0]
    maxposs = [(0, 0)]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if fork_valgrid[x][y] > maxval:
                maxval = fork_valgrid[x][y]
                maxposs = [(x, y)]
            elif fork_valgrid[x][y] == maxval:
                maxposs.append((x, y))
    #print(maxval, maxposs)
    fork_valgrid = find_forks(grid, 'o')
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if fork_valgrid[x][y] > maxval:
                maxval = fork_valgrid[x][y]
                maxposs = [(x, y)]
            elif fork_valgrid[x][y] == maxval:
                maxposs.append((x, y))
    yield random.choice(maxposs)

def find_forks(grid, calculating_for):
    valgrid = []
    for x in range(len(grid)):
        valgrid.append([1]*len(grid[0]))
    checklines = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for dir in [(1, 1), (1, 0), (1, -1), (0, -1)]:
                comp = 0
                line = get_line_3(grid, (x, y), 5, dir, calculating_for=='o')
                fail = False
                for elem in line:
                    if elem == 'o' or elem == 'n':
                        fail = True
                        break
                    elif elem == 'x':
                        comp += 1
                if fail: continue
                if comp == 0: continue
                poss = []
                for i in range(5):
                    poss.append((x+dir[0]*i, y+dir[1]*i))
                checklines.append({'positions': poss, 'completion': comp, 'dir': dir})
    forks = []
    for line_index, line1 in enumerate(checklines):
        for line2 in checklines[line_index:]:
            if line1['dir'] == line2['dir']:
                continue
            intersection = None
            for pos in line1['positions']:
                if pos in line2['positions']:
                    intersection = pos
            if intersection == None: continue
            poss = []
            comp = 0
            for pos in line1['positions']:
                if pos != intersection:
                    if get_of_grid_3(grid, pos) == calculating_for:
                        comp += 1
                    poss.append(pos)
            for pos in line2['positions']:
                if pos != intersection:
                    if get_of_grid_3(grid, pos) == calculating_for:
                        comp += 1
                    poss.append(pos)
            fork = {'completion': comp, 'positions': poss}
            forks.append(fork)
            break

    #print(checklines)
    #print(forks)
    for fork in forks:
        for pos in fork['positions']:
            if get_of_grid_3(grid, pos) == '_':
                valgrid[pos[0]][pos[1]] *= fork['completion']
    return valgrid
    

def Quiqfinder(grid, placing_as):
    patterns = [
        #      placing: V
        list('-_xxx_---'),
        list('--_xx_x--'),
        list('---_x_xx-'),
        list('--xxx__--'),
        list('-x_xx_---'),
        list('--x_x_x--'),
        list('---x__xx-'),
        list('-xxx__---'),
        list('-xx_x_---'),
        list('--xx__x--'),
        list('--xx__x--'),
        list('-xx_x_---'),
        list('-__xx___-'),
        list('--__x_x__'),
        list('-_x_x__--'),
        list('--_x__x_-'),
        list('-_xx___--'),
        # to_line_3('_x_x___--'),
        # to_line_3('--_x___x_'),
        # to_line_3('_xx____--'),
        # to_line_3('_x__x__--'),
        # to_line_3('-_x___x_-'),
    ]
    #x_s = list(range(len(grid)))
    #y_s = list(range(len(grid[0])))
    # random.shuffle(x_s)
    # random.shuffle(y_s)
    # for x in x_s:
    #    for y in y_s:
    for pos in get_inflated_pos(grid):
        x, y = pos
        dirs_done = []
        cnt = 0
        for dir in ALLDIRS:
            line = get_line_3(
                grid, (x-dir[0]*5, y-dir[1]*5), 9, dir, placing_as == 'o')
            for i, pattern in enumerate(patterns):
                if invertDir(dir) in dirs_done:
                    continue
                if intersect_lines(pattern, line):
                    dirs_done.append(dir)
                    cnt += 1
                    if cnt >= 2:
                        return (x, y)
    return None

def invertDir(dir):
    return (-dir[0], -dir[1])
def get_inflated_pos(grid):
    out = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if get_of_grid_3(grid, (x, y)) != '_':
                continue
            for offset in INFLATED_OFFSETS:
                x_offset = offset[0]
                y_offset = offset[1]
                #print(x+x_offset, y+y_offset)
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

def intersect_lines(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != '-' and l2[i] != '-' and l1[i] != l2[i]:
            return False
    return True


def get_of_grid_3(grid, pos):
    if pos[0] < 0 or pos[0] > len(grid)-1 or pos[1] < 0 or pos[1] > len(grid[0])-1:
        return 'n'
    else:
        return grid[pos[0]][pos[1]]


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


def get_all_grid_poss(x_len, y_len):
    for x in range(x_len):
        for y in range(y_len):
            yield (x, y)
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
