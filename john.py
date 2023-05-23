# mod_type: bot
# bot_name: Beginner John

import random
import json

prev_board = None
INFLATED_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]


def bot(grid, playing_as):
    global global_text, prev_board
    global_text = ''
    opponent = 'x' if playing_as == 'o' else 'o'
    yield
    attention = []
    if prev_board == None:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                attention.append((x, y))
    else:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if prev_board[x][y] != grid[x][y]:
                    for xd in range(-2, 3):
                        for yd in range(-2, 3):
                            if x+xd >= 0 and x+xd < len(grid) and y+yd >= 0 and y+yd < len(grid[x+xd]):
                                attention.append((x+xd, y+yd))
    if len(attention) == 0:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == playing_as:
                    attention.append((x, y))
    random.shuffle(attention)
    print(attention)
    if random.random() > 0.3:
        possible_positions = []
        for x, y in attention:
            if grid[x][y] == '_':
                prev_board = json.loads(json.dumps(grid))
                possible_positions.append((x, y))
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
            list('---xx_---'),
            list('----x_x--'),
            list('----x_-x-'),
            list('---x-_-x-'),
        ]
        for line_to_defo in lines:
            yield
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
    yield random.choice(get_inflated_pos(grid))


def intersect_lines(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != '-' and l2[i] != '-' and l1[i] != l2[i]:
            return False
    return True


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


def get_of_grid_3(grid, pos):
    if pos[0] < 0 or pos[0] > len(grid)-1 or pos[1] < 0 or pos[1] > len(grid[0])-1:
        return 'n'
    else:
        return grid[pos[0]][pos[1]]


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
