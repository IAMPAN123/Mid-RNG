import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Idle Animation')

# Background color
BG = (50, 50, 50)  

# White color for transparency
WHITE = (255, 255, 255)  

# Load the sprite sheet image for idle animation
idle_sprite_sheet_image = pygame.image.load('Images/idle_spritesheet.png').convert_alpha()
idle_sprite_sheet = spritesheet.SpriteSheet(idle_sprite_sheet_image)

# Load frames for the idle animation (4 frames, each 32x32 pixels)
idle_frame_0 = idle_sprite_sheet.get_image(0, 32, 32, 3, WHITE)
idle_frame_1 = idle_sprite_sheet.get_image(1, 32, 32, 3, WHITE)
idle_frame_2 = idle_sprite_sheet.get_image(2, 32, 32, 3, WHITE)
idle_frame_3 = idle_sprite_sheet.get_image(3, 32, 32, 3, WHITE)

# List of idle frames
idle_frames = [idle_frame_0, idle_frame_1, idle_frame_2, idle_frame_3]

# Variables to manage animation state
idle_frame_index = 0
idle_animation_speed = 240  # Slower animation for 'desired fps' fps (60fps / 'desired fps' fps )
idle_animation_counter = 0

# Position of the idle animation on the screen
idle_position = (100, 100)  # Change (x, y) coordinates here to reposition the animation

run = True
while run:
    # Update background
    screen.fill(BG)

    # Animate the idle frames
    idle_animation_counter += 1
    if idle_animation_counter >= idle_animation_speed:
        idle_animation_counter = 0
        idle_frame_index = (idle_frame_index + 1) % len(idle_frames)

    # Display current idle frame at the specified position
    screen.blit(idle_frames[idle_frame_index], idle_position)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the display
    pygame.display.update()

pygame.quit()

### All comments are added by Lee Jun Yan for education purposes and proof of learning
### Source: https://www.youtube.com/watch?v=M6e3_8LHc7A&t