import pygame #импортируем библиотеку pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700, 400)) #размеры игрового экрана
pygame.display.set_caption("My game") #название игры

#Player
backyard = pygame.image.load('images/backyard.jpg').convert() #картинка заднего фона
player = pygame.image.load('images/player_right/player_right1.png') #картинка игрока
walk_right = [pygame.image.load('images/player_right/player_right1.png'),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right5.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right6.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right7.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right8.png').convert_alpha()] #спрайт движения направо
walk_left = [pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left5.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left6.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left7.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left8.png').convert_alpha()] #спрайт движения налево

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
pygame.time.set_timer(enemy_timer, 3000)

label = pygame.font.Font('fonts/Poppins/Poppins-BlackItalic.ttf', 50)
lose_label = label.render('You lose :(', False, (193,196,199))
restart_label = label.render('Restart?', False, (115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(300, 250))

fireballs_left = 5
fireball = pygame.image.load('images/fireball.png').convert_alpha()
fireballs = []

gameplay = True

running = True
while running:

    screen.blit(backyard, (backyard_x,0))
    screen.blit(backyard, (backyard_x + 700,0))


    if gameplay: #основной игровой цикл

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y)) #хитбокс игрока

        if enemy_list_in_game:
             for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 5

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
            player_anim_count += 1

        backyard_x -= 2
        if backyard_x == -700:
            backyard_x = 0

        if fireballs:
            for (i, el) in enumerate(fireballs):
                screen.blit(fireball, (el.x, el.y))
                el.x += 12

                if el.x > 750:
                    fireballs.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            fireballs.pop(i)

    else:
        screen.fill((87,88,89))
        screen.blit(lose_label, (300, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] :
            gameplay = True
            player_x = 100
            enemy_list_in_game.clear()
            fireballs.clear()
            fireballs_left = 5

    pygame.display.update() #обновление экрана для движения на экране

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(710, 310)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and fireballs_left > 0:
            fireballs.append(fireball.get_rect(topleft=(player_x + 50, player_y + 10)))
            fireballs_left -= 1

    clock.tick(20)
