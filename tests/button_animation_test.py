import pygame
import sys

pygame.init()
screen_width, screen_height = 600, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Button Animation Test")
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue_1 = (16, 28, 64)  # Darkest
blue_2 = (32, 56, 127)  # Mid
blue_3 = (52, 91, 203)  # Kinda light

arcon_font = "Arcon-Regular.ttf"

button_width = 300
button_height = 50
button_font_size = 35


class Button(object):
    def __init__(self, text, text_font, text_size, text_color, rect, button_color, button_img):
        self.text = text
        self.text_font = text_font
        self.text_size = text_size
        self.text_color = text_color
        self.text_background_color = button_color
        self.rect = rect  # (x_pos, y_pos, x, y)
        self.button_color = button_color
        self.button_img = button_img
        self.opacity_1 = 255
        self.opacity_2 = 0
        self.line_1 = self.rect[0]
        self.line_2 = self.rect[0] + self.rect[2]

    def draw(self):
        if self.button_img is None:
            # Fading Button
            button_surface = pygame.Surface((button_width, button_height))
            button_text_surface = get_text_surface(self.text, self.text_font, self.text_size, self.text_color)

            button_surface.fill((self.button_color[0], self.button_color[1], self.button_color[2]))
            button_surface.blit(button_text_surface, (button_surface.get_width()/2 - button_text_surface.get_width()/2,
                                                      0))
            button_surface.set_alpha(self.opacity_1)
            screen.blit(button_surface, (self.rect[0], self.rect[1]))

            # Appearing Button
            button_surface_2 = pygame.Surface((button_width, button_height))
            button_text_surface_2 = get_text_surface(self.text, self.text_font, self.text_size, self.button_color)

            button_surface_2.fill(white)  # Fill with background color
            button_surface_2.blit(button_text_surface_2, (button_surface_2.get_width()/2 -
                                  button_text_surface_2.get_width()/2, 0))
            button_surface_2.set_alpha(self.opacity_2)
            screen.blit(button_surface_2, (self.rect[0], self.rect[1]))

        else:
            screen.blit(self.button_img, (self.rect[0], self.rect[1]))
            if self.text is not None:
                button_text_surface = get_text_surface(self.text, self.text_font, self.text_size, self.text_color)
                screen.blit(button_text_surface, (self.rect[0] + self.rect[2] / 2 - button_text_surface.get_width() / 2,
                                                  self.rect[1]))

    def draw_line(self, start_pos, end_pos):
        pygame.draw.line(screen, self.button_color, start_pos, end_pos, 3)

    def hover(self):
        mos_x, mos_y = pygame.mouse.get_pos()
        if self.rect[0] <= mos_x <= (self.rect[0] + self.rect[2]) and self.rect[1] <= mos_y <= \
                (self.rect[1] + self.rect[3]):
            return True

        else:
            return False


def get_text_surface(text, text_font, text_size, text_color):
    font = pygame.font.Font(text_font, text_size)
    return font.render(text, True, text_color)


button = Button("Test", arcon_font, 36, white, (100, 100, button_width, button_height), blue_3, None)

while True:
    screen.fill(white)
    button.draw()

    if button.hover() is True:
        # Line Animation
        button.line_1 += 20
        if button.line_1 >= button.rect[0] + button.rect[2]:
            button.line_1 = button.rect[0] + button.rect[2] + 1
        button.draw_line((button.rect[0], button.rect[1]), (button.line_1, button.rect[1]))

        button.line_2 -= 20
        if button.line_2 <= button.rect[0]:
            button.line_2 = button.rect[0]
        button.draw_line((button.rect[0] + button.rect[2], button.rect[1] + button.rect[3]),
                         (button.line_2, button.rect[1] + button.rect[3]))

        # Fading
        button.opacity_1 -= 20
        if button.opacity_1 <= 0:
            button.opacity_1 = 0

        button.opacity_2 += 20
        if button.opacity_2 >= 255:
            button.opacity_2 = 255

    else:
        button.line_1 -= 20
        if button.line_1 <= button.rect[0]:
            button.line_1 = button.rect[0]
        button.draw_line((button.rect[0], button.rect[1]), (button.line_1, button.rect[1]))

        button.line_2 += 20
        if button.line_2 >= button.rect[0] + button.rect[2]:
            button.line_2 = button.rect[0] + button.rect[2]
        button.draw_line((button.rect[0] + button.rect[2], button.rect[1] + button.rect[3]), (button.line_2,
                         button.rect[1] + button.rect[3]))

        button.opacity_1 += 20
        if button.opacity_1 >= 255:
            button.opacity_1 = 255

        button.opacity_2 -= 20
        if button.opacity_2 <= 0:
            button.opacity_2 = 0

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
