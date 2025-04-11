# Mengimpor modul pygame untuk pembuatan game
import pygame

# Mengimpor sys untuk fungsi sistem seperti keluar dari program
import sys

# Mengimpor random untuk membuat posisi apel secara acak
import random

# Mengimpor time untuk fungsi delay saat game over
import time

# Inisialisasi pygame dan mengecek error saat inisialisasi
check_errors = pygame.init()

# Ukuran lebar jendela game
frame_size_x = 720

# Ukuran tinggi jendela game
frame_size_y = 480

# Menentukan judul jendela game
pygame.display.set_caption('Snake Game')

# Membuat jendela game dengan ukuran yang ditentukan
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Objek untuk mengatur kecepatan frame per detik (FPS)
fps_controller = pygame.time.Clock()

# Arah awal ular bergerak
direction = 'RIGHT'

# Variabel untuk menyimpan perubahan arah input pengguna
change_to = direction

# Menyimpan skor pemain
score = 0

# Posisi awal kepala ular
snake_pos = [100, 50]

# Posisi awal tubuh ular (3 bagian: kepala dan 2 ekor)
snake_body = [[100, 50], [90, 50], [80, 50]]

# Posisi awal apel ditentukan secara acak
apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]

# Menandakan apakah apel tersedia di layar
apple_spawn = True

# Warna-warna yang digunakan dalam game
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

# Fungsi untuk menampilkan layar game over dan keluar dari game
def game_over():
    # Membuat font untuk teks game over
    my_font = pygame.font.SysFont('Arial', 90)
    # Membuat teks "YOU DIED" berwarna merah
    game_over_surface = my_font.render('YOU DIED', True, red)
    # Mendapatkan posisi dari teks untuk ditampilkan
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (360, 120)
    # Mengisi layar dengan warna hitam dan menampilkan teks
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    # Menunggu 3 detik sebelum keluar
    time.sleep(3)
    # Keluar dari game
    pygame.quit()
    sys.exit()

# Loop utama game
while True:
    # Menangani semua event input dari pengguna
    for event in pygame.event.get():
        # Jika tombol close (X) ditekan
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Jika tombol keyboard ditekan
        elif event.type == pygame.KEYDOWN:
            # Deteksi arah berdasarkan input pengguna
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            # Jika ESC ditekan, keluar dari game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    # Mencegah ular berbelok langsung ke arah berlawanan
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Memperbarui posisi kepala ular berdasarkan arah
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Mengisi layar dengan warna putih
    game_window.fill(white)

    # Debug: mencetak arah terbaru di konsol
    print(change_to)

    # Menambahkan posisi baru kepala ular ke list tubuh ular
    snake_body.insert(0, list(snake_pos))

    # Mengecek apakah kepala ular berada di posisi apel
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        # Jika iya, tambahkan skor dan tandai apel perlu digenerate ulang
        score += 1
        apple_spawn = False
    else:
        # Jika tidak, hapus bagian ekor agar ular tetap panjangnya sama
        snake_body.pop()

    # Menggambar seluruh tubuh ular di layar
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Jika apel belum muncul, buat posisi baru secara acak
    if not apple_spawn:
        apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    # Tandai bahwa apel sudah muncul
    apple_spawn = True

    # Menggambar apel di layar
    pygame.draw.rect(game_window, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))

    # Jika kepala ular melewati batas kiri/kanan layar
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    # Jika kepala ular melewati batas atas/bawah layar
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()

    # Mengecek apakah kepala ular bertabrakan dengan tubuhnya sendiri
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Membuat font dan teks untuk menampilkan skor
    score_font = pygame.font.SysFont('Arial', 20)
    score_surface = score_font.render('Score : ' + str(score), True, black)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (72, 15)
    # Menampilkan skor di layar
    game_window.blit(score_surface, score_rect)

    # Memperbarui tampilan jendela
    pygame.display.update()

    # Mengatur kecepatan game (10 frame per detik)
    fps_controller.tick(10)
