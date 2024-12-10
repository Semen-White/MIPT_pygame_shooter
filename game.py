import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("My game")

backyard = pygame.image.load('images/backyard.jpg')
player = pygame.image.load('images/player_right/player_right1.png')
walk_right = [pygame.image.load('images/player_right/player_right1.png'),
    pygame.image.load('images/player_right/player_right2.png'),
    pygame.image.load('images/player_right/player_right3.png'),
    pygame.image.load('images/player_right/player_right4.png'),
    pygame.image.load('images/player_right/player_right5.png'),
    pygame.image.load('images/player_right/player_right6.png'),
    pygame.image.load('images/player_right/player_right7.png'),
    pygame.image.load('images/player_right/player_right8.png')
]

player_anim_count = 0

backyard_x = 0

running = True
while running:

    screen.blit(backyard, (backyard_x,0))
    screen.blit(backyard, (backyard_x + 700,0))
    screen.blit(walk_right[player_anim_count], (100, 320))

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

    clock.tick(15)
