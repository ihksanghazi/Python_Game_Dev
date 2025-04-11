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
        window_screen.blit(game_sprites['background'], (0, 0))
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))
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

game_sprites['base'] =pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/jump.wav')

while True:
    welcome_screen()
    main_game()