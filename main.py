import pygame
from random import randint  # Untuk memilih angka acak, digunakan saat spawn musuh

# Inisialisasi pygame
pygame.init()

# Ukuran layar
frame_size_x = 800 
frame_size_y = 400 

# Membuat window untuk game
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption("Running Game")

# Mengatur FPS game
clock = pygame.time.Clock()
FPS = 60

# Mengatur font untuk teks
font = pygame.font.Font("gallery/fonts/Pixeltype.ttf", 32)

# Variabel awal
start_time = 0
game_active = False  # Game belum aktif saat dijalankan

# Load gambar animasi pemain (berjalan)
player_walk_1 = pygame.image.load("gallery/sprites/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("gallery/sprites/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player = player_walk[player_index]

# Gambar pemain saat melompat
player_jump = pygame.image.load("gallery/sprites/player/Player3.png").convert_alpha()

# Posisi awal pemain
player_rect = player.get_rect(midbottom=(80, 300))
player_gravity = 0  # Untuk efek gravitasi saat melompat

# Load suara lompat
jump_sound = pygame.mixer.Sound('gallery/audio/jump.mp3')

# Load dan mainkan backsound
back_sound = pygame.mixer.Sound('gallery/audio/backsound.mp3')
back_sound.play(loops=-1)  # Loop terus menerus
back_sound.set_volume(0.5)  # Set volume backsound

# Load background dan tanah
skybox = pygame.image.load('gallery/sprites/Sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

# Load musuh 1 (jalan di tanah)
enemy_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy.png").convert_alpha()
enemy_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy_2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

# Load musuh 2 (terbang di udara)
enemy2_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

# List untuk menyimpan posisi obstacle (musuh)
obstacle_rect_list = []

# Timer untuk spawn obstacle tiap 1000ms (1 detik)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Timer untuk animasi musuh
enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 200)  # musuh 1 update setiap 200ms

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)  # musuh 2 update setiap 500ms

# Fungsi untuk menggambar layar saat game aktif
def active_game():
    global player_gravity, obstacle_rect_list 

    window_screen.blit(skybox, (0,0))        # Gambar background langit
    window_screen.blit(ground, (0, 320))     # Gambar tanah

    score = display_score()                  # Tampilkan skor

    # Update posisi pemain karena gravitasi
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 320:
        player_rect.bottom = 320  # Biar nggak jatuh ke bawah tanah

    player_animation()                       # Jalankan animasi pemain
    window_screen.blit(player, player_rect)  # Gambar pemain

    obstacle_rect_list = obstacle_movement(obstacle_rect_list)  # Update dan gambar musuh

# Fungsi untuk menggambar layar saat game tidak aktif
def inactive_game():
    window_screen.fill((64, 64, 64))  # Background warna abu-abu

    # Tampilkan pemain di tengah layar
    window_screen.blit(player, (frame_size_x // 2 - 30 , frame_size_y // 2 - 30 ))

    # Tampilkan nama game
    game_name = font.render("Running Game", False, "white")
    game_name = pygame.transform.scale2x(game_name)
    game_name_rect = game_name.get_rect(center=(400, 80))

    # Tampilkan instruksi mulai
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))

    window_screen.blit(game_name, game_name_rect)
    window_screen.blit(game_message, game_message_rect)

# Fungsi untuk menghitung dan menampilkan skor berdasarkan waktu bermain
def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    window_screen.blit(score, score_rect)
    return current_time

# Fungsi untuk memindahkan obstacle dan menampilkannya
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5  # Gerakkan ke kiri
            if obstacle_rect.bottom == 320:
                window_screen.blit(enemy, obstacle_rect)  # Tipe musuh di tanah
            else:
                window_screen.blit(enemy2, obstacle_rect)  # Tipe musuh terbang
        # Hapus obstacle yang sudah keluar dari layar
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

# Fungsi untuk spawn dan animasi musuh
def spawn_enemy():
    global enemy_frame_index, enemy2_frame_index, enemy, enemy2

    if event.type == obstacle_timer:
        # Random spawn musuh 1 atau musuh 2
        if randint(0, 2):
            print("enemy has been spawned")
            # Musuh tanah
            obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900, 1100), 320)))
        else:
            # Musuh udara
            obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900, 1100), 210)))

    # Update frame animasi musuh 1
    if event.type == enemy_animation_timer:
        enemy_frame_index = 1 if enemy_frame_index == 0 else 0
        enemy = enemy_frames[enemy_frame_index]

    # Update frame animasi musuh 2
    if event.type == enemy2_animation_timer:
        enemy2_frame_index = 1 if enemy2_frame_index == 0 else 0
        enemy2 = enemy2_frames[enemy2_frame_index]

# Fungsi animasi pemain (jalan atau lompat)
def player_animation():
    global player_index, player
    if player_rect.bottom < 320:
        player = player_jump  # Saat di udara, pakai sprite lompat
    else:
        player_index += 0.1  # Animasi berjalan
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

# Loop utama game
while True:
    for event in pygame.event.get():
        # Keluar game jika tombol quit atau ESC ditekan
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            # Tangani spawn dan animasi musuh
            spawn_enemy()

            # Tangani input keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 320:
                    jump_sound.play()
                    player_gravity = -20  # Lompatan pemain

        else:
            # Aktifkan game saat tombol spasi ditekan
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 600)

    # Update layar tergantung status game
    if game_active:
        active_game()
    else:
        inactive_game()
        player_animation()

    # Perbarui tampilan dan atur kecepatan frame
    pygame.display.update()
    clock.tick(FPS)
