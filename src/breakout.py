from __future__ import division

import random
import sys
import time
import pygame

pygame.init()
screen_width, screen_height = 552, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout V2")
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
blue_1 = (16, 28, 64)   # Darkest
blue_2 = (32, 56, 127)  # Mid
blue_3 = (52, 91, 203)  # Kinda light

# Fonts
arcon_font = "Fonts/Arcon-Regular.ttf"
comfortaa = "Fonts/Comfortaa_Regular.ttf"

# Images
# Buttons
quit_button_img = pygame.image.load("Images/quit_icon.png")
next_button_img = pygame.image.load("Images/next_icon.png")
back_button_img = pygame.image.load("Images/back_icon.png")
right_arrow_img = pygame.image.load("Images/right_arrow.png")
left_arrow_img = pygame.image.load("Images/left_arrow.png")
on_switch = pygame.image.load("Images/on_switch.png")
off_switch = pygame.image.load("Images/off_switch.png")

# Bricks
red_brick = pygame.image.load("Images/red_brick.png")
orange_brick = pygame.image.load("Images/orange_brick.png")
yellow_brick = pygame.image.load("Images/yellow_brick.png")
green_brick = pygame.image.load("Images/green_brick.png")
blue_brick = pygame.image.load("Images/blue_brick.png")
purple_brick = pygame.image.load("Images/purple_brick.png")
white_brick_1 = pygame.image.load("Images/white_brick_1.png")
white_brick_2 = pygame.image.load("Images/white_brick_2.png")
white_brick_3 = pygame.image.load("Images/white_brick_3.png")
gray_brick = pygame.image.load("Images/gray_brick.png")
red_brick_breaking_sheet = pygame.image.load("Images/red_brick_breaking.png")

# Color Selection
red_selection_1 = pygame.image.load("Images/red_selection_1.png")
red_selection_2 = pygame.image.load("Images/red_selection_2.png")
green_selection_1 = pygame.image.load("Images/green_selection_1.png")
green_selection_2 = pygame.image.load("Images/green_selection_2.png")
blue_selection_1 = pygame.image.load("Images/blue_selection_1.png")
blue_selection_2 = pygame.image.load("Images/blue_selection_2.png")


# Other Images
header_img = pygame.image.load("Images/Header.png")
mouse_img = pygame.image.load("Images/mouse.png")

# Audio
start_screen_music = pygame.mixer.Sound("Audio/start_screen_music.wav")
bounce = pygame.mixer.Sound("Audio/bounce.wav")

# Other Variables
button_width = 300
button_height = 50
button_font_size = 35
white_bricks = {1: white_brick_1, 2: white_brick_2, 3: white_brick_3}
game_ball_color = red


class Ball(object):
    def __init__(self, x_pos, y_pos, color, paddle):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = 10
        self.color = color
        self.move_x = 3
        self.move_y = 3
        self.rect = (self.x_pos - self.radius, self.y_pos - self.radius, self.radius*2, self.radius*2)
        self.angle_dict = {0: (-7, 1), 1: (-5, 1), 2: (-3, 3), 3: (-2, 4), 4: (random.choice((1, -1)), 4),
                           5: (2, 4), 6: (3, 3), 7: (5, 1), 8: (7, 1), "paused": (0, 0)}
        self.angle = 3
        self.paddle = paddle

    def draw(self):
        self.x_pos += self.move_x
        self.y_pos += self.move_y
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
        self.rect = (self.x_pos - self.radius, self.y_pos - self.radius, self.radius*2, self.radius*2)

        # Collision with screen
        if self.x_pos + 10 >= screen_width or self.x_pos - 10 <= 0:
            self.bounce_x()

        if self.y_pos + 10 >= screen_height or self.y_pos - 10 <= 0:
            self.bounce_y()

        # Ensures that the ball never goes out of the screen. (As sometimes paddle pushes ball out.)
        if self.x_pos >= screen_width:
            self.x_pos = screen_width - 100

        if self.x_pos <= 0:
            self.x_pos = 100

    def paddle_collision(self):
        if collision(self.rect, self.paddle.rect) is True:
            self.angle = self.btp_pos()
            # There is a weird issue where the ball would hit the very corner of the paddle and angle would be None
            if self.angle is None:
                if self.x_pos <= self.paddle.x_pos:
                    self.angle = 0

                else:
                    self.angle = 8

            self.move_x, self.move_y = self.angle_dict[self.angle]
            self.bounce_y()

        else:
            return False

    def brick_collision(self, brick):
        if collision(self.rect, brick.rect) is True:
            if brick.x_pos < self.x_pos < brick.x_pos + brick.x:
                self.bounce_y()

            elif brick.y_pos < self.y_pos < brick.y_pos + brick.y:
                self.bounce_x()

            else:
                self.bounce_x()
                self.bounce_y()

        else:
            return False

    def btp_pos(self):  # Ball to paddle position
        # Return 1 of 7 values
        # Each value at what angle the ball should bounce
        # Function should only be called when ball collides with paddle
        paddle_segment = self.paddle.x/7
        for i in range(1, 8):
            if self.paddle.x_pos + paddle_segment*(i - 1) <= self.x_pos <= self.paddle.x_pos + paddle_segment*i:
                return i

    def bounce_x(self):
        self.move_x *= -1
        if game_audio.ball_sound:
            bounce.play()

    def bounce_y(self):
        self.move_y *= -1
        if game_audio.ball_sound:
            bounce.play()


class Paddle(object):
    def __init__(self, y_pos, color):
        self.x = 100
        self.y = 15
        self.x_pos = 450
        self.y_pos = y_pos
        self.rect = (self.x_pos, self.y_pos, self.x, self.y)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.update_paddle()

    def update_paddle(self):
        self.x_pos = pygame.mouse.get_pos()[0] - self.x/2
        if self.x_pos + self.x >= screen_width:
            self.x_pos = screen_width - self.x

        elif self.x_pos <= 0:
            self.x_pos = 0
        self.rect = (self.x_pos, self.y_pos, self.x, self.y)


class Brick(object):
    def __init__(self, x_pos, y_pos, brick_image, destroyed=False):
        self.brick_image = brick_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x = 69
        self.y = 44
        self.sprite_x_pos = 0
        self.sprite_y_pos = 0
        self.sprite_x = 92
        self.sprite_y = 92
        self.rect = (self.x_pos, self.y_pos, self.x, self.y)
        self.cracked = 1  # Specifically for white bricks
        self.destroyed = destroyed
        self.timer = ObjectTimer()
        self.sprite_timer = ObjectTimer()

    def draw(self):
        red_brick_breaking_sheet.set_clip((self.sprite_x_pos, self.sprite_y_pos, self.sprite_x, self.sprite_y))
        breaking_surface = red_brick_breaking_sheet.subsurface(red_brick_breaking_sheet.get_clip())

        if self.brick_image == white_bricks[self.cracked]:
            if self.destroyed is True and self.cracked < 3:
                self.cracked += 1
                self.brick_image = white_bricks[self.cracked]
                self.destroyed = False

        if self.destroyed is False:
            self.sprite_x_pos = 0
            screen.blit(self.brick_image, (self.x_pos, self.y_pos))

        else:
            self.timer.reset_timer(1)
            if self.timer.check_time() is False:
                self.sprite_timer.reset_timer(0.0025)
                if self.sprite_timer.check_time() is False:
                    screen.blit(breaking_surface, (self.x_pos, self.y_pos))

                else:
                    self.sprite_x_pos += self.sprite_x
                    if self.sprite_x_pos >= red_brick_breaking_sheet.get_width():
                        self.sprite_x_pos = red_brick_breaking_sheet.get_width()

    def get_hit(self):
        if self.brick_image == gray_brick:
            self.destroyed = False

        else:
            self.destroyed = True


class Button(object):
    def __init__(self, background_color, text, text_font, text_size, text_color, rect, button_color):
        self.background_color = background_color
        # Button Text
        self.text = text
        self.text_font = text_font
        self.text_size = text_size
        self.text_color = text_color
        # Button
        self.rect = rect  # (x_pos, y_pos, x, y)
        self.button_color = button_color
        self.opacity_1 = 255
        self.opacity_2 = 0
        # Button lines
        self.line_1 = self.rect[0]
        self.line_2 = self.rect[0] + self.rect[2]

    def draw(self):
        # Fading
        button_surface = pygame.Surface((button_width, button_height))
        button_text_surface = get_text_surface(self.text, self.text_font, self.text_size, self.text_color)

        button_surface.fill((self.button_color[0], self.button_color[1], self.button_color[2]))
        button_surface.blit(button_text_surface, (button_surface.get_width()/2 - button_text_surface.get_width()/2,
                                                  0))
        button_surface.set_alpha(self.opacity_1)
        screen.blit(button_surface, (self.rect[0], self.rect[1]))

        # Appearing
        button_surface_2 = pygame.Surface((button_width, button_height))
        button_text_surface_2 = get_text_surface(self.text, self.text_font, self.text_size, self.button_color)

        button_surface_2.fill(self.background_color)
        button_surface_2.blit(button_text_surface_2, (button_surface_2.get_width()/2 -
                              button_text_surface_2.get_width()/2, 0))
        button_surface_2.set_alpha(self.opacity_2)
        screen.blit(button_surface_2, (self.rect[0], self.rect[1]))

    def hover(self):
        mos_x, mos_y = pygame.mouse.get_pos()
        if self.rect[0] <= mos_x <= (self.rect[0] + self.rect[2]) and self.rect[1] <= mos_y <= (self.rect[1] +
                                                                                                self.rect[3]):
            return True

        else:
            return False

    def draw_line(self, start_pos, end_pos):
        pygame.draw.line(screen, self.button_color, start_pos, end_pos, 3)

    def fading_animation(self):
        if self.hover() is True:
            # Upper line
            self.line_1 += 20
            if self.line_1 >= self.rect[0] + self.rect[2]:
                self.line_1 = self.rect[0] + self.rect[2] - 2
            self.draw_line((self.rect[0] + 1, self.rect[1]), (self.line_1 + 1, self.rect[1]))

            # Lower line
            self.line_2 -= 20
            if self.line_2 <= self.rect[0]:
                self.line_2 = self.rect[0] + 3
            self.draw_line((self.rect[0] + self.rect[2] - 2, self.rect[1] + self.rect[3] - 2), (self.line_2 - 2,
                           self.rect[1] + self.rect[3] - 2))

            # Fading
            self.opacity_1 -= 20
            if self.opacity_1 <= 0:
                self.opacity_1 = 0

            # Appearing
            self.opacity_2 += 20
            if self.opacity_2 >= 255:
                self.opacity_2 = 255

        else:
            self.line_1 -= 20
            if self.line_1 <= self.rect[0]:
                self.line_1 = self.rect[0]
            self.draw_line((self.rect[0] + 1, self.rect[1]), (self.line_1 + 1, self.rect[1]))

            self.line_2 += 20
            if self.line_2 >= self.rect[0] + self.rect[2]:
                self.line_2 = self.rect[0] + self.rect[2]
            # + 2 and - 2 are to help prevent the line from sticking out of the button
            self.draw_line((self.rect[0] + self.rect[2] - 2, self.rect[1] + self.rect[3] - 2), (self.line_2 - 2,
                           self.rect[1] + self.rect[3] - 2))

            self.opacity_1 += 20
            if self.opacity_1 >= 255:
                self.opacity_1 = 255

            self.opacity_2 -= 20
            if self.opacity_2 <= 0:
                self.opacity_2 = 0


class ButtonImage(object):
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image
        self.pressed = False

    def draw(self, button_states=None):
        # Only for on/off buttons
        if button_states is not None:
            if self.pressed:
                self.image = button_states[0]

            else:
                self.image = button_states[1]

        screen.blit(self.image, (self.rect[0], self.rect[1]))

    def hover(self):
        mos_x, mos_y = pygame.mouse.get_pos()
        if self.rect[0] <= mos_x <= (self.rect[0] + self.rect[2]) and \
           self.rect[1] <= mos_y <= (self.rect[1] + self.rect[3]):
            return True

        else:
            return False


class ControlsDemo(object):
    def __init__(self, mouse_rect, paddle_rect):
        # Mouse
        self.mouse_image = mouse_img
        self.mouse_rect = mouse_rect
        self.mouse_x_pos = mouse_rect[0]
        self.mouse_y_pos = mouse_rect[1]
        self.mouse_x = mouse_rect[2]
        self.mouse_y = mouse_rect[3]
        self.mouse_speed = -3
        self.mouse_timer = ObjectTimer()

        # Paddle
        self.paddle_rect = paddle_rect
        self.paddle_x_pos = paddle_rect[0]
        self.paddle_y_pos = paddle_rect[1]
        self.paddle_x = paddle_rect[2]
        self.paddle_y = paddle_rect[3]
        self.paddle_color = white
        self.paddle_speed = -6
        self.paddle_timer = ObjectTimer()

        # Instructions
        self.background_color = blue_1
        self.arrow_opacity = 255
        self.opacity_step = 10

    def draw_mouse(self):
        if 350 <= self.mouse_x_pos <= 500:
            self.mouse_x_pos += self.mouse_speed

        else:
            self.mouse_timer.reset_timer(1)
            if self.mouse_timer.check_time() is False:
                self.mouse_x_pos += 0

            else:
                self.mouse_speed = -self.mouse_speed
                self.mouse_x_pos += self.mouse_speed

        self.mouse_rect = (self.mouse_x_pos, self.mouse_y_pos, self.mouse_x, self.mouse_y)
        screen.blit(self.mouse_image, (self.mouse_x_pos, self.mouse_y_pos))

    def draw_paddle(self):
        if 150 <= self.paddle_x_pos <= 450:
            self.paddle_x_pos += self.paddle_speed

        else:
            self.paddle_timer.reset_timer(1)
            if self.paddle_timer.check_time() is False:
                self.paddle_x_pos += 0

            else:
                self.paddle_speed = -self.paddle_speed
                self.paddle_x_pos += self.paddle_speed

        self.paddle_rect = (self.paddle_x_pos, self.paddle_y_pos, self.paddle_x, self.paddle_y)
        pygame.draw.rect(screen, self.paddle_color, self.paddle_rect)

    def draw_instructions(self):
        # Text
        line_1 = get_text_surface("Control Paddle by", arcon_font, 40, white)
        line_2 = get_text_surface("Moving Mouse", arcon_font, 40, white)
        screen.blit(line_1, (screen_width/2 - line_1.get_width()/2, screen_height/2 - line_1.get_height()/2 - 50))
        screen.blit(line_2, (screen_width/2 - line_2.get_width()/2,
                             screen_height/2 - line_2.get_height()/2 + line_1.get_height() - 50))

        # Arrows
        right_arrow_surface = pygame.Surface((right_arrow_img.get_width(), right_arrow_img.get_height()))
        left_arrow_surface = pygame.Surface((left_arrow_img.get_width(), left_arrow_img.get_height()))
        right_arrow_surface.fill(self.background_color)
        left_arrow_surface.fill(self.background_color)
        right_arrow_surface.set_alpha(self.arrow_opacity)
        left_arrow_surface.set_alpha(self.arrow_opacity)

        right_arrow_surface.blit(right_arrow_img, (0, 0))
        left_arrow_surface.blit(left_arrow_img, (0, 0))
        screen.blit(right_arrow_surface, (455, screen_height/2 - right_arrow_img.get_height()))
        screen.blit(left_arrow_surface, (20, screen_height/2 - right_arrow_img.get_height()))


class BricksDemo(object):
    def __init__(self, paddle_rect, ball_rect, brick_rect):
        # Paddle
        self.paddle_rect = paddle_rect
        self.paddle_original_rect = paddle_rect
        self.paddle_x_pos = paddle_rect[0]
        self.paddle_y_pos = paddle_rect[1]
        self.paddle_x = paddle_rect[2]
        self.paddle_y = paddle_rect[3]
        self.paddle_color = white
        self.paddle_speed = -6

        # Ball
        self.ball_rect = ball_rect
        self.ball_original_rect = ball_rect
        self.ball_radius = int(ball_rect[2]/2)
        self.ball_x_pos = ball_rect[0] + self.ball_radius
        self.ball_y_pos = ball_rect[1] + self.ball_radius
        self.ball_color = red
        self.ball_x_speed = 3
        self.ball_y_speed = 3

        # Brick
        self.brick_rect = brick_rect
        self.brick_x_pos = brick_rect[0]
        self.brick_y_pos = brick_rect[1]
        self.brick_x = brick_rect[2]
        self.brick_y = brick_rect[3]
        self.brick_destroyed = False
        self.brick_timer = ObjectTimer()
        self.brick_sprite_x_pos = 0
        self.brick_sprite_y_pos = 0
        self.brick_sprite_x = 92
        self.brick_sprite_y = 92
        self.brick_sprite_timer = ObjectTimer()

        # Text
        self.line_1 = get_text_surface("Bounce Ball to", arcon_font, 50, white)
        self.line_2 = get_text_surface("Break Bricks", arcon_font, 50, white)

    def draw_paddle(self):
        if self.paddle_x_pos <= 150:
            self.draw_ball()

        elif self.paddle_x_pos > 150:
            self.paddle_x_pos += self.paddle_speed

        self.paddle_rect = (self.paddle_x_pos, self.paddle_y_pos, self.paddle_x, self.paddle_y)
        pygame.draw.rect(screen, self.paddle_color, self.paddle_rect)

    def draw_ball(self):
        self.ball_x_pos += self.ball_x_speed
        self.ball_y_pos += self.ball_y_speed
        self.ball_rect = (self.ball_x_pos - self.ball_radius, self.ball_y_pos - self.ball_radius, self.ball_radius*2,
                          self.ball_radius*2)
        pygame.draw.circle(screen, self.ball_color, (self.ball_x_pos, self.ball_y_pos), self.ball_radius)

        if collision(self.ball_rect, self.paddle_rect) is True:
            self.ball_y_speed = -self.ball_y_speed

        if collision(self.ball_rect, self.brick_rect) is True:
            self.brick_destroyed = True

    def draw_brick(self):
        red_brick_breaking_sheet.set_clip((self.brick_sprite_x_pos, self.brick_sprite_y_pos, self.brick_sprite_x,
                                           self.brick_sprite_y))
        animation_surface = red_brick_breaking_sheet.subsurface(red_brick_breaking_sheet.get_clip())

        if self.brick_destroyed is False:
            screen.blit(red_brick, (self.brick_x_pos, self.brick_y_pos))
            self.brick_sprite_x_pos = 0

        else:
            # Reset after 0.5s
            self.brick_timer.reset_timer(1)
            if self.brick_timer.check_time() is True:
                self.reset_objects()

            else:
                # Bounce ball
                self.ball_x_speed = -1
                self.ball_y_speed = -1

                # Brick breaking animation
                self.brick_sprite_timer.reset_timer(0.0025)
                if self.brick_sprite_timer.check_time() is False:
                    screen.blit(animation_surface, (self.brick_x_pos, self.brick_y_pos - self.brick_y/2))

                else:
                    # Don't show cracked brick
                    self.brick_sprite_x_pos += 92
                    if self.brick_sprite_x_pos > red_brick_breaking_sheet.get_width():
                        self.brick_sprite_x_pos = red_brick_breaking_sheet.get_width()

    def draw_instructions(self):
        screen.blit(self.line_1, (screen_width/2 - self.line_1.get_width()/2, 50))
        screen.blit(self.line_2, (screen_width/2 - self.line_2.get_width()/2, 50 + self.line_1.get_height()))

    def reset_objects(self):
        self.paddle_x_pos = self.paddle_original_rect[0]
        self.ball_x_pos = self.ball_original_rect[0]
        self.ball_y_pos = self.ball_original_rect[1]
        self.ball_x_speed = 3
        self.ball_y_speed = 3
        self.brick_destroyed = False


class ObjectTimer(object):
    def __init__(self):
        self.sec = 0
        self.current_time = time.perf_counter()
        self.wanted_time = time.perf_counter() + self.sec
        # self.counting attribute prevents timer object from constantly resetting itself in a loop
        self.counting = False

    def reset_timer(self, sec):
        if self.counting is False:
            self.sec = sec
            self.wanted_time = time.perf_counter() + self.sec
            self.counting = True

        else:
            pass

    def update_time(self):
        self.current_time = time.perf_counter()

    def check_time(self):
        self.update_time()
        if self.current_time >= self.wanted_time:
            self.counting = False
            return True

        else:
            return False


class Instructions(object):
    def __init__(self):
        self.next_button = ButtonImage((490, 580, 40, 40), next_button_img)
        self.back_button = ButtonImage((415, 580, 40, 40), back_button_img)
        self.control_objects = ControlsDemo((500, 50, 43, 68), (450, 500, 100, 15))
        self.brick_objects = BricksDemo((450, 500, 100, 15), (50, 350, 20, 20), (350, 300, 69, 43))

    def main_screen(self):
        while True:
            screen.fill(blue_1)

            # Text
            instructions_header = get_text_surface("How To Play", arcon_font, 50, white)
            objective_subheader = get_text_surface("Objective of The Game: ", arcon_font, 25, white)
            text_file = open("Text/Breakout-Objective.txt", "r")
            objective_raw_text = text_file.readlines()
            for i in range(0, len(objective_raw_text)):
                objective_text = get_text_surface(objective_raw_text[i].rstrip(), comfortaa, 17, white)
                screen.blit(objective_text, (30, 170 + i*(objective_text.get_height() + 2)))
            text_file.close()
            good_luck_text = get_text_surface("Good Luck!", arcon_font, 40, white)

            screen.blit(instructions_header, (screen_width/2 - instructions_header.get_width()/2, 30))
            screen.blit(objective_subheader, (30, 120))
            screen.blit(good_luck_text, (screen_width/2 - good_luck_text.get_width()/2, 350))

            # Buttons
            quit_button.draw()
            self.next_button.draw()
            self.back_button.draw()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.hover() is True:
                        start_screen()
                        sys.exit()

                    if next_button.hover() is True:
                        self.controls_screen()
                        sys.exit()

                    if back_button.hover() is True:
                        self.bricks_screen()
                        sys.exit()

    def controls_screen(self):
        while True:
            screen.fill(blue_1)

            # Controls Objects
            self.control_objects.draw_mouse()
            self.control_objects.draw_paddle()
            self.control_objects.draw_instructions()
            self.control_objects.arrow_opacity -= self.control_objects.opacity_step
            if self.control_objects.arrow_opacity <= 0 or self.control_objects.arrow_opacity >= 255:
                self.control_objects.opacity_step = -self.control_objects.opacity_step

            # Buttons
            quit_button.draw()
            self.next_button.draw()
            self.back_button.draw()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.hover() is True:
                        start_screen()
                        sys.exit()

                    if next_button.hover() is True:
                        self.bricks_screen()
                        sys.exit()

                    if back_button.hover() is True:
                        self.main_screen()
                        sys.exit()

    def bricks_screen(self):
        while True:
            screen.fill(blue_1)

            # Instruction Objects
            self.brick_objects.draw_instructions()
            self.brick_objects.draw_paddle()
            self.brick_objects.draw_brick()

            # Buttons
            quit_button.draw()
            self.next_button.draw()
            self.back_button.draw()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.hover() is True:
                        start_screen()
                        sys.exit()

                    if next_button.hover() is True:
                        self.main_screen()
                        sys.exit()

                    if back_button.hover() is True:
                        self.controls_screen()
                        sys.exit()


