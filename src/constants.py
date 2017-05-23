"""
Constants
"""

import pygame

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
