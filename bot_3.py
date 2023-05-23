# mod_type: bot
# bot_name: Bot 3
# version: 1.0.0

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


def intersect_lines(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != '-' and l2[i] != '-' and l1[i] != l2[i]:
            return False
    return True


def eval_line_3(line_ingrid):
    lines = [
        {'value': 'inf', 'line': list('-xxxx_---')},
        {'value': 'inf', 'line': list('--xxx_x--')},
        {'value': 'inf', 'line': list('---xx_xx-')},
        {'value': 'inf',  'line': list('---oo_oo-')},
        {'value': 'inf',  'line': list('--ooo_o--')},
        {'value': 'inf',  'line': list('xoooo_---')},
        {'value': 'inf',  'line': list('noooo_---')},
        {'value': 14,     'line': list('-_xxx__--')},
        {'value': 10,     'line': list('-_xxx_n--')},
        {'value': 14,     'line': list('--_xx_x_-')},
        {'value': 13,     'line': list('---oo_o--')},
        {'value': 12,     'line': list('-_ooo_---')},
        {'value': 5,     'line': list('-__xx___-')},
        {'value': 5,     'line': list('--__x_x__')},
        {'value': 4,     'line': list('-xooo__--')},
        {'value': 4,     'line': list('--_xx__--')},
        {'value': 4,     'line': list('---_x_x_-')},
        {'value': 3,     'line': list('----o_o--')},
        {'value': 2,     'line': list('---oo_---')},
        {'value': 1,     'line': list('----x_---')},
        # {'value': 0,    'line': to_line_3('----o_---')},
    ]
    value = 0
    for line_inlist in lines:
        if intersect_lines(line_ingrid, line_inlist['line']):
            if line_inlist['value'] == 'inf':
                return 'inf'
            else:
                value += 3**line_inlist['value']
    return value


def eval_pos_3(grid, pos, playing_as):
    sum = 0
    lines_to_check = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                dir = (x, y)
                lines_to_check.append(get_line_3(
                    grid, (pos[0]-dir[0]*5, pos[1]-dir[1]*5), 9, dir, playing_as == 'o'))
    for line in lines_to_check:
        calc = eval_line_3(line)
        if calc == 'inf':
            return 'inf'
        else:
            sum += calc
    return sum


def bot(grid, playing_as, return_sorted=False):
    possible_positions = get_possible_positions(grid)
    if len(possible_positions) == 0:
        if return_sorted:
            yield [{'pos': [len(grid)//2, len(grid[0])//2], 'val': 0}]
        yield ([len(grid)//2, len(grid[0])//2])
    positions_to_go = []
    for position in possible_positions:
        eval = eval_pos_3(grid, position, playing_as)
        if eval == 'inf':
            if return_sorted:
                yield [{'pos': position, 'val': 100000000000000000000000000000000}]
            yield position
        else:
            positions_to_go.append({'pos': position, 'val': eval})
    positions_to_go = sorted(positions_to_go, key=lambda d: d['val'])
    if return_sorted:
        yield positions_to_go
    yield positions_to_go[-1]['pos']


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
