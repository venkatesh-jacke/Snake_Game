import pygame
import random
pygame.init()

pygame.mixer.init()
# creating window

screen_width = 900
screen_height = 900
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("snake game")
carImg = pygame.image.load('apple.png')
overImg = pygame.image.load('snake.gif')
welcm = pygame.image.load('welcome.jpg')
green = (1, 50, 32)


# Game specific variables
start_on = True


def start_game():
    pygame.mixer.music.load('media.io_background.wav')
    pygame.mixer.music.play(20)
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    snake_width = 20
    FPS = 60
    snake_mv = 'r'
    food_pos = (random.randint(1, 880), random.randint(70, 880))
    head = [[snake_x, snake_y]]
    snake_len = 1
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Snake Chan", 29)
    font2 = pygame.font.SysFont("Snake Chan", 45)
    return exit_game, game_over, snake_x, snake_y, snake_width, FPS, snake_mv, food_pos, head, snake_len, clock, font, font2

exit_game, game_over, snake_x, snake_y, snake_width, FPS, snake_mv, food_pos, head, snake_len, clock, font, font2 = start_game()
def plot_snake(gameWindow, head, snake_width):
    pygame.draw.circle(gameWindow, green, [head[-1][0] + snake_width//2, head[-1][1] + snake_width//2], snake_width//2 + 1)
    if snake_len//3 < snake_width//2:
        for i in range(0, len(head)//3):
            pygame.draw.circle(gameWindow, green, [head[i][0] + snake_width//2, head[i][1] + snake_width//2], snake_width//2 + i - snake_len//3)
        for i in head[len(head)//3:-1]:
            pygame.draw.circle(gameWindow, green, [i[0] + snake_width//2, i[1] + snake_width//2], snake_width//2)
    else:
        for i in range(0, snake_width//2):
            pygame.draw.circle(gameWindow, green, [head[i][0] + snake_width//2, head[i][1] + snake_width//2], snake_width//2 - snake_width//2 + i)
        for i in head[snake_width//2:-1]:
            pygame.draw.circle(gameWindow, green, [i[0] + snake_width//2, i[1] + snake_width//2], snake_width//2)
    if snake_mv == 'u' or snake_mv == 'd':
        pygame.draw.circle(gameWindow, (255, 255, 255), [head[-1][0] + snake_width//2 + 3, head[-1][1] + snake_width//2], 2)
        pygame.draw.circle(gameWindow, (255, 255, 255), [head[-1][0] + snake_width//2 - 3, head[-1][1] + snake_width//2], 2)
    else:
        pygame.draw.circle(gameWindow, (255, 255, 255), [head[-1][0] + snake_width//2, head[-1][1] + snake_width//2 - 3], 2)
        pygame.draw.circle(gameWindow, (255, 255, 255), [head[-1][0] + snake_width//2, head[-1][1] + snake_width//2 + 3], 2)

def put_text(text, color, x, y, font):
    text_screen = font.render(text, True, color)
    gameWindow.blit(text_screen, [x, y])

with open("high_score.txt", "r") as f:
    high_score = int(f.read())
# Creating a game loop
sound1 = pygame.mixer.Sound('bite.wav')
while not exit_game:
    while start_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_on = False
        gameWindow.blit(welcm, (0, 0))
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake_mv != 'l':
                snake_mv = 'r'
            elif event.key == pygame.K_LEFT and snake_mv != 'r':
                snake_mv = 'l'
            elif event.key == pygame.K_UP and snake_mv != 'd':
                snake_mv = 'u'
            elif event.key == pygame.K_DOWN and snake_mv != 'u':
                snake_mv = 'd'
    if snake_mv == 'r':
        snake_x += 4
    elif snake_mv == 'l':
        snake_x -= 4
    elif snake_mv == 'u':
        snake_y -= 4
    elif snake_mv == 'd':
        snake_y += 4


    if snake_x in range(food_pos[0], food_pos[0] + 40) and snake_y in range(food_pos[1], food_pos[1] + 40):
        snake_len += 1
        sound1.play()
        head.append([snake_x, snake_y])
        food_pos = (random.randint(1, 880), random.randint(70, 880))
    else:
        # if len(head) > snake_len:
        head.append([snake_x, snake_y])
        del head[0]
    gameWindow.fill((255, 255, 255))
    if snake_len - 1 > high_score:
        high_score = snake_len - 1
    if head[-1][0] >= 900 or head[-1][0] <= 1 or head[-1][1] >= 900 or head[-1][1] <= 60 or head[-1] in head[:-1]:
        pygame.mixer.music.load('bite.wav')
        pygame.mixer.music.play()
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))
        game_over = True
        while game_over == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        exit_game, game_over, snake_x, snake_y, snake_width, FPS, snake_mv, food_pos, head, snake_len, clock, font, font2 = start_game()
                        gameWindow.fill((255, 255, 255))
                        put_text('score : ' + str(snake_len - 1), green, 10, 10, font)
                        put_text('highest score : ' + str(high_score), green, 450, 10, font)
                        pygame.draw.line(gameWindow, (0, 0, 0), (0, 60), (900, 60), 5)
                        gameWindow.blit(carImg, (food_pos[0], food_pos[1]))
                        plot_snake(gameWindow, head, snake_width)
                        pygame.display.update()
                        clock.tick(FPS)
                        game_over = False
                        continue
                    else:
                        pygame.quit()
                        exit()
            pygame.display.update()
            clock.tick(FPS)
            gameWindow.blit(overImg, (340, 180))
            put_text('Game over', green, 300, 400, font2)
            put_text('press ENTER to restart or any other key', green, 20, 500, font)
        # break
    put_text('score : ' + str(snake_len - 1), green, 10, 10, font)
    put_text('highest score : ' + str(high_score), green, 450, 10, font)
    pygame.draw.line(gameWindow, (0, 0, 0), (0, 60), (900, 60), 5)
    gameWindow.blit(carImg, (food_pos[0], food_pos[1]))
    plot_snake(gameWindow, head, snake_width)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
exit()
#Created by my workshop experience