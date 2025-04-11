# Mengimpor modul pygame untuk membuat game
import pygame

# Mengimpor modul sys untuk mengakses fungsi sistem (seperti keluar dari program)
import sys

# Mengimpor modul random untuk menghasilkan angka acak (digunakan untuk posisi apel)
import random

# Menginisialisasi pygame dan memeriksa error
check_errors = pygame.init()

# Menentukan ukuran jendela game (lebar)
frame_size_x = 720

# Menentukan ukuran jendela game (tinggi)
frame_size_y = 480

# Memberi judul pada jendela game
pygame.display.set_caption('Snake Game')

# Membuat jendela game dengan ukuran yang telah ditentukan
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menentukan arah awal pergerakan ular
direction = 'RIGHT'

# Variabel untuk menyimpan perubahan arah
change_to = direction

# Menentukan posisi awal kepala ular
snake_pos = [100, 50]

# Menentukan posisi tubuh ular (3 blok: kepala + 2 bagian tubuh)
snake_body = [[100, 50], [90, 50], [80, 50]]

# Menghasilkan posisi acak untuk apel di grid 10x10
apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]

# Menandakan bahwa apel tersedia di layar
apple_spawn = True

# Mendefinisikan warna putih (digunakan untuk background)
white = pygame.Color(255,255,255)

# Mendefinisikan warna hitam (tidak digunakan saat ini)
black = pygame.Color(0,0,0)

# Mendefinisikan warna merah (digunakan untuk apel)
red = pygame.Color(255,0,0)

# Mendefinisikan warna hijau (digunakan untuk ular)
green = pygame.Color(0,255,0)

# Mendefinisikan warna biru (tidak digunakan saat ini)
blue = pygame.Color(0,0,255)

# Memulai loop utama game
while True:
    # Mengecek semua event (input dari pengguna)
    for event in pygame.event.get():
        # Jika event adalah keluar (misal klik tombol X)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Jika event adalah menekan tombol keyboard
        elif event.type == pygame.KEYDOWN:
            # Jika tombol panah atas ditekan, ubah arah ke atas
            if event.key == pygame.K_UP :
                change_to = 'UP'
            # Jika tombol panah bawah ditekan, ubah arah ke bawah
            if event.key == pygame.K_DOWN :
                change_to = 'DOWN'
            # Jika tombol panah kiri ditekan, ubah arah ke kiri
            if event.key == pygame.K_LEFT :
                change_to = 'LEFT'
            # Jika tombol panah kanan ditekan, ubah arah ke kanan
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            # Jika tombol Escape ditekan, keluar dari game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    # Mengisi latar belakang jendela dengan warna putih
    game_window.fill(white)

    # Menampilkan perubahan arah di konsol (debug)
    print(change_to)

    # Menambahkan posisi kepala ular ke tubuh ular (gerakan)
    snake_body.insert(0, list(snake_pos))

    # Menggambar setiap bagian tubuh ular di layar
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Jika apel tidak ada di layar, buat posisi apel baru
    if not apple_spawn:
        apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]

    # Menandai bahwa apel telah di-spawn
    apple_spawn = True

    # Menggambar apel di layar
    pygame.draw.rect(game_window, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10)) 

    # Memperbarui layar game
    pygame.display.update()