class ColorSettings(object):
    def __init__(self):
        self.ball_text = get_text_surface("BALL COLOR", comfortaa, 30, white)
        self.red_selection = ButtonImage((100, 350, 30, 30), red_selection_1)
        self.green_selection = ButtonImage((140, 350, 30, 30), green_selection_1)
        self.blue_selection = ButtonImage((180, 350, 30, 30), blue_selection_1)
        self.color_dict = {self.red_selection: red, self.green_selection: green, self.blue_selection: blue}
        self.red_selection.pressed = True  # Make sure the first button is pressed
        self.selected_color = red

    def draw(self):
        screen.blit(self.ball_text, (100, 300))
        self.red_selection.draw([red_selection_2, red_selection_1])
        self.green_selection.draw([green_selection_2, green_selection_1])
        self.blue_selection.draw([blue_selection_2, blue_selection_1])

    def update(self):
        buttons = list(self.color_dict.keys())  # List of buttons
        for b in buttons:
            if b.hover():
                b.pressed = not b.pressed

                # Give radio buttons effect of only having one selectable button
                if buttons.index(b) == 1:
                    buttons[0].pressed = False
                    buttons[2].pressed = False

                else:
                    opposite_index = len(buttons) - buttons.index(b) - 1
                    buttons[opposite_index].pressed = False
                    if opposite_index == 0:
                        buttons[opposite_index + 1].pressed = False

                    else:
                        buttons[opposite_index - 1].pressed = False

            if b.pressed:
                self.selected_color = self.color_dict[b]

    def get_color(self):
        return self.selected_color


class GamePlay(object):
    def __init__(self, ball_color):
        self.current_level = 1
        self.win = False
        self.game_over = False
        self.paddle = Paddle(570, black)
        self.ball = None
        self.ball_color = ball_color
        self.brick_colors = None
        self.brick_array = None

        # Pause Screen Objects
        self.continue_button = Button(blue_1, "Continue", arcon_font, button_font_size, white,
                                      (screen_width/2 - button_width/2, 220, button_width, button_height), blue_3)
        self.restart_button = Button(blue_1, "Restart", arcon_font, button_font_size, white,
                                     (screen_width/2 - button_width/2, 290, button_width, button_height), blue_2)
        self.pause_screen_buttons = [self.continue_button, self.restart_button]

        # Game Over and Win Screen Objects
        self.play_again_button = Button(blue_1, "Play Again", arcon_font, button_font_size, white,
                                        (screen_width/2 - button_width/2, 220, button_width, button_height), blue_3)
        self.next_level_button = Button(blue_1, "Next Level", arcon_font, button_font_size, white,
                                        (screen_width/2 - button_width/2, 220, button_width, button_height), blue_3)

    def update(self, current_level):
        self.win = False
        self.game_over = False

        if current_level == 1:
            self.ball = Ball(300, 400, self.ball_color, self.paddle)
            self.brick_colors = [red_brick, yellow_brick, green_brick, blue_brick]
            self.brick_array = create_bricks((1, 5), (1, 9), self.brick_colors, None, None, None)

        elif current_level == 2:
            self.ball = Ball(300, 400, self.ball_color, self.paddle)
            self.brick_colors = [red_brick, red_brick, orange_brick, orange_brick, yellow_brick]
            self.brick_array = create_bricks((1, 6), (1, 9), self.brick_colors, ((0, 0, 0, 3), (0, 5, 0, 8),
                                                                                 (1, 0, 1, 2), (1, 6, 1, 8),
                                                                                 (2, 0, 2, 1), (2, 7, 2, 8),
                                                                                 (3, 0, 3, 0), (3, 8, 3, 8)),
                                             ((3, 1), (3, 3), (3, 4), (3, 6)), None)

        elif current_level == 3:
            self.ball = Ball(300, 400, self.ball_color, self.paddle)
            self.brick_colors = [red_brick, orange_brick, yellow_brick, green_brick, blue_brick, purple_brick]
            self.brick_array = create_bricks((1, 7), (1, 9), self.brick_colors, None, None,
                                             ((0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3), (1, 5), (1, 7),
                                              (2, 0), (2, 2), (2, 4), (2, 6), (3, 1), (3, 3), (3, 5), (3, 7),
                                              (4, 0), (4, 2), (4, 4), (4, 6)))

        else:
            self.win = True
            self.finish_screen()

    def play(self, paused=False):
        if paused is False:
            self.update(self.current_level)

        while True:
            screen.fill(white)

            # Game Objects
            self.ball.draw()
            self.paddle.draw()
            self.ball.paddle_collision()
            for row in self.brick_array:
                for brick in row:
                    brick.draw()
                    if brick.destroyed is False:
                        if self.ball.brick_collision(brick) is not False:
                            brick.get_hit()

            # Win
            if win_condition(self.brick_array):
                self.current_level += 1
                self.finish_screen()
                sys.exit()

            # Game Over
            if lose_condition(self.ball, self.paddle):
                self.game_over = True
                self.finish_screen()
                sys.exit()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused_screen()
                        sys.exit()

                    if event.key == pygame.K_c:
                        self.current_level += 1
                        self.play()

    def paused_screen(self):
        while True:
            screen.fill(blue_1)

            header_surface = get_text_surface("PAUSED", arcon_font, 55, white)
            screen.blit(header_surface, (screen_width/2 - header_surface.get_width()/2, 75))
            for b in self.pause_screen_buttons:
                b.draw()
                b.fading_animation()
            quit_button.draw()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.continue_button.hover() is True:
                        self.play(paused=True)
                        sys.exit()

                    if self.restart_button.hover() is True:
                        self.play()
                        sys.exit()

                    if quit_button.hover() is True:
                        start_screen()
                        sys.exit()

    def finish_screen(self):
        while True:
            screen.fill(blue_1)

            if self.win is True:
                header_text = "YOU WIN!"

            elif self.game_over is True:
                header_text = "GAME OVER"

            else:
                header_text = "LEVEL COMPLETE!"

            header_surface = get_text_surface(header_text, arcon_font, 55, white)
            screen.blit(header_surface, (screen_width/2 - header_surface.get_width()/2, 75))

            if self.win is True or self.game_over is True:
                self.play_again_button.draw()
                self.play_again_button.fading_animation()

            else:
                self.next_level_button.draw()
                self.next_level_button.fading_animation()
            quit_button.draw()

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.win is True or self.game_over is True:
                        if self.play_again_button.hover() is True:
                            self.current_level = 1
                            self.win = False
                            self.game_over = False
                            self.play()
                            sys.exit()

                    else:
                        if self.next_level_button.hover() is True:
                            self.play()
                            sys.exit()

                    if quit_button.hover() is True:
                        self.win = False
                        self.game_over = False
                        start_screen()
                        sys.exit()


