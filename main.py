import random
import sys
import pygame
from pygame.locals import *

FPS = 32
frame_size_x = 289
frame_size_y = 511
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
game_sprites = {}
game_sounds = {}
player = 'gallery/sprites/astro.png'
background = 'gallery/sprites/bg.jpg'
base = 'gallery/sprites/base.jpg'
pipe = 'gallery/sprites/pipe.png'
ground_by = frame_size_y * 0.8
pygame.init()
fps_controller = pygame.time.Clock()
pygame.display.set_caption('Astro Man')

def main_game():
    player_x = int(frame_size_x/5)
    player_y = int(frame_size_x/2)
    base_x = 0
    player_jump = False
    player_jump_acc = -8
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1
    pipe_vel_x = -4
    new_pipe_1 = get_random_pipe()
    new_pipe_2 = get_random_pipe()
    upper_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[0]['y']},
        {'x': frame_size_x + 200 + (frame_size_x / 2),'y': new_pipe_2[0]['y']},
    ]

    lower_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[1]['y']},
        {'x': frame_size_x + 200 + (frame_size_x / 2),'y': new_pipe_2[1]['y']},
    ]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_jump_acc
                    player_jump = True
                    game_sounds['jump'].play()
        if player_vel_y < player_max_vel_y and not player_jump:
            player_vel_y += player_acc_y
        if player_jump:
            player_jump = False
        player_height = game_sprites['player'].get_height()
        player_y = player_y + min(player_vel_y, ground_by - player_y - player_height)

        window_screen.blit(game_sprites['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            window_screen.blit(game_sprites['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            window_screen.blit(game_sprites['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))
        for upper_pipe , lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x
        if 0<upper_pipes[0]['x']<5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])
        if upper_pipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
            
        pygame.display.update()
        fps_controller.tick(FPS)

def welcome_screen():
    player_x = int(frame_size_x/5)
    player_y = int((frame_size_y - game_sprites['player'].get_height())/2)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                window_screen.blit(game_sprites['background'], (0, 0))
                window_screen.blit(game_sprites['player'], (player_x, player_y))
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                welcome_rect = welcome_surface.get_rect()
                welcome_rect.midtop = (frame_size_x/2, 32)
                window_screen.blit(welcome_surface, welcome_rect)
                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)

def get_random_pipe():
    pipe_height = game_sprites['pipe'][0].get_height() #get the height of the pipe sprite
    offset = frame_size_y/3
    y2 = offset + random.randrange(0, int(frame_size_y - game_sprites['base'].get_height()- 1.2*offset))
    y1 = pipe_height - y2 + offset
    pipe_x = frame_size_x + 10
    
    pipe = [
        {'x': pipe_x, 'y': -y1}, #upper Pipe
        {'x': pipe_x, 'y': y2}  #lower Pipe
    ]
    return pipe

game_sprites['base'] =pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()
game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),pygame.image.load(pipe).convert_alpha())
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/jump.wav')

while True:
    welcome_screen()
    main_game()