# Import pustaka pygame untuk membuat game
import pygame
# Import semua modul dari pygame.locals (seperti K_LEFT, QUIT, dll)
from pygame.locals import *
# Import modul sys untuk keluar dari game dengan sys.exit()
import sys

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar game (lebar x tinggi)
frame_size_x = 900
frame_size_y = 500

# Frame Per Second (jumlah frame per detik)
FPS = 60
# Kecepatan gerak pesawat
velocity = 5
# Event khusus ketika pemain terkena peluru
green_hit = pygame.USEREVENT+1
blue_hit = pygame.USEREVENT+2
# Ukuran pesawat
ship_width = 55
ship_height = 40
# Batas maksimal peluru yang bisa ditembak sekaligus
max_num_of_bullet = 5
# Kecepatan peluru
bullet_velocity = 7

# Membuat window game dengan ukuran tertentu
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menampilkan judul di jendela game
pygame.display.set_caption("Space Shooter")

# Warna dalam format RGB
white = (255, 255, 255)
black = (0, 0, 0)
green = (110, 194, 54)
blue = (23, 54, 235)

# Font untuk menampilkan health
health_font = pygame.font.SysFont('Impact', 40)
# Font untuk menampilkan pemenang
winner_font = pygame.font.SysFont('Impact', 100)

# Membuat garis batas tengah di layar (untuk membagi wilayah)
border = pygame.Rect((frame_size_x//2)-5,0,10,frame_size_y)

# Load dan sesuaikan background
background = pygame.transform.scale(pygame.image.load('gallery/sprites/background.png'),(frame_size_x, frame_size_y)).convert()
# Load logo game
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
space_shooter_logo = pygame.transform.scale(space_shooter_logo, (300, 150))
# Load dan rotasi gambar pesawat hijau
green_ship_img = pygame.transform.rotate(pygame.image.load('gallery/sprites/shipGreen.png').convert_alpha(), 270)
# Load dan rotasi gambar pesawat biru
blue_ship_img = pygame.transform.rotate(pygame.image.load('gallery/sprites/shipBlue.png').convert_alpha(), 90)
# Resize gambar pesawat hijau dan biru ke ukuran yang telah ditentukan
green_ship = pygame.transform.scale(green_ship_img,(ship_width,ship_height)).convert_alpha()
blue_ship = pygame.transform.scale(blue_ship_img,(ship_width,ship_height)).convert_alpha()

# Load efek suara tembakan dan terkena peluru
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')
bullet_hit_sound = pygame.mixer.Sound('gallery/audio/sfx_hit.ogg')
game_end_sound = pygame.mixer.Sound('gallery/audio/sfx_game_over.ogg')

# Fungsi untuk menangani pergerakan pesawat biru (player 2)
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - velocity > border.x + border.width - 5:
        blue.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and blue.x - velocity + blue.width < frame_size_x - 5:
        blue.x += velocity
    if keys_pressed[pygame.K_UP] and blue.y - velocity > 0:
        blue.y -= velocity
    if keys_pressed[pygame.K_DOWN] and blue.y - velocity + blue.height < frame_size_y - 5:
        blue.y += velocity

# Fungsi untuk menangani pergerakan pesawat hijau (player 1)
def green_movement_handler(key_pressed, green):
    if key_pressed[pygame.K_w] and green.y - velocity > 0:
        green.y -= velocity
    if key_pressed[pygame.K_a] and green.x - velocity > 5:
        green.x -= velocity
    if key_pressed[pygame.K_s] and green.y - velocity + green.height < frame_size_y - 5:
        green.y += velocity
    if key_pressed[pygame.K_d] and green.x - velocity +green.width < border.x -5:
        green.x += velocity

# Fungsi untuk menangani logika peluru: gerak, tabrakan, dan penghapusan
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            green_bullets.remove(bullet)
        elif bullet.x > frame_size_x:
            green_bullets.remove(bullet)
    
    for bullet in blue_bullets:
        bullet.x -= bullet_velocity
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(green_hit))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

# Fungsi untuk menggambar ulang semua elemen di layar
def draw_window(green_rect, blue_rect, green_bullets, blue_bullets, green_health, blue_health):
    window_screen.blit(background, (0, 0))
    pygame.draw.rect(window_screen, black, border)

    window_screen.blit(green_ship, (green_rect.x, green_rect.y))
    window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))

    green_health_text = health_font.render("Health: " + str(green_health), 1, white)
    blue_health_text = health_font.render("Health: " + str(blue_health), 1, white)
    window_screen.blit(blue_health_text, (720, 10))
    window_screen.blit(green_health_text, (10, 10))

    for bullet in green_bullets:
        pygame.draw.rect(window_screen, green, bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(window_screen, blue, bullet)

    pygame.display.update()

# Fungsi untuk menampilkan layar kemenangan dan suara akhir
def draw_winner(text):
    winner_text = winner_font.render(text, 1, white)
    window_screen.blit(winner_text, (frame_size_x // 2 - winner_text.get_width() / 2, frame_size_y // 2 - winner_text.get_height() / 2))
    pygame.display.update()
    game_end_sound.play()
    pygame.time.delay(5000)

# Fungsi utama untuk menjalankan game
def main():
    clock = pygame.time.Clock()
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)
    green_bullets = []
    blue_bullets = []
    green_health = 10
    blue_health = 10

    while True:
        clock.tick(FPS)  # Membatasi kecepatan game
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Tembakan peluru
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(green_rect.x + green_rect.width, green_rect.y + green_rect.height // 2, 10, 5)
                    green_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(blue_rect.x, blue_rect.y + blue_rect.height // 2, 10, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()

            # Terdeteksi terkena peluru
            if event.type == green_hit:
                green_health -= 1
                bullet_hit_sound.play()
            if event.type == blue_hit:
                blue_health -= 1
                bullet_hit_sound.play()

        # Cek pemenang
        winner_text = ""
        if green_health <= 0:
            winner_text = "Blue Player Wins!"
        if blue_health <= 0:
            winner_text = "Green Player Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        # Deteksi input gerakan
        keys_pressed = pygame.key.get_pressed()
        green_movement_handler(keys_pressed, green_rect)
        blue_movement_handler(keys_pressed, blue_rect)

        # Update peluru
        handle_bullets(green_bullets, blue_bullets, green_rect, blue_rect)

        # Gambar ulang layar
        draw_window(green_rect, blue_rect, green_bullets, blue_bullets, green_health, blue_health)

# Fungsi untuk menampilkan layar sambutan (welcome screen)
def welcome_screen():
    while True:
        window_screen.blit(background, (0, 0))
        window_screen.blit(space_shooter_logo, (frame_size_x // 3, 40))
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (frame_size_x // 2 - welcome_text.get_width() // 2, frame_size_y // 2 - welcome_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()
        pygame.display.update()

# Jalankan layar awal
welcome_screen()