class GameAudio(object):
    def __init__(self):
        self.ball_sound = True
        self.start_screen_music = True

    def check_ball_sound(self):
        if self.ball_sound:
            return True

        else:
            return False

    def check_start_screen_music(self):
        if self.start_screen_music:
            return True

        else:
            return False


def get_text_surface(text, text_font, text_size, text_color):
    font = pygame.font.Font(text_font, text_size)
    return font.render(text, True, text_color)


def collision(rect_1, rect_2):  # Takes object rect
    cond_1 = (rect_1[1] + rect_1[3]) < rect_2[1]  # Bottom < Top
    cond_2 = rect_1[1] > (rect_2[1] + rect_2[3])  # Top > Bottom
    cond_3 = (rect_1[0] + rect_1[2]) < rect_2[0]  # Left < Right
    cond_4 = rect_1[0] > (rect_2[0] + rect_2[2])  # Right > Left

    if cond_1 is False:
        if cond_2 is False:
            if cond_3 is False:
                if cond_4 is False:
                    return True


def create_bricks(row_range, column_range, brick_colors, empty_spots, metal_bricks, cracked_bricks):
    matrix = [[1 for _ in range(column_range[0], column_range[1])] for _ in range(row_range[0], row_range[1])]

    if empty_spots is not None:
        for hole in empty_spots:
            # I have to do this since Python will not accept redundant parentheses.
            # If I only have one value nested in empty_spots, Python will ignore the extra parentheses
            if hole is not None:
                point_1 = (hole[0], hole[1])
                point_2 = (hole[2], hole[3])
                for i in range(point_1[1], point_2[1]):
                    matrix[point_1[0]][i] = 0

    if metal_bricks is not None:
        # I have to do this since Python will not accept redundant parentheses.
        # If I only have one value nested in empty_spots, Python will ignore the extra parentheses
        if type(metal_bricks[0]) != tuple:
            matrix[metal_bricks[0]][metal_bricks[1]] = 2

        else:
            for brick in metal_bricks:
                matrix[brick[0]][brick[1]] = 2

    if cracked_bricks is not None:
        if type(cracked_bricks[0]) != tuple:
            matrix[cracked_bricks[0]][cracked_bricks[1]] = 3

        else:
            for brick in cracked_bricks:
                matrix[brick[0]][brick[1]] = 3

    for r in matrix:
        for c in r:
            if c == 0:
                matrix[matrix.index(r)][r.index(c)] = Brick(69*(r.index(c)), 43*matrix.index(r),
                                                            brick_colors[matrix.index(r)], destroyed=True)

            elif c == 1:
                matrix[matrix.index(r)][r.index(c)] = Brick(69*(r.index(c)), 100 + 43*matrix.index(r),
                                                            brick_colors[matrix.index(r)])

            elif c == 2:
                matrix[matrix.index(r)][r.index(c)] = Brick(69*(r.index(c)), 100 + 43*matrix.index(r), gray_brick)

            elif c == 3:
                matrix[matrix.index(r)][r.index(c)] = Brick(69*(r.index(c)), 100 + 43*matrix.index(r), white_brick_1)

    return matrix


