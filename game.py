import pygame  # импортируем библиотеку pygame
import random as rd

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700, 400))  # размеры игрового экрана
pygame.display.set_caption("Ghost girl")  # название игры

ticks = 60

# Player
startscreen = pygame.image.load('images/start_screen.png').convert_alpha()
backyard_sound = pygame.mixer.Sound('sounds/music.mp3')
backyard = pygame.image.load('images/backyard.jpg').convert()  # картинка заднего фона
player = pygame.image.load('images/player_right/player_right1.png')  # картинка игрока
walk_right = [pygame.image.load('images/player_right/player_right1.png'),
              pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right5.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right6.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right7.png').convert_alpha(),
              pygame.image.load('images/player_right/player_right8.png').convert_alpha()]  # спрайт движения направо
walk_left = [pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left5.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left6.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left7.png').convert_alpha(),
             pygame.image.load('images/player_left/player_left8.png').convert_alpha()]  # спрайт движения налево

enemy = pygame.image.load('images/enemy/ghost.png').convert_alpha()
enemy_list_in_game = []

player_anim_count = 0
player_anim_count_0 = 0
backyard_x = 0

player_speed = 10 - ticks // 10
player_x = 100
player_y = 320

is_jump = False
jump_count = 7

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)
enemy_spawn_time = 0

label = pygame.font.Font('fonts/Poppins/Poppins-BlackItalic.ttf', 35)
lose_label = label.render('You lose :(', False, (232, 137, 218))
restart_label = label.render('Restart?', False, (232, 137, 218))
restart_label_rect = restart_label.get_rect(topleft=(480, 75))
play_label = label.render('Play', False, (232, 137, 218))
play_label_rect = play_label.get_rect(topleft=(480, 75))
start_label = label.render('Ghost Girl', False, (232, 137, 218))

fireballs_left = 10000
fireball = pygame.image.load('images/fireball.png').convert_alpha()
fireball_boom = pygame.image.load(
    'images/explode (1).png').convert_alpha()  # <--------- вставить картинку взрыва файрболла
fireballs = []

gameplay = True
running = True
start = False

while running:

    screen.blit(startscreen, (0, 0))
    screen.blit(play_label, play_label_rect)
    screen.blit(start_label, (400, 25))
    mouse = pygame.mouse.get_pos()
    if play_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        start = True

    if start:

        screen.blit(backyard, (backyard_x, 0))
        screen.blit(backyard, (backyard_x + 700, 0))

        if gameplay:  # основной игровой цикл

            backyard_sound.play()
            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))  # хитбокс игрока

            if enemy_list_in_game:
                for (i, el) in enumerate(enemy_list_in_game):
                    # enemy_spawn_time = rd.randint(1000,5000)
                    # pygame.time.set_timer(enemy_timer, enemy_spawn_time)
                    screen.blit(enemy, el)
                    # enemy_speed_mod = rd.randint(-10,10)
                    el.x -= 5  # + enemy_speed_mod

                    if el.x < -50:
                        enemy_list_in_game.pop(i)

                    if player_rect.colliderect(el):
                        gameplay = False
            keys = pygame.key.get_pressed()

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
                if jump_count >= -7:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 0.5
                else:
                    is_jump = False
                    jump_count = 7

            if is_jump == False:  # <------------------- Анимация прыжка и замедление скорости для увеличенных тиков
                if player_anim_count == 7:
                    player_anim_count = 0
                    player_anim_count_0 = 0
                else:
                    player_anim_count_0 += 0.1
                    player_anim_count = int(player_anim_count_0)

            backyard_x -= 2
            if backyard_x == -700:
                backyard_x = 0

            if fireballs:
                print(fireballs)
                for (i, el) in enumerate(fireballs):
                    screen.blit(fireball, (el.x, el.y))
                    el.x += 12

                    if el.x > 750:
                        fireballs.pop(i)

                    if enemy_list_in_game:
                        for (index, enemy_el) in enumerate(enemy_list_in_game):
                            if el.colliderect(enemy_el):
                                screen.blit(fireball_boom, (el.x, el.y))
                                enemy_list_in_game.pop(index)
                                fireballs.pop(i)

        else:
            screen.blit(startscreen, (0, 0))
            screen.blit(lose_label, (450, 25))
            screen.blit(restart_label, restart_label_rect)

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = 100
                enemy_list_in_game.clear()
                fireballs.clear()
                fireballs_left = 10000

    pygame.display.update()  # обновление экрана для движения на экране

    for event in pygame.event.get():
        enemy_spawn_time = rd.randint(0, 15)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:  # or enemy_spawn_time >= 6
            # enemy_spawn_time += rd.randint(0,10000)
            enemy_list_in_game.append(enemy.get_rect(topleft=(710, 310)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and fireballs_left > 0:
            fireballs.append(fireball.get_rect(topleft=(player_x + 50, player_y + 10)))
            fireballs_left -= 1

    clock.tick(ticks)
