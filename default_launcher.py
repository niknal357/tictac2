# mod_type: launcher

import time
import math
import random
import os
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--trusted-host", "pypi.org",
                          "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", package])
try:
    import pygame
except:
    install('pygame')
    import pygame
#from perlin_noise import PerlinNoise
import colorsys

#noise = PerlinNoise(octaves=2)

VERSION = 'dev0.1'

C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)

def lerp(a, b, p):
    return a+b*p-a*p

button_selections = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}

ld_mode = 'dark'

BUTTON_ENLARGEMENT = 10

def draw_button(surface: pygame.Surface, region_top_left_corner: tuple, region_size: tuple, txt: str, mouse_pos: tuple, id: str, mouse_down: bool, font: pygame.font.Font):
    global button_selections
    full_top = region_top_left_corner[1]
    full_left = region_top_left_corner[0]
    full_right = full_left+region_size[0]
    full_bottom = full_top+region_size[1]
    deselected_top = region_top_left_corner[1]+BUTTON_ENLARGEMENT
    deselected_left = region_top_left_corner[0]+BUTTON_ENLARGEMENT
    deselected_right = deselected_left+region_size[0]-BUTTON_ENLARGEMENT*2
    deselected_bottom = deselected_top+region_size[1]-BUTTON_ENLARGEMENT*2
    collide = False
    top = lerp(deselected_top, full_top, button_selections[id])
    bottom = lerp(deselected_bottom, full_bottom, button_selections[id])
    left = lerp(deselected_left, full_left, button_selections[id])
    right = lerp(deselected_right, full_right, button_selections[id])
    detection_rect = pygame.Rect(left, top, right-left, bottom-top)
    if detection_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        button_selections[id] = button_selections[id]*0.9+0.1
        collide = True
    else:
        button_selections[id] *= 0.9
    if ld_mode == 'light':
        draw_polygon_alpha(surface, (0, 0, 0, lerp(180, 230, button_selections[id])), [(left, top), (right, top), (right, bottom), (left, bottom)])
        text = font.render(txt, True, (255, 255, 255))
    elif ld_mode == 'dark':
        draw_polygon_alpha(surface, (255, 255, 255, lerp(128, 200, button_selections[id])), [(left, top), (right, top), (right, bottom), (left, bottom)])
        text = font.render(txt, True, (0, 0, 0))
    surface.blit(text, (full_left+region_size[0]/2-font.size(txt)[0]/2, full_top+region_size[1]/2-font.size(txt)[1]/2))
    if collide and mouse_down:
        return True
    return False

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [
                        (x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


splitage = 100
radius = math.sqrt(2*((0.3*splitage) ** 2))


bot1 = 0
bot2 = -1
def launcher(options):
    global bot1
    global bot2
    alpha = 0
    global ld_mode
    returning = 'quit'
    end_frame = 0
    pygame.init()
    font = pygame.font.SysFont('calibri', 50)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill('white')
    pygame.display.flip()
    x_size, y_size = screen.get_size()
    running = True
    squares = []
    for x in range(x_size//splitage+1):
        for y in range(y_size//splitage+1):
            squares.append({'x': x, 'y': y, 'middle_x': x*splitage+splitage//2, 'middle_y': y*splitage+splitage//2,
                           'offset_x': 0, 'offset_y': 0, 'rotation': 0, 'radius': radius, 'keyframes': []})
            squares[-1]['offset_x_want'] = squares[-1]['offset_x']
            squares[-1]['offset_y_want'] = squares[-1]['offset_y']
            squares[-1]['rotation_want'] = squares[-1]['rotation']
            squares[-1]['radius_want'] = squares[-1]['radius']
    last_effect = time.time()
    color_x, color_y = (x_size//2, y_size//2)
    color_vel_x, color_vel_y = (0, 0)
    mouse_was_down = True
    mouse_down = True
    while running:
        alpha *= 0.95
        mouse_was_down = mouse_down
        mouse_down = pygame.mouse.get_pressed(num_buttons=3)[0]
        bot1 = bot1%len(options)
        bot2 = bot2%len(options)
        random.seed(time.time())
        # color_vel_x += random.random()*2-1
        # color_vel_y += random.random()*2-1
        # color_x += color_vel_x
        # color_y += color_vel_y
        # if color_x < 0:
        #     color_vel_x = abs(color_vel_x)*0.9
        # elif color_x > x_size:
        #     color_vel_x = -abs(color_vel_x)*0.9
        # if color_y < 0:
        #     color_vel_y = abs(color_vel_y)*0.9
        # elif color_y > y_size:
        #     color_vel_y = -abs(color_vel_y)*0.9
        mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
        start_time = time.time()
        if last_effect+1.5 < time.time():
            random.seed(time.time())
            last_effect = time.time()
            effect = random.choice([1, 2, 3, 4])
            if effect == 1:
                dir1 = random.randint(0, 3)
                dir2 = random.randint(0, 3)
                rand1 = random.randint(-5, 10)
                rand2 = random.randint(-4, 3)*90+45
                rand3 = random.randint(-4, 3)*90+45
                for square in squares:
                    x = square['x']
                    y = square['y']
                    if dir1 == 0:
                        square['keyframes'].append(
                            {'time': start_time+x/20+y/20, 'offset_x': 0, 'offset_y': 0, 'radius': -rand1, 'rotation': rand2})
                    elif dir1 == 1:
                        square['keyframes'].append(
                            {'time': start_time+x_size/splitage/20-x/20+y/20, 'offset_x': 0, 'offset_y': 0, 'radius': -rand1, 'rotation': rand2})
                    elif dir1 == 2:
                        square['keyframes'].append(
                            {'time': start_time+y_size/splitage/20+x/20-y/20, 'offset_x': 0, 'offset_y': 0, 'radius': -rand1, 'rotation': rand2})
                    else:
                        square['keyframes'].append(
                            {'time': start_time+x_size/splitage/20+y_size/splitage/20-x/20-y/20, 'offset_x': 0, 'offset_y': 0, 'radius': -rand1, 'rotation': rand2})

                    if dir2 == 0:
                        square['keyframes'].append(
                            {'time': start_time+x/20+y/20+4, 'offset_x': 0, 'offset_y': 0, 'radius': rand1, 'rotation': rand3})
                    elif dir2 == 1:
                        square['keyframes'].append(
                            {'time': start_time+x_size/splitage/20-x/20+y/20+4, 'offset_x': 0, 'offset_y': 0, 'radius': rand1, 'rotation': rand3})
                    elif dir2 == 2:
                        square['keyframes'].append(
                            {'time': start_time+y_size/splitage/20+x/20-y/20+4, 'offset_x': 0, 'offset_y': 0, 'radius': rand1, 'rotation': rand3})
                    else:
                        square['keyframes'].append(
                            {'time': start_time+x_size/splitage/20+y_size/splitage/20-x/20-y/20+4, 'offset_x': 0, 'offset_y': 0, 'radius': rand1, 'rotation': rand3})
            elif effect == 2:
                x = random.randint(0, x_size//splitage)
                rand1 = random.randint(0, 1)*2-1
                rand2 = random.randint(0, 1)*2-1
                rand3 = random.randint(0, 1)*2-1
                rand4 = random.randint(-1, 1)
                rand5 = random.randint(-6, 6)*90
                rand6 = random.randint(-6, 6)*90
                for square in squares:
                    if square['x'] == x:
                        square['keyframes'].append({'time': (
                            start_time+square['y']*rand1/20), 'offset_x': 0, 'offset_y': 0, 'radius': rand4*7, 'rotation': rand5})
                        square['keyframes'].append({'time': (
                            start_time+square['y']*rand1/20+2), 'offset_x': 0, 'offset_y': 0, 'radius': rand4*-7, 'rotation': rand6})
            elif effect == 3:
                y = random.randint(0, y_size//splitage)
                rand1 = random.randint(0, 1)*2-1
                rand2 = random.randint(0, 1)*2-1
                rand3 = random.randint(0, 1)*2-1
                rand4 = random.randint(-1, 1)
                rand5 = random.randint(-6, 6)*90
                rand6 = random.randint(-6, 6)*90
                for square in squares:
                    if square['y'] == y:
                        square['keyframes'].append({'time': (
                            start_time+square['x']*rand1/20), 'offset_x': 0, 'offset_y': 0, 'radius': rand4*7, 'rotation': rand5})
                        square['keyframes'].append({'time': (
                            start_time+square['x']*rand1/20+2), 'offset_x': 0, 'offset_y': 0, 'radius': rand4*-7, 'rotation': rand6})
            elif effect == 4:
                for square in squares:
                    if random.random() > 0.8:
                        square['keyframes'].append({'time': start_time+random.random(
                        )*0.7, 'offset_x': 0, 'offset_y': 0, 'radius': 0, 'rotation': random.randint(-7, 7)*90})
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.quit()
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    #pygame.quit()
                    return 'quit'
                elif event.key == pygame.K_SPACE:
                    random.seed(time.time())
                    for square in squares:
                        if random.random() > 0.3:
                            if random.random() > 0.5:
                                square['keyframes'].append(
                                    {'time': start_time, 'offset_x': 0, 'offset_y': 0, 'radius': 0, 'rotation': random.randint(-4, 4)*90})
                            else:
                                rand1 = (random.random()-0.5)*4
                                square['keyframes'].append(
                                    {'time': start_time, 'offset_x': 0, 'offset_y': 0, 'radius': 0, 'rotation': random.randint(-4, 4)*90+rand1*45})
                                square['keyframes'].append(
                                    {'time': start_time+1, 'offset_x': 0, 'offset_y': 0, 'radius': 0, 'rotation': -rand1*45})
                    # for square in squares:
                    #    square['keyframes'] = []
                    #    square['offset_x_want'] = 0
                    #    square['offset_y_want'] = 0
                    #    square['rotation_want'] = 0
                    #    square['radius_want'] = radius
        if ld_mode == 'light':
            screen.fill((255, 255, 255))
        if ld_mode == 'dark':
            screen.fill((0, 0, 0))
        random.seed(0)
        for square in squares:
            for _ in range(len(square['keyframes'])):
                keyframe = square['keyframes'].pop(0)
                if keyframe['time'] > start_time:
                    square['keyframes'].append(keyframe)
                    continue
                square['offset_x_want'] += keyframe['offset_x']
                square['offset_y_want'] += keyframe['offset_y']
                square['rotation_want'] += keyframe['rotation']
                square['radius_want'] += keyframe['radius']
            square['offset_x'] = square['offset_x'] * \
                0.9+square['offset_x_want']*0.1
            square['offset_y'] = square['offset_y'] * \
                0.9+square['offset_y_want']*0.1
            square['rotation'] = square['rotation'] * \
                0.9+square['rotation_want']*0.1
            square['radius'] = square['radius']*0.9+square['radius_want']*0.1
            center_x = square['middle_x']+square['offset_x']
            center_y = square['middle_y']+square['offset_y']
            n = random.random()+(time.time()/10) % 1
            dist = math.sqrt((center_x-mouse_x)**2+(center_y-mouse_y)**2)
            saturation = min(max((-dist+400)/300, 0), 1)*0.6
            col = colorsys.hsv_to_rgb(n, saturation, 0.4+saturation)
            col = (col[0]*255, col[1]*255, col[2]*255, 128)
            points = [
                (math.cos(math.radians(45+square['rotation'])) * square['radius']+center_x, math.sin(
                    math.radians(45+square['rotation'])) * square['radius']+center_y),
                (math.cos(math.radians(135+square['rotation']))*square['radius']+center_x, math.sin(
                    math.radians(135+square['rotation']))*square['radius']+center_y),
                (math.cos(math.radians(225+square['rotation']))*square['radius']+center_x, math.sin(
                    math.radians(225+square['rotation']))*square['radius']+center_y),
                (math.cos(math.radians(315+square['rotation']))*square['radius']+center_x, math.sin(
                    math.radians(315+square['rotation']))*square['radius']+center_y),
            ]
            #pygame.draw.polygon(draw_surface, col, points)
            draw_polygon_alpha(screen, col, points)
        #draw_polygon_alpha(screen, (0, 0, 0, 128), [(10, 10), (310, 10), (310, 160), (10, 160)])
        keys = pygame.key.get_pressed()
        if draw_button(screen, (10, 10), (350, 170), 'play', pygame.mouse.get_pos(), 'a', mouse_down and not mouse_was_down, font):
            returning = (options[bot1], options[bot2], {'ld_mode': ld_mode})
            running = False
            #pygame.quit()
            return returning
        if draw_button(screen, (10, 180), (350, 170), 'x: '+options[bot1]['name'], pygame.mouse.get_pos(), 'b', mouse_down and not mouse_was_down, font):
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                bot1 -= 1
            else:
                bot1 += 1
        if draw_button(screen, (10, 350), (350, 170), 'o: '+options[bot2]['name'], pygame.mouse.get_pos(), 'c', mouse_down and not mouse_was_down, font):
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                bot2 -= 1
            else:
                bot2 += 1
        if ld_mode =='light':
            if draw_button(screen, (10, 520), (350, 170), 'dark mode', pygame.mouse.get_pos(), 'd', mouse_down and not mouse_was_down, font):
                ld_mode = 'dark'
                alpha = 255
        elif ld_mode =='dark':
            if draw_button(screen, (10, 520), (350, 170), 'light mode', pygame.mouse.get_pos(), 'd', mouse_down and not mouse_was_down, font):
                ld_mode = 'light'
                alpha = 255
        if draw_button(screen, (10, 690), (350, 170), 'exit', pygame.mouse.get_pos(), 'e', mouse_down and not mouse_was_down, font):
            running = False
            #pygame.quit()
            return 'quit'
        if alpha > 1:
            if ld_mode == 'light':
                draw_polygon_alpha(screen, (255, 255, 255, alpha), [(0, 0), (x_size, 0), (x_size, y_size), (0, y_size)])
            if ld_mode == 'dark':
                draw_polygon_alpha(screen, (0, 0, 0, alpha), [(0, 0), (x_size, 0), (x_size, y_size), (0, y_size)])
        time.sleep(max(0, end_frame-time.time()))
        pygame.display.flip()
        end_frame = time.time()+1/60
    #pygame.quit()
    return returning

    # return (random.choice(options), random.choice(options))


if __name__ == '__main__':
    launcher([{'name': 'human'}, {'name': 'bot1'},
             {'name': 'bot2'}, {'name': 'bot3'}])
