import pygame
import sys

pygame.init()
screen_width, screen_height = 600, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paddle Object")
clock = pygame.time.Clock()

white = (255, 255, 255)
red = (255, 0, 0)


class Paddle(object):
    def __init__(self, y_pos):
        self.x = 100
        self.y = 15
        self.x_pos = pygame.mouse.get_pos()[0] - self.x/2

        self.x_pos = 200

        self.y_pos = y_pos
        self.rect = (self.x_pos, self.y_pos, self.x, self.y)
        self.color = red

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # self.update_paddle()

    def update_paddle(self):
        self.x_pos = pygame.mouse.get_pos()[0] - self.x/2
        if self.x_pos + self.x >= screen_width:
            self.x_pos = screen_width - self.x

        elif self.x_pos <= 0:
            self.x_pos = 0
        self.rect = (self.x_pos, self.y_pos, self.x, self.y)

    def btp_test(self):
        seg = self.x/7
        for i in range(1, 8):
            if self.x_pos + seg*(i - 1) <= pygame.mouse.get_pos()[0] <= self.x_pos + seg*i:
                print(i)

            else:
                pass


paddle = Paddle(500)


def main_loop():
    while True:
        screen.fill(white)
        paddle.draw()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                paddle.btp_test()


main_loop()
