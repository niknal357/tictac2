#mod_type: engine
import sys
import subprocess
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--trusted-host", "pypi.org",
                          "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", package])
import time

try:
    import pygame
except:
    install('pygame')
    import pygame

def lerp(a, b, p):
    return a+b*p-a*p
def scan_for_win_and_return(grid, grid_onscreen_positions):
    GRID_SIZE_X = len(grid)
    GRID_SIZE_Y = len(grid[0])
    fail = False
    winline = None
    win = '_'
    for x in range(GRID_SIZE_X):
        for y in range(GRID_SIZE_Y):
            if grid[x][y] == '_':
                fail = True
                continue
            if x < GRID_SIZE_X-4:
                horizonal_check = True
                if y < GRID_SIZE_Y-4:
                    diagonal_check_upwards = True
                else:
                    diagonal_check_upwards = False
                if y > 3:
                    diagonal_check_downwards = True
                else:
                    diagonal_check_downwards = False
            else:
                horizonal_check = False
                diagonal_check_upwards = False
                diagonal_check_downwards = False
            if y < GRID_SIZE_Y-4:
                vertical_check = True
            else:
                vertical_check = False
            if horizonal_check:
                if grid[x][y] == grid[x+1][y] and grid[x][y] == grid[x+2][y] and grid[x][y] == grid[x+3][y] and grid[x][y] == grid[x+4][y]:
                    win = grid[x][y]
                    winline = (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['center_y'], grid_onscreen_positions[x+4][y]['right_spaced'], grid_onscreen_positions[x+4][y]['center_y'])
                    break
            if vertical_check:
                if grid[x][y] == grid[x][y+1] and grid[x][y] == grid[x][y+2] and grid[x][y] == grid[x][y+3] and grid[x][y] == grid[x][y+4]:
                    win = grid[x][y]
                    winline = (grid_onscreen_positions[x][y]['center_x'], grid_onscreen_positions[x][y]['top_spaced'], grid_onscreen_positions[x][y+4]['center_x'], grid_onscreen_positions[x][y+4]['bottom_spaced'])
                    break
            if diagonal_check_upwards:
                if grid[x][y] == grid[x+1][y+1] and grid[x][y] == grid[x+2][y+2] and grid[x][y] == grid[x+3][y+3] and grid[x][y] == grid[x+4][y+4]:
                    win = grid[x][y]
                    winline = (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['top_spaced'], grid_onscreen_positions[x+4][y+4]['right_spaced'], grid_onscreen_positions[x+4][y+4]['bottom_spaced'])
                    break
            if diagonal_check_downwards:
                if grid[x][y] == grid[x+1][y-1] and grid[x][y] == grid[x+2][y-2] and grid[x][y] == grid[x+3][y-3] and grid[x][y] == grid[x+4][y-4]:
                    winline = (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['bottom_spaced'], grid_onscreen_positions[x+4][y-4]['right_spaced'], grid_onscreen_positions[x+4][y-4]['top_spaced'])
                    win = grid[x][y]
                    break
    if win == '_' and fail == False:
        win = '-'
    return (win, winline)
def engine(bot1, bot2, grid_size=(20, 20), other_settings={}):
    if 'ld_mode' not in other_settings:
        ld_mode = 'dark'
    else:
        ld_mode = other_settings['ld_mode']
    grid = []
    for x in range(grid_size[0]):
        grid.append(['_']*grid_size[1])
    pygame.init()
    font = pygame.font.SysFont("Calibri", 24)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    x_size, y_size = screen_size = screen.get_size()
    lines = []
    playing_field_size = (0, 0)
    end_frame = 0
    winline = None
    mouse_down = True
    last_placed = None
    while playing_field_size[0] <= x_size and playing_field_size[1] <= y_size:
        playing_field_size = (playing_field_size[0]+grid_size[0], playing_field_size[1]+grid_size[1])
    playing_field_size = (playing_field_size[0]-grid_size[0], playing_field_size[1]-grid_size[1])
    playing_field_size = (playing_field_size[0]*0.9, playing_field_size[1]*0.9)
    grid_top = y_size/2-playing_field_size[1]/2
    grid_bottom = y_size/2+playing_field_size[1]/2
    grid_left = x_size/2-playing_field_size[0]/2
    grid_right = x_size/2+playing_field_size[0]/2
    grid_onscreen_positions = []
    for i in range(grid_size[0]):
        grid_onscreen_positions.append([None]*grid_size[1])
    for i in range(grid_size[0]+1):
        lines.append(((lerp(grid_left, grid_right, i/grid_size[0]), grid_top), (lerp(grid_left, grid_right, i/grid_size[0]), grid_bottom)))
    for i in range(grid_size[1]+1):
        lines.append(((grid_left, lerp(grid_top, grid_bottom, i/grid_size[1])), (grid_right, lerp(grid_top, grid_bottom, i/grid_size[1]))))
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            x_left = (x)/grid_size[0]
            y_top = (y)/grid_size[1]
            x_right = (x+1)/grid_size[0]
            y_bottom = (y+1)/grid_size[1]
            x_norm = (x+0.5)/grid_size[0]
            y_norm = (y+0.5)/grid_size[1]
            grid_onscreen_positions[x][y] = {'bottom_spaced': lerp(grid_top, grid_bottom, y_bottom)-1, 'top_spaced': lerp(grid_top, grid_bottom, y_top)+3, 'right_spaced': lerp(grid_left, grid_right, x_right)-1, 'left_spaced': lerp(grid_left, grid_right, x_left)+3, 'bottom': lerp(grid_top, grid_bottom, y_bottom)+1, 'top': lerp(grid_top, grid_bottom, y_top)+1, 'right': lerp(grid_left, grid_right, x_right)+1, 'left': lerp(grid_left, grid_right, x_left)+1, 'center_x': lerp(grid_left, grid_right, x_norm), 'center_y': lerp(grid_top, grid_bottom, y_norm)}
    running = True
    bot1_func = bot1['func']
    bot2_func = bot2['func']
    turn = 'x'
    bot_func = None
    is_human = False
    while running:
        txt = ''
        mouse_was_down = mouse_down
        mouse_down = pygame.mouse.get_pressed(num_buttons=3)[0]
        mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if bot_func == None:
            thinking_text = ''
            if turn == 'x':
                if bot1_func == None:
                    is_human = True
                    bot_func = 'human'
                else:
                    is_human = False
                    bot_func = bot1_func(grid, 'x')
            elif turn == 'o':
                if bot2_func == None:
                    is_human = True
                    bot_func = 'human'
                else:
                    is_human = True
                    bot_func = bot2_func(grid, 'o')
            elif turn == '-':
                is_human = False
                bot_func = 'turns off'
            else:
                print('invalid turn value')
        if ld_mode == 'light':
            screen.fill((190, 190, 190))
        elif ld_mode == 'dark':
            screen.fill((50, 50, 50))
        square_selected = None
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                checking_rect = pygame.Rect(grid_onscreen_positions[x][y]['left'], grid_onscreen_positions[x][y]['top'], grid_onscreen_positions[x][y]['right']-grid_onscreen_positions[x][y]['left'], grid_onscreen_positions[x][y]['bottom']-grid_onscreen_positions[x][y]['top'])
                if (x, y) == last_placed:
                    if checking_rect.collidepoint(mouse_x, mouse_y):
                        if ld_mode == 'light':
                            pygame.draw.rect(screen, (160, 160, 160), checking_rect)
                        elif ld_mode == 'dark':
                            pygame.draw.rect(screen, (80, 80, 80), checking_rect)
                        square_selected = (x, y)
                    else:
                        if ld_mode == 'light':
                            pygame.draw.rect(screen, (170, 170, 170), checking_rect)
                        elif ld_mode == 'dark':
                            pygame.draw.rect(screen, (60, 60, 60), checking_rect)
                elif checking_rect.collidepoint(mouse_x, mouse_y):
                    if ld_mode == 'light':
                        pygame.draw.rect(screen, (170, 170, 170), checking_rect)
                    elif ld_mode == 'dark':
                        pygame.draw.rect(screen, (60, 60, 60), checking_rect)
                    square_selected = (x, y)
                if grid[x][y] == 'x':
                    if ld_mode == 'light':
                        pygame.draw.line(screen, (140, 90, 90), (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['top_spaced']), (grid_onscreen_positions[x][y]['right_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']), width=2)
                        pygame.draw.line(screen, (140, 90, 90), (grid_onscreen_positions[x][y]['right_spaced'], grid_onscreen_positions[x][y]['top_spaced']), (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']), width=2)
                    elif ld_mode == 'dark':
                        pygame.draw.line(screen, (255, 128, 128), (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['top_spaced']), (grid_onscreen_positions[x][y]['right_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']), width=2)
                        pygame.draw.line(screen, (255, 128, 128), (grid_onscreen_positions[x][y]['right_spaced'], grid_onscreen_positions[x][y]['top_spaced']), (grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']), width=2)
                if grid[x][y] == 'o':
                    if ld_mode == 'light':
                        pygame.draw.ellipse(screen, (60, 140, 60), pygame.Rect(grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['top_spaced'], grid_onscreen_positions[x][y]['right_spaced']-grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']-grid_onscreen_positions[x][y]['top_spaced']), width=2)
                    elif ld_mode == 'dark':
                        pygame.draw.ellipse(screen, (128, 255, 128), pygame.Rect(grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['top_spaced'], grid_onscreen_positions[x][y]['right_spaced']-grid_onscreen_positions[x][y]['left_spaced'], grid_onscreen_positions[x][y]['bottom_spaced']-grid_onscreen_positions[x][y]['top_spaced']), width=2)
        for line in lines:
            pygame.draw.line(screen, (128, 128, 128), line[0], line[1], width=2)
        if bot_func == 'human':
            if square_selected != None:
                if mouse_down and not mouse_was_down:
                    if grid[square_selected[0]][square_selected[1]] == '_':
                        grid[square_selected[0]][square_selected[1]] = turn
                        last_placed = square_selected
                        winstate = scan_for_win_and_return(grid, grid_onscreen_positions)
                        winline = winstate[1]
                        if winstate[0] == turn:
                            if turn == 'x':
                                end_reason = 'X ('+bot1['name']+') has won!'
                            elif turn == 'o':
                                end_reason = 'O ('+bot2['name']+') has won!'
                            turn = '-'
                        elif winstate[0] == '-':
                            turn = '-'
                            end_reason = 'Draw!'
                        else:
                            if turn == 'x':
                                turn = 'o'
                            else:
                                turn = 'x'
                        bot_func = None
        elif bot_func != 'turns off':
            end_processing_time = time.time()+1/10
            res = None
            while end_processing_time > time.time():
                res = next(bot_func)
                if type(res) is str:
                    thinking_text = res
                if res != None and type(res) is not str:
                    break
            if res != None and type(res) is not str:
                if grid[res[0]][res[1]] == '_':
                    grid[res[0]][res[1]] = turn
                    last_placed = res
                    winstate = scan_for_win_and_return(grid, grid_onscreen_positions)
                    winline = winstate[1]
                    if winstate[0] == turn:
                        if turn == 'x':
                            end_reason = 'X ('+bot1['name']+') has won!'
                        elif turn == 'o':
                            end_reason = 'O ('+bot2['name']+') has won!'
                        turn = '-'
                    elif winstate[0] == '-':
                        turn = '-'
                        end_reason = 'Draw!'
                    else:
                        if turn == 'x':
                            turn = 'o'
                        else:
                            turn = 'x'
                    bot_func = None
                else:
                    bot_func = None
                    turn = '-'
                    end_reason = 'Bot made invalid move: '+str(res)
        vert_pos = 10
        txt = ''
        if turn == '-':
            txt += 'Game over!'
            if ld_mode == 'light':
                text = font.render(txt, True, (0, 0, 0))
            elif ld_mode == 'dark':
                text = font.render(txt, True, (255, 255, 255))
            screen.blit(text, (10, vert_pos))
            vert_pos += 30
            txt = 'Reason: '+end_reason
            if ld_mode == 'light':
                text = font.render(txt, True, (0, 0, 0))
            elif ld_mode == 'dark':
                text = font.render(txt, True, (255, 255, 255))
            screen.blit(text, (10, vert_pos))
            vert_pos += 30
            txt = ''
        else:
            #txt += 'turn: '+turn
            #if ld_mode == 'light':
            #    text = font.render(txt, True, (0, 0, 0))
            #elif ld_mode == 'dark':
            #    text = font.render(txt, True, (255, 255, 255))
            #screen.blit(text, (10, vert_pos))
            #vert_pos += 30
            #txt = ''
            txt += 'current turn: '
            if turn == 'x':
                txt += 'X ('+bot1['name']+')'
            elif turn == 'o':
                txt += 'O ('+bot2['name']+')'
            if ld_mode == 'light':
                text = font.render(txt, True, (0, 0, 0))
            elif ld_mode == 'dark':
                text = font.render(txt, True, (255, 255, 255))
            screen.blit(text, (10, vert_pos))
            vert_pos += 30
            txt = ''
            if thinking_text != '':
                txt+='bot is thinking: '+thinking_text
                if ld_mode == 'light':
                    text = font.render(txt, True, (0, 0, 0))
                elif ld_mode == 'dark':
                    text = font.render(txt, True, (255, 255, 255))
                screen.blit(text, (10, vert_pos))
                vert_pos += 30
                txt = ''
        if winline != None:
            if ld_mode == 'light':
                pygame.draw.line(screen, (70, 70, 70), (winline[0], winline[1]), (winline[2], winline[3]), width=3)
            elif ld_mode == 'dark':
                pygame.draw.line(screen, (255, 255, 255), (winline[0], winline[1]), (winline[2], winline[3]), width=3)
        time.sleep(max(0, end_frame-time.time()))
        pygame.display.flip()
        end_frame = time.time()+1/60
    return 'launcher'
