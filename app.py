import sys
import pygame
import random
from time import sleep

pygame.init()


class Fruit():
    def __init__(self, window, window_pos, item_size):
        self.window_pos = window_pos
        self.window = window
        self.item_size = item_size
        self.color = 221, 75, 57
        self.randomize()

    def draw(self):
        pygame.draw.rect(self.window, self.color,
                         (self.x, self.y, self.item_size, self.item_size))

    def randomize(self):
        x = random.randrange(0, board_size[0])
        y = random.randrange(0, board_size[1])
        x += self.window_pos[0]
        y += self.window_pos[1]

        self.x = x - x % self.item_size
        self.y = y-y % self.item_size


class Snake():
    def __init__(self, window, window_size, window_pos, item_size):
        self.window = window
        self.window_size = window_size
        self.window_pos = window_pos

        self.item_size = item_size
        self.color = 66, 133, 244
        self.head_color = 70, 100, 232
        self.reset()

    def reset(self):
        x = self.window_size[0]//2+self.window_pos[0]
        y = self.window_size[1]//2+self.window_pos[1]
        self.snake = [
            {
                'x': x,
                'y': y
            }
        ]
        self.future_item = None
        self.dx = 1
        self.dy = 0

    def move(self):
        head = self.snake[0]
        self.future_item = self.snake.pop()
        self.snake.insert(0, {
            'x': (head['x'] - self.window_pos[0] + self.dx*self.item_size) % (self.window_size[0]) + self.window_pos[0],
            'y': (head['y'] - self.window_pos[1] + self.dy*self.item_size) % (self.window_size[1]) + self.window_pos[1]
        })

    def draw(self):
        for i, item in enumerate(self.snake):
            color = self.color
            if i == 0:
                color = self.head_color

            pygame.draw.rect(
                self.window, color, (item['x'], item['y'], self.item_size, self.item_size))

    def eat(self, fruit):
        head = self.snake[0]
        return abs(head['x']-fruit.x) < 20 and abs(head['y']-fruit.y) < 20

    def overlap(self):
        return self.snake.count(self.snake[0]) > 1

    def grow(self):
        self.snake.append(self.future_item)


# global variables
score = record = 0
game_started = False


size = width, height = 600, 600
board_size = size[0] * 0.8, size[1] * 0.8
window_pos = ((size[0]-board_size[0])//2, (size[1]-board_size[1])//2)
display_surface = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 72)
game_over_text = font.render('Game Over.', False, (153, 21, 0))
intro_text = font.render('PySnake', False, (255, 255, 255))


snake = Snake(display_surface, window_size=board_size,
              window_pos=((size[0] - board_size[0]) // 2,
                          (size[1] - board_size[1]) // 2),
              item_size=20)
fruit = Fruit(display_surface, window_pos, item_size=20)

apple_image = {
    'size': {
        'width': 40,
        'height': 40
    }
}

apple_image['pos'] = {
    'x': (window_pos[0] - apple_image['size']['width']) // 2,
    'y': (window_pos[1] - apple_image['size']['height']) // 2,
}
apple_image['image'] = pygame.transform.scale(
    pygame.image.load('./images/apple.png'), (apple_image['size']['width'], apple_image['size']['height']))


trophy_image = {
    'size': {
        'width': 40,
        'height': 40
    }
}

trophy_image['pos'] = {
    'x': (size[0]-apple_image['pos']['x']-trophy_image['size']['width']),
    'y': (window_pos[1] - apple_image['size']['height']) // 2,
}
trophy_image['image'] = pygame.transform.scale(
    pygame.image.load('./images/trophy.png'), (trophy_image['size']['width'], trophy_image['size']['height']))


clock = pygame.time.Clock()
game_over = False
press_spacebar_to_play_again = {
    "text": pygame.font.SysFont('Comic Sans MS', 24).render('Press SPACEBAR to play again.', False, (153, 21, 0)),
    "hidden": True
}

press_spacebar_to_start = {
    "text": pygame.font.SysFont('Comic Sans MS', 24).render('Press SPACEBAR to Start', False, (255, 255, 255)),
    "hidden": True
}


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.dx <= 0:
                snake.dx = -1
                snake.dy = 0
                continue
            elif event.key == pygame.K_RIGHT and snake.dx >= 0:
                snake.dx = 1
                snake.dy = 0
                continue
            elif event.key == pygame.K_UP and snake.dy <= 0:
                snake.dx = 0
                snake.dy = -1
                continue
            elif event.key == pygame.K_DOWN and snake.dy >= 0:
                snake.dx = 0
                snake.dy = 1
                continue
            elif event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif game_over:
                    snake.reset()
                    score = 0
                    game_over = False

    if not game_started:
        display_surface.fill((33, 150, 243))
        display_surface.blit(
            intro_text, ((size[0] - intro_text.get_width()) // 2, (size[1] - intro_text.get_height() - intro_text.get_height()) // 2))

        if not press_spacebar_to_start['hidden']:
            display_surface.blit(
                press_spacebar_to_start['text'], ((size[0] - press_spacebar_to_start['text'].get_width()) // 2, size[0]-50))

        press_spacebar_to_start['hidden'] = not press_spacebar_to_start['hidden']
        pygame.display.flip()
        clock.tick(1)
    elif game_over:
        display_surface.fill((232, 92, 70))
        display_surface.blit(
            game_over_text, ((size[0] - game_over_text.get_width()) // 2, (size[1] - game_over_text.get_height() - game_over_text.get_height()) // 2))

        if not press_spacebar_to_play_again['hidden']:
            display_surface.blit(
                press_spacebar_to_play_again['text'], ((size[0] - press_spacebar_to_play_again['text'].get_width()) // 2, size[0]-50))

        press_spacebar_to_play_again['hidden'] = not press_spacebar_to_play_again['hidden']
        pygame.display.flip()
        clock.tick(1)
    else:
        score_text = pygame.font.SysFont('Arial', 20).render(
            str(score), False, (200, 200, 200))
        record_text = pygame.font.SysFont('Arial', 20).render(
            str(record), False, (200, 200, 200))

        display_surface.fill((86, 138, 52))
        pygame.draw.rect(display_surface, (170, 215, 81),
                         (window_pos[0], window_pos[1], board_size[0], board_size[1]))

        pygame.draw.rect(display_surface, (74, 117, 44),
                         (0, 0, size[0], window_pos[1]))

        snake.move()
        fruit.draw()
        if snake.eat(fruit):
            snake.grow()
            score += 1
            record = score if score > record else record
            fruit.randomize()
        if snake.overlap():
            # game over
            game_over = True
            sleep(1)
        snake.draw()
        display_surface.blit(
            apple_image['image'], (apple_image['pos']['x'], apple_image['pos']['y']))
        display_surface.blit(
            score_text, (apple_image['pos']['x']+apple_image['size']['width'], apple_image['pos']['y']+10))
        display_surface.blit(
            trophy_image['image'], (trophy_image['pos']['x'], trophy_image['pos']['y']))
        display_surface.blit(
            record_text, (trophy_image['pos']['x']-10, trophy_image['pos']['y']+10))

        pygame.display.flip()
        clock.tick(10)
