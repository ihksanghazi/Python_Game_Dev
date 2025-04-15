# Import library pygame dan modul pendukung
import pygame
from pygame.locals import *
import sys

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar permainan
frame_size_x = 900
frame_size_y = 500

# Set nilai FPS (frame per second)
FPS = 60  # Kecepatan game (60 frame per detik)

# Ukuran pesawat pemain
ship_width = 55     # Lebar pesawat (55 pixel)
ship_height = 40    # Tinggi pesawat (40 pixel)

# Jumlah maksimal peluru yang bisa ditembak
max_num_of_bullet = 5

# Membuat jendela permainan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menetapkan judul pada jendela game
pygame.display.set_caption("Space Shooter")

# Definisi warna dalam format RGB
white = (255, 255, 255)
black = (0, 0, 0)
green = (110, 194, 54)  # Warna peluru hijau
blue = (23, 54, 235)    # Warna peluru biru

# Load dan atur gambar latar belakang
background = pygame.transform.scale(
    pygame.image.load('gallery/sprites/background.png'),
    (frame_size_x, frame_size_y)
).convert()

# Load dan atur logo permainan
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
space_shooter_logo = pygame.transform.scale(space_shooter_logo, (300, 150))

# Load dan rotasi pesawat hijau (menghadap kanan)
green_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/green_ship.png').convert_alpha(), 270)

# Load dan rotasi pesawat biru (menghadap kiri)
blue_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/blue_ship.png').convert_alpha(), 90)

# Skalakan gambar pesawat agar sesuai ukuran
green_ship = pygame.transform.scale(green_ship_img, (ship_width, ship_height)).convert_alpha()
blue_ship = pygame.transform.scale(blue_ship_img, (ship_width, ship_height)).convert_alpha()

# Load efek suara untuk peluru
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')

# Fungsi utama permainan
def main():
    clock = pygame.time.Clock()  # Buat clock untuk mengatur kecepatan game
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)  # Posisi awal pesawat hijau
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)   # Posisi awal pesawat biru
    green_bullets = []  # Daftar peluru yang ditembak oleh pemain hijau
    blue_bullets = []   # Daftar peluru yang ditembak oleh pemain biru

    while True:
        clock.tick(FPS)  # Batasi loop per detik agar tetap konsisten

        # Mengecek event dari keyboard/mouse
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()  # Keluar dari pygame
                sys.exit()     # Keluar dari program

            # Kontrol untuk menembak peluru
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < max_num_of_bullet:
                    bullet_fire_sound.play()  # Suara tembakan pesawat hijau
                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_num_of_bullet:
                    bullet_fire_sound.play()  # Suara tembakan pesawat biru

        # Gambar latar belakang dan pesawat
        window_screen.blit(background, (0, 0))
        window_screen.blit(green_ship, (green_rect.x, green_rect.y))
        window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))
        pygame.display.update()  # Update tampilan layar

# Fungsi tampilan awal sebelum game dimulai
def welcome_screen():
    while True:
        # Tampilkan latar belakang dan logo
        window_screen.blit(background, (0, 0))
        window_screen.blit(space_shooter_logo, (frame_size_x//3, 40))

        # Tampilkan teks "Press Any Key"
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (
            frame_size_x // 2 - welcome_text.get_width() // 2,
            frame_size_y // 2 - welcome_text.get_height() // 2
        ))

        # Cek input keyboard
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()  # Pindah ke game utama jika ada tombol ditekan

        pygame.display.update()  # Update tampilan layar

# Jalankan welcome screen sebagai titik awal
welcome_screen()
