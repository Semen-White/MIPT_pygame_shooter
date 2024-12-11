import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("My game")

#Player
backyard = pygame.image.load('images/backyard.jpg').convert()
player = pygame.image.load('images/player_right/player_right1.png')
walk_right = [pygame.image.load('images/player_right/player_right1.png'),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right5.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right6.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right7.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right8.png').convert_alpha()]
walk_left = [pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left5.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left6.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left7.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left8.png').convert_alpha()]

enemy = pygame.image.load('images/enemy/ghost.png').convert_alpha()
enemy_list_in_game = []

player_anim_count = 0
backyard_x = 0

player_speed = 10
player_x = 100
player_y = 320

is_jump = False
jump_count = 8

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 7000)


running = True
while running:
    keys = pygame.key.get_pressed()
    screen.blit(backyard, (backyard_x,0))
    screen.blit(backyard, (backyard_x + 700,0))

    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

    if enemy_list_in_game:
        for el in enemy_list_in_game:
            screen.blit(enemy, el)
            el.x -= 5

            if player_rect.colliderect(el):
                print("You lose")



    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))




    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 600:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_UP]:
            is_jump = True
    else:
        if jump_count >= -8:
            if jump_count > 0:
                player_y -= (jump_count ** 2) / 2
            else:
                player_y += (jump_count ** 2) / 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 8

    if player_anim_count == 7:
        player_anim_count = 0
    else:
        player_anim_count +=1

    backyard_x -= 2
    if backyard_x == -700:
        backyard_x = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(710, 310)))
    clock.tick(20)
