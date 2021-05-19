import pygame, random
from pygame.locals import * 
from pygame import mixer
from itertools import cycle


def game():
    # função que calcula posição aleatoria que a maçã aparecera
    def on_grid_random():
        x=random.randint(0,59)
        y=random.randint(0,59)
        return(x * 10,y * 10)

    # a colisão da cobrinha com a maçã
    def collision(c1,c2):
        return(c1[0]==c2[0]) and (c1[1]==c2[1])

    # variaveis de controle
    UP=0
    RIGHT=1
    DOWN=2
    LEFT=3

    # inica o pygame e cria uma tela
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('Snake')

    # inicia o mixer
    mixer.init()
    mixer.music.load("Going to Sleep 8bit.mp3")
    mixer.music.set_volume(0.4)
    mixer.music.play(-1)

    # a dimensão inicial e a cor da cobrinha
    snake = [(200, 200), (210, 200), (220,200)]
    snake_skin = pygame.Surface((10,10))
    snake_skin.fill((255,255,255))

    # a cor a dimensão e a cor da maçã
    apple_pos = on_grid_random()
    apple = pygame.Surface((10,10))
    apple.fill((255,0,0))

    # direção inicial que cobrinha vai
    my_direction = LEFT

    # um temporizador para reduzir a velocidade da cobrinha
    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 18)
    score = 0
    game_over = False



    # um loop para deixar o jogo rodando
    while not game_over:
        clock.tick(10)

        # captura eventos de entrada do usuario
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_UP and my_direction != DOWN:
                    my_direction = UP
                if event.key == K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT
                if event.key == K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT
                if event.key == K_p:
                    mixer.music.pause()
                if event.key == K_r:
                    mixer.music.unpause()

        # verifica a colisão entre a cobrinha e a maçã
        if collision(snake[0],apple_pos):
            apple_pos=on_grid_random()
            snake.append((0,0))
            score += 1

        # verifica a colisão entre a cobrinha e o cenario
        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            game_over = True
            break

        # verifica a colisão da cobrinha com ela mesma
        for i in range(1, len(snake)-1):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                game_over = True
                break

        # verifica se o game over é verdadeiro e sai do loop
        if game_over:
            break

        # faz a cobrinha se mover
        for i in range(len(snake)-1,0,-1):
            snake[i]=(snake[i-1][0],snake[i-1][1])

        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])

        # posiciona a maçã e a cobrinha na tela
        screen.fill((0,0,0))
        screen.blit(apple,apple_pos)

        # desenha as Gridlines
        for x in range(0, 600, 10):
            pygame.draw.line(screen,(40, 40, 40),(x,0),(x,600))

        for y in range(0, 600, 10):
            pygame.draw.line(screen,(40, 40, 40),(0, y),(600, y))

        # adicona o Score
        score_font = font.render("Score: %s" % (score), True, (255, 255, 255))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        # Controles da música
        music_font = pygame.font.Font('freesansbold.ttf', 14)
        music_text = "Music: p-pause r-resume"
        music_font = music_font.render(music_text, True, (255, 255, 255))
        music_rect = music_font.get_rect()
        music_rect.topleft = (5 , 10)
        screen.blit(music_font, music_rect)


        for pos in snake:
            screen.blit(snake_skin,pos)

        pygame.display.update()

    # loop se game over for diferente de false
    # toca o som de game over e coloca "game over" no topo da tela
    while True:
        mixer.music.stop()
        mixer.music.load("mixkit-arcade-retro-game-over-213.wav")
        mixer.music.set_volume(0.5)
        mixer.music.play()

        # Gamer Over message
        game_over_font = pygame.font.Font('freesansbold.ttf', 18)
        game_over_screen = game_over_font.render("GAME OVER",True,(255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (300, 300)

        # Restart message
        restart_font = pygame.font.Font('freesansbold.ttf', 18)
        restart_screen = restart_font.render("Press Space to Restart",True,(255, 255, 255))
        restart_rect = restart_screen.get_rect()
        restart_rect.midtop = (300, 330)

        screen.blit(game_over_screen, game_over_rect)
        screen.blit(restart_screen, restart_rect)
        pygame.display.update()
        pygame.time.wait(500)            
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game()
                        