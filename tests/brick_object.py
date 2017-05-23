import pygame
import sys

pygame.init()
screen_width, screen_height = 600, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brick Object")
clock = pygame.time.Clock()

sheet = pygame.image.load("Images/red_brick_sprite_sheet.png")

white = (255, 255, 255)
red = (255, 0, 0)


class Brick(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprite_x_pos = 0
        self.sprite_y_pos = 0
        self.sprite_x = 92
        self.sprite_y = 92
        self.rect = (self.sprite_x_pos, self.sprite_y_pos, self.sprite_x, self.sprite_y)

    def draw(self):
        # sheet.set_clip(pygame.Rect(sprite_rect_x, sprite_rect_y, sprite_x, sprite_y))
        sheet.set_clip(self.rect)
        # draw_me = sheet.subsurface(sheet.get_clip())
        draw_me = sheet.subsurface(sheet.get_clip())
        screen.blit(draw_me, (self.x_pos, self.y_pos))

    def update_sprite(self):
        self.sprite_x_pos += self.sprite_x
        if self.sprite_x_pos > sheet.get_width():
            self.sprite_x_pos = 0

        self.rect = (self.sprite_x_pos, self.sprite_y_pos, self.sprite_x, self.sprite_y)


brick1 = Brick(100, 100)
brick2 = Brick(170, 100)


def main_loop():
    while True:
        screen.fill(white)

        brick1.draw()
        brick2.draw()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


main_loop()
