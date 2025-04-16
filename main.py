import pygame

pygame.init()
frame_size_x = 800 
frame_size_y = 400 

window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

pygame.display.set_caption("Running Game")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("gallery/fonts/Pixeltype.ttf", 32)

start_time = 0

game_active = False   #This variable is used to check whether the game is active or not

player_walk_1 = pygame.image.load("gallery/sprites/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("gallery/sprites/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player = player_walk[player_index]
player_jump = pygame.image.load("gallery/sprites/player/Player3.png").convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))
player_gravity = 0

skybox = pygame.image.load('gallery/sprites/Sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

def active_game():
    global player_gravity 
    window_screen.blit(skybox, (0,0))    #Tampilkan background
    window_screen.blit(ground, (0, 320))    #Tampilkan tanah/ground
    score = display_score()
    player_animation()   #Jalankan animasi pemain
    window_screen.blit(player, player_rect)   #Tampilkan pemain di layar


def inactive_game():
    window_screen.fill((64, 64, 64))
    window_screen.blit(player, (frame_size_x // 2 - 30 , frame_size_y//2 - 30 ))

    game_name = font.render("Running Game", False,"white")
    game_name = pygame.transform.scale2x(game_name)
    game_name_rect = game_name.get_rect(center=(400,80))
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))
    window_screen.blit(game_name, game_name_rect)
    window_screen.blit(game_message, game_message_rect)

def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    window_screen.blit(score, score_rect)
    return current_time

def player_animation():
    global player_index, player
    player_index += 0.1
    if player_index >= len(player_walk):
        player_index = 0
    player = player_walk[int(player_index)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            print("Game Active")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/600)

    if game_active:
        # print("Game Active")
        active_game()
    else:
        # print("Game Inactive")
        inactive_game()
        player_animation()

    pygame.display.update()
    clock.tick(FPS)
