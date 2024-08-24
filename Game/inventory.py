import pygame
from spritesheet import SpriteSheet

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.inventory_width = 300
        self.inventory_height = 350
        self.inventory_position = ((600 - self.inventory_width) // 2, (700 - self.inventory_height) // 2)
        self.font = pygame.font.SysFont(None, 36)
        self.inventory_text = self.font.render('Inventory', True, (255, 255, 255))
        self.slot_size = 32
        self.padding = 10
        self.selected_slot = None
        self.animation_index = 0
        self.is_open = False
        self.current_page = 1
        self.close_button_rect = None

        self.inventory_slots = self._create_slots()
        self.idle_frames = self._load_idle_frames()
        self.animation_speed = 100  # Adjust the speed of the animation (higher is slower)

    def _create_slots(self):
        slots = []
        # Calculate total width and height of the grid
        total_grid_width = (self.slot_size * 5) + (self.padding * 6)
        total_grid_height = (self.slot_size * 5) + (self.padding * 6)
        
        # Calculate offsets to centralize the grid within the inventory window
        offset_x = (self.inventory_width - total_grid_width) // 2
        offset_y = (self.inventory_height - total_grid_height) // 2

        for row in range(5):
            for col in range(5):
                x = self.inventory_position[0] + offset_x + self.padding + col * (self.slot_size + self.padding)
                y = self.inventory_position[1] + offset_y + self.padding + row * (self.slot_size + self.padding)
                slots.append((x, y))
        return slots

    def _load_idle_frames(self):
        idle_spritesheet_image = pygame.image.load('Images/idle_spritesheet.png').convert_alpha()
        sprite_sheet = SpriteSheet(idle_spritesheet_image)
        idle_frames = [sprite_sheet.get_image(i, 32, 32, 1, (0, 0, 0)) for i in range(4)]

        # Set white (255, 255, 255) as the transparent color (or whatever color is the background)
        for frame in idle_frames:
            frame.set_colorkey((255, 255, 255))  # Assuming white is the background you want to remove
        
        return idle_frames

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def handle_event(self, event):
        if self.is_open:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button_rect.collidepoint(mouse_x, mouse_y):
                    self.close()
                else:
                    self._check_slot_click(mouse_x, mouse_y)

    def _check_slot_click(self, mouse_x, mouse_y):
        for i, (x, y) in enumerate(self.inventory_slots):
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                if self.selected_slot != i:
                    self.selected_slot = i
                    self.animation_index = 0
                break

    def update_animation(self):
        if self.selected_slot is not None:
            self.animation_index += 1
            if self.animation_index >= len(self.idle_frames) * self.animation_speed:
                self.animation_index = 0

    def draw(self):
        """Draw the inventory window, slots, text, and close button."""
        # Draw inventory background
        pygame.draw.rect(self.screen, (50, 50, 50), (*self.inventory_position, self.inventory_width, self.inventory_height))

        # Draw 'Inventory' text
        self.screen.blit(self.inventory_text, (self.inventory_position[0] + 10, self.inventory_position[1] + 10))

        # Draw close button (rect and text 'X')
        self.close_button_rect = pygame.Rect(self.inventory_position[0] + self.inventory_width - 40, self.inventory_position[1] + 10, 30, 30)
        pygame.draw.rect(self.screen, (200, 0, 0), self.close_button_rect)  # Red button background
        pygame.draw.rect(self.screen, (255, 255, 255), self.close_button_rect, 2)  # White border
        close_text = self.font.render('X', True, (255, 255, 255))  # White 'X'
        self.screen.blit(close_text, (self.close_button_rect.x + 7, self.close_button_rect.y + 2))  # Positioning 'X' in the center

        # Draw inventory slots
        for i, (x, y) in enumerate(self.inventory_slots):
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, self.slot_size, self.slot_size), 2)

            if self.selected_slot == i:  # Draw animation on the selected slot
                frame_index = (self.animation_index // self.animation_speed) % len(self.idle_frames)
                frame = self.idle_frames[frame_index]
                self.screen.blit(frame, (x, y))
