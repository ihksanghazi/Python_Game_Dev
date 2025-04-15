# Import pustaka pygame dan modul tambahan
import pygame
from pygame.locals import *
import sys

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar game
frame_size_x = 900
frame_size_y = 500

# Frame rate per second dan kecepatan objek
FPS = 60             # Kecepatan game (60 frame per detik)
velocity = 5         # Kecepatan pergerakan pesawat

# Ukuran pesawat
ship_width = 55      # Lebar pesawat
ship_height = 40     # Tinggi pesawat

# Batas jumlah peluru yang bisa aktif di layar
max_num_of_bullet = 5

# Kecepatan peluru
bullet_velocity = 7

# Membuat jendela game
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menetapkan judul jendela
pygame.display.set_caption("Space Shooter")

# Warna yang digunakan (dalam RGB)
white = (255, 255, 255)
black = (0, 0, 0)
green = (110, 194, 54)
blue = (23, 54, 235)

# Membuat batas tengah sebagai pemisah wilayah dua pemain
border = pygame.Rect((frame_size_x//2)-5, 0, 10, frame_size_y)

# Memuat gambar latar belakang
background = pygame.transform.scale(
    pygame.image.load('gallery/sprites/background.png'),
    (frame_size_x, frame_size_y)
).convert()

# Memuat logo game dan menyesuaikan ukurannya
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
space_shooter_logo = pygame.transform.scale(space_shooter_logo, (300, 150))

# Memuat dan merotasi pesawat sesuai arah masing-masing pemain
green_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipGreen.png').convert_alpha(), 270)
blue_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipBlue.png').convert_alpha(), 90)

# Mengatur ukuran pesawat setelah dirotasi
green_ship = pygame.transform.scale(green_ship_img, (ship_width, ship_height)).convert_alpha()
blue_ship = pygame.transform.scale(blue_ship_img, (ship_width, ship_height)).convert_alpha()

# Memuat suara tembakan
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')

# Fungsi untuk mengatur pergerakan pesawat biru
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - velocity > border.x + border.width - 5:
        blue.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and blue.x + blue.width + velocity < frame_size_x - 5:
        blue.x += velocity
    if keys_pressed[pygame.K_UP] and blue.y - velocity > 0:
        blue.y -= velocity
    if keys_pressed[pygame.K_DOWN] and blue.y + blue.height + velocity < frame_size_y - 5:
        blue.y += velocity

# Fungsi untuk mengatur pergerakan pesawat hijau
def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_w] and green.y - velocity > 0:
        green.y -= velocity
    if keys_pressed[pygame.K_a] and green.x - velocity > 5:
        green.x -= velocity
    if keys_pressed[pygame.K_s] and green.y + green.height + velocity < frame_size_y - 5:
        green.y += velocity
    if keys_pressed[pygame.K_d] and green.x + green.width + velocity < border.x - 5:
        green.x += velocity

# Fungsi untuk menangani pergerakan dan tabrakan peluru
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += bullet_velocity  # Gerak ke kanan
        if blue.colliderect(bullet):
            green_bullets.remove(bullet)  # Jika terkena biru
        elif bullet.x > frame_size_x:
            green_bullets.remove(bullet)  # Keluar layar

    for bullet in blue_bullets:
        bullet.x -= bullet_velocity  # Gerak ke kiri
        if green.colliderect(bullet):
            blue_bullets.remove(bullet)  # Jika terkena hijau
        elif bullet.x < 0:
            blue_bullets.remove(bullet)  # Keluar layar

# Fungsi untuk menggambar ulang semua elemen di layar
def draw_window(green_rect, blue_rect, green_bullets, blue_bullets):
    window_screen.blit(background, (0, 0))  # Gambar background
    pygame.draw.rect(window_screen, black, border)  # Gambar garis tengah
    window_screen.blit(green_ship, (green_rect.x, green_rect.y))  # Gambar pesawat hijau
    window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))     # Gambar pesawat biru

    # Gambar peluru hijau
    for bullet in green_bullets:
        pygame.draw.rect(window_screen, green, bullet)

    # Gambar peluru biru
    for bullet in blue_bullets:
        pygame.draw.rect(window_screen, blue, bullet)

    pygame.display.update()  # Update tampilan layar

# Fungsi utama yang menjalankan logika game
def main():
    clock = pygame.time.Clock()
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)   # Posisi awal hijau
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)    # Posisi awal biru
    green_bullets = []  # List peluru hijau
    blue_bullets = []   # List peluru biru

    while True:
        clock.tick(FPS)  # Mengatur kecepatan loop

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Menembak peluru dengan CTRL
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < max_num_of_bullet:
                    # Membuat peluru dari posisi pesawat hijau
                    bullet = pygame.Rect(
                        green_rect.x + green_rect.width,
                        green_rect.y + green_rect.height // 2,
                        10, 5
                    )
                    green_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_num_of_bullet:
                    # Membuat peluru dari posisi pesawat biru
                    bullet = pygame.Rect(
                        blue_rect.x,
                        blue_rect.y + blue_rect.height // 2,
                        10, 5
                    )
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()

        # Ambil status tombol yang ditekan
        keys_pressed = pygame.key.get_pressed()

        # Panggil fungsi kontrol pergerakan
        green_movement_handler(keys_pressed, green_rect)
        blue_movement_handler(keys_pressed, blue_rect)

        # Panggil fungsi peluru
        handle_bullets(green_bullets, blue_bullets, green_rect, blue_rect)

        # Gambar semua elemen
        draw_window(green_rect, blue_rect, green_bullets, blue_bullets)

# Fungsi tampilan awal sebelum game dimulai
def welcome_screen():
    while True:
        window_screen.blit(background, (0, 0))  # Gambar background
        window_screen.blit(space_shooter_logo, (frame_size_x // 3, 40))  # Gambar logo

        # Buat teks sambutan
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)

        # Tampilkan teks di tengah layar
        window_screen.blit(
            welcome_text,
            (frame_size_x // 2 - welcome_text.get_width() // 2,
             frame_size_y // 2 - welcome_text.get_height() // 2)
        )

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()  # Masuk ke permainan utama

        pygame.display.update()  # Update layar

# Jalankan tampilan awal sebagai awal program
welcome_screen()
