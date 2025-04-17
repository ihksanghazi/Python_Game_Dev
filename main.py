# Mengimpor modul pygame dan fungsi randint dari random
import pygame
from random import randint

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar permainan
frame_size_x = 800 
frame_size_y = 400 

# Membuat window dengan ukuran yang telah ditentukan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Memberi judul pada jendela game
pygame.display.set_caption("Running Game")

# Untuk mengatur kecepatan frame per detik
clock = pygame.time.Clock()
FPS = 60

# Font yang digunakan untuk menampilkan teks di layar
font = pygame.font.Font("gallery/fonts/Pixeltype.ttf", 32)

# Waktu mulai permainan
start_time = 0

# Status game apakah sedang berjalan atau tidak
game_active = False

# Pemain memiliki 2 gambar untuk animasi jalan
player_walk_1 = pygame.image.load("gallery/sprites/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("gallery/sprites/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player = player_walk[player_index]

# Gambar ketika pemain melompat
player_jump = pygame.image.load("gallery/sprites/player/Player3.png").convert_alpha()

# Posisi awal pemain
player_rect = player.get_rect(midbottom=(80, 300))

# Gravitasi awal
player_gravity = 0

# Skor dan skor tertinggi
score = 0
high_score = 0

# Efek suara lompatan dan suara ketika game over
jump_sound = pygame.mixer.Sound('gallery/audio/jump.mp3')
game_over_sound = pygame.mixer.Sound('gallery/audio/death.mp3')

# Backsound game diputar berulang kali
back_sound = pygame.mixer.Sound('gallery/audio/backsound.mp3')
back_sound.play(loops=-1)
back_sound.set_volume(0.5)

# Gambar background dan tanah
skybox = pygame.image.load('gallery/sprites/Sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

# Gambar musuh pertama (dua frame untuk animasi)
enemy_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy.png").convert_alpha()
enemy_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy_2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

# Gambar musuh kedua (dua frame untuk animasi)
enemy2_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

# List yang menampung semua obstacle (musuh) di layar
obstacle_rect_list = []

# Timer untuk spawn obstacle secara berkala
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Timer untuk animasi musuh
enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 200)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)

# Fungsi untuk menampilkan tampilan saat game aktif
def active_game():
    global player_gravity, obstacle_rect_list, game_active, score 
    window_screen.blit(skybox, (0,0))  # Gambar background
    window_screen.blit(ground, (0, 320))  # Gambar tanah
    score = display_score()  # Update skor

    # Logika gravitasi pemain
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 320:
        player_rect.bottom = 320

    # Animasi pemain
    player_animation()
    window_screen.blit(player, player_rect)  # Gambar pemain

    # Gerakkan dan tampilkan obstacle
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    # Cek apakah ada tabrakan
    game_active = collision(player_rect, obstacle_rect_list)

# Fungsi untuk menampilkan tampilan saat game belum dimulai atau game over
def inactive_game():
    global score, high_score
    window_screen.fill((64, 64, 64))  # Latar belakang abu-abu
    window_screen.blit(player, (frame_size_x // 2 - 30 , frame_size_y//2 - 30 ))  # Tampilkan pemain

    # Tampilkan nama game dan pesan
    game_name = font.render("Running Game", False,"white")
    game_name = pygame.transform.scale2x(game_name)
    game_name_rect = game_name.get_rect(center=(400,80))
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))
    score_message = font.render("Your score : {}".format(score), False, "white")
    score_message_rect = score_message.get_rect(center = (400, 320))
    high_score_message = font.render("Your high score : {}". format(high_score), False, "white")
    high_score_message_rect = high_score_message.get_rect(center = (400, 350))

    # Jika belum bermain, tampilkan pesan untuk memulai
    if score == 0:
        window_screen.blit(game_message, game_message_rect)
    else:
        # Tampilkan skor dan high score setelah game over
        window_screen.blit(score_message, score_message_rect)
        window_screen.blit(high_score_message, high_score_message_rect)

    # Jalankan animasi pemain dan reset obstacle
    player_animation()
    obstacle_rect_list.clear()

# Fungsi untuk menghitung dan menampilkan skor
def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    window_screen.blit(score, score_rect)
    return current_time

# Fungsi untuk menggerakkan dan menggambar obstacle
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5  # Gerakkan ke kiri

            # Gambar musuh sesuai posisi
            if obstacle_rect.bottom == 320:
                window_screen.blit(enemy, obstacle_rect)
            else:
                window_screen.blit(enemy2, obstacle_rect)

        # Filter obstacle yang masih di dalam layar
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

# Fungsi untuk mendeteksi tabrakan antara pemain dan obstacle
def collision(player, obstacles):
    global high_score
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                game_over_sound.play()
                if score > high_score:
                    high_score = score
                return False  # Game berhenti jika tabrakan
    return True  # Lanjutkan game jika tidak ada tabrakan

# Fungsi untuk spawn dan animasi musuh
def spawn_enemy():
    global enemy_frame_index, enemy2_frame_index, enemy, enemy2
    if event.type == obstacle_timer:
        if randint(0, 2):
            print("enemy has been spawned")
            obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900, 1100), 320)))
        else:
            obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900, 1100), 210)))

    # Animasi musuh pertama
    if event.type == enemy_animation_timer:
        enemy_frame_index = 1 - enemy_frame_index
        enemy = enemy_frames[enemy_frame_index]

    # Animasi musuh kedua
    if event.type == enemy2_animation_timer:
        enemy2_frame_index = 1 - enemy2_frame_index
        enemy2 = enemy2_frames[enemy2_frame_index]

# Fungsi untuk animasi pemain (jalan atau lompat)
def player_animation():
    global player_index, player
    player_index += 0.1
    if player_rect.bottom < 320:
        player = player_jump  # Jika di udara, tampilkan gambar lompat
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

# Loop utama game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            spawn_enemy()  # Jalankan spawn musuh dan animasi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 320:
                    jump_sound.play()
                    player_gravity = -20  # Melompat
            print("Game Active")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/600)

    # Update tampilan game berdasarkan status aktif
    if game_active:
        active_game()
    else:
        inactive_game()

    # Refresh layar dan atur FPS
    pygame.display.update()
    clock.tick(FPS)
