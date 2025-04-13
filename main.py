# Mengimpor pustaka-pustaka yang diperlukan
import random
import sys
import pygame
from pygame.locals import *

# Menentukan jumlah frame per detik (FPS)
FPS = 32

# Ukuran layar permainan
frame_size_x = 289
frame_size_y = 511

# Membuat window tampilan permainan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Dictionary untuk menyimpan gambar sprite dan suara
game_sprites = {}
game_sounds = {}

# Lokasi file gambar yang digunakan
player = 'gallery/sprites/astro.png'
background = 'gallery/sprites/bg.jpg'
base = 'gallery/sprites/base.jpg'
pipe = 'gallery/sprites/pipe.png'

# Posisi dasar tanah (base)
ground_by = frame_size_y * 0.8

# Menginisialisasi Pygame dan pengatur FPS
pygame.init()
fps_controller = pygame.time.Clock()
pygame.display.set_caption('Astro Man')

# Fungsi utama game saat gameplay dimulai
def main_game():
    # Posisi awal karakter
    player_x = int(frame_size_x / 5)
    player_y = int(frame_size_x / 2)
    base_x = 0

    # Variabel untuk mengatur lompatan
    player_jump = False
    player_jump_acc = -8  # percepatan lompatan ke atas

    while True:
        # Menangani event (tombol, keluar)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_jump_acc
                    player_jump = True
                    game_sounds['jump'].play()  # mainkan suara lompatan

        # Menampilkan latar belakang, karakter, dan base
        window_screen.blit(game_sprites['background'], (0, 0))
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))

        # Update tampilan dan atur kecepatan FPS
        pygame.display.update()
        fps_controller.tick(FPS)

# Fungsi tampilan awal (welcome screen) sebelum game dimulai
def welcome_screen():
    # Menentukan posisi awal karakter dan base
    player_x = int(frame_size_x / 5)
    player_y = int((frame_size_y - game_sprites['player'].get_height()) / 2)
    base_x = 0

    while True:
        # Menangani event saat di welcome screen
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return  # Mulai game jika tombol ditekan
            else:
                # Tampilkan latar belakang, karakter, judul, dan base
                window_screen.blit(game_sprites['background'], (0, 0))
                window_screen.blit(game_sprites['player'], (player_x, player_y))
                
                # Membuat dan menampilkan teks judul
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                welcome_rect = welcome_surface.get_rect()
                welcome_rect.midtop = (frame_size_x / 2, 32)
                window_screen.blit(welcome_surface, welcome_rect)

                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)

# Memuat gambar-gambar ke dalam dictionary game_sprites
game_sprites['base'] = pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()

# Memuat suara ke dalam dictionary game_sounds
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/jump.wav')

# Loop utama: tampilkan welcome screen, lalu masuk ke gameplay
while True:
    welcome_screen()
    main_game()