def win_condition(matrix):
    brick_count = 0
    metal_bricks = 0

    for i in matrix:
        for b in i:
            if b.brick_image == gray_brick:
                metal_bricks += 1

            if b.destroyed is True:
                brick_count += 1

    if brick_count >= len(matrix)*len(matrix[0]) - metal_bricks:
        return True


def lose_condition(ball, paddle):
    if ball.y_pos > paddle.y_pos + 50:
        return True


def start_screen():
    # The code is kinda ugly, but... it works
    global game_play
    global game_ball_color
    game_ball_color = color_settings.selected_color
    game_play = GamePlay(game_ball_color)

    start_screen_music.stop()
    if game_audio.start_screen_music:
        start_screen_music.play()

    else:
        start_screen_music.stop()
    start_screen_ball = Ball(10, 10, white, None)
    play_button = Button(blue_1, "Play", arcon_font, button_font_size, white,
                         (screen_width / 2 - button_width / 2, 220, button_width, button_height), blue_3)
    instructions_button = Button(blue_1, "How To Play", arcon_font, button_font_size, white, (screen_width/2 -
                                 button_width/2, 240 + button_height, button_width, button_height), blue_2)
    settings_button = Button(blue_1, "Settings", arcon_font, button_font_size, white, (screen_width/2 - button_width/2,
                             310 + button_height, button_width, button_height), blue_2)
    start_screen_buttons = [play_button, instructions_button, settings_button]

    while True:
        screen.fill(blue_1)

        start_screen_ball.draw()
        screen.blit(header_img, (screen_width/2 - header_img.get_width()/2, 60))
        quit_button.draw()

        # Buttons
        for b in start_screen_buttons:
            b.draw()
            # Collision with ball
            if collision(start_screen_ball.rect, b.rect) is True:
                if b.rect[0] <= start_screen_ball.x_pos + start_screen_ball.radius - 1 \
                        and b.rect[0] + b.rect[2] >= start_screen_ball.x_pos - start_screen_ball.radius + 1:
                    start_screen_ball.bounce_y()

                if b.rect[1] <= start_screen_ball.y_pos + start_screen_ball.radius - 2 \
                        and b.rect[3] + b.rect[1] >= start_screen_ball.y_pos - start_screen_ball.radius + 3:
                    start_screen_ball.bounce_x()

            # Hover Animation
            b.fading_animation()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.hover() is True:
                    game_play.current_level = 1
                    start_screen_music.stop()
                    game_play.play()
                    sys.exit()

                if instructions_button.hover() is True:
                    instructions.main_screen()
                    sys.exit()

                if settings_button.hover() is True:
                    settings_screen()
                    sys.exit()

                if quit_button.hover() is True:
                    sys.exit()


def settings_screen():
    global game_ball_color
    header_surface = get_text_surface("SETTINGS", arcon_font, 55, white)
    music_text = get_text_surface("MUSIC", comfortaa, 30, white)
    sound_text = get_text_surface("SOUND", comfortaa, 30, white)
    settings_text = get_text_surface("*NOTE: Exit to start screen to update settings.", comfortaa, 20, white)

    while True:
        screen.fill(blue_1)

        screen.blit(header_surface, (screen_width/2 - header_surface.get_width()/2, 50))
        screen.blit(music_text, (100, 150))
        screen.blit(sound_text, (100, 215))
        screen.blit(settings_text, (75, 425))
        music_button.draw([off_switch, on_switch])
        sound_button.draw([off_switch, on_switch])
        color_settings.draw()
        quit_button.draw()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                color_settings.update()
                game_ball_color = color_settings.get_color()

                if quit_button.hover() is True:
                    start_screen()
                    sys.exit()

                if music_button.hover() is True:
                    music_button.pressed = not music_button.pressed
                    game_audio.start_screen_music = not game_audio.start_screen_music

                if sound_button.hover() is True:
                    sound_button.pressed = not sound_button.pressed
                    game_audio.ball_sound = not game_audio.ball_sound


# Universal
quit_button = ButtonImage((40, 580, 40, 40), quit_button_img)
next_button = ButtonImage((490, 580, 40, 40), next_button_img)
back_button = ButtonImage((415, 580, 40, 40), back_button_img)
music_button = ButtonImage((350, 150, 77, 46), on_switch)
sound_button = ButtonImage((350, 215, 77, 46), on_switch)
instructions = Instructions()
color_settings = ColorSettings()
game_play = GamePlay(game_ball_color)
game_audio = GameAudio()

# Start Game
start_screen()
