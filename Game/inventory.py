import pygame
import json
from spritesheet import SpriteSheet

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.inventory_width = 400
        self.inventory_height = 500
        self.inventory_position = ((600 - self.inventory_width) // 2, (700 - self.inventory_height) // 3)
        self.font = pygame.font.SysFont(None, 36)
        self.description_font = pygame.font.SysFont(None, 18)
        self.line_spacing = 3
        self.inventory_text = self.font.render('Inventory', True, (255, 255, 255))
        self.slot_size = 50
        self.padding = 10
        self.selected_slot = None
        self.animation_index = 0
        self.is_open = False
        self.current_page = 1
        self.close_button_rect = None
        self.left_screen_width_ratio = 0.3
        self.right_screen_width_ratio = 0.7

        self.left_screen_width = int(self.inventory_width * self.left_screen_width_ratio)
        self.right_screen_width = int(self.inventory_width * self.right_screen_width_ratio)
        self.screen_height = 100

        self.inventory_slots = self._create_slots()
        self.idle_frames = self._load_idle_frames()
        self.item_images = self._load_item_images()  # Load item images
        self.item_descriptions = self._load_item_descriptions()

        self.animation_speed = 40

    def _create_slots(self):
        slots = []
        total_grid_width = (self.slot_size * 5) + (self.padding * 6)
        total_grid_height = (self.slot_size * 5) + (self.padding * 6)
        
        offset_x = (self.inventory_width - total_grid_width) // 2
        offset_y = (self.inventory_height - total_grid_height - self.screen_height - self.padding) // 1.4

        for row in range(5):
            for col in range(5):
                x = self.inventory_position[0] + offset_x + self.padding + col * (self.slot_size + self.padding)
                y = self.inventory_position[1] + offset_y + self.padding + row * (self.slot_size + self.padding)
                slots.append((x, y))
        return slots

    def _load_idle_frames(self):
        idle_spritesheet_image = pygame.image.load('Images/idle_spritesheet_new.png').convert_alpha()
        sprite_sheet = SpriteSheet(idle_spritesheet_image)
        idle_frames = [sprite_sheet.get_image(i, 50, 50, 1, (0, 0, 0)) for i in range(4)]
        for frame in idle_frames:
            frame.set_colorkey((255, 255, 255))
        return idle_frames

    def _load_item_images(self):
        """Load item images from the folder."""
        item_images = [
            pygame.image.load('Images/common_item.png').convert_alpha(),                    #1
            pygame.image.load('Images/uncommon_item.png').convert_alpha(),
            pygame.image.load('Images/rare_item.png').convert_alpha(),
            pygame.image.load('Images/legendary_item.png').convert_alpha(),
            pygame.image.load('Images/mid_item.png').convert_alpha(),
            # Add more as necessary for other slots
        ]

        # Resize images to fit into the slots if necessary
        for i, img in enumerate(item_images):
            if img is not None:
                item_images[i] = pygame.transform.scale(img, (self.slot_size, self.slot_size))

        return item_images

    def _load_item_descriptions(self):
        """Load item descriptions from an external JSON file."""
        with open('Game/item_descriptions.json', 'r') as file:
            descriptions = json.load(file)
        return descriptions

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
            # Increment the animation index
            self.animation_index += 1
            
            # Ensure the index wraps around the number of frames to loop the animation
            if self.animation_index >= len(self.idle_frames) * self.animation_speed:
                self.animation_index = 0


    def draw(self):
        """Draw the inventory window, slots, text, close button, and additional screens."""
        # Draw inventory background
        pygame.draw.rect(self.screen, (50, 50, 50), (*self.inventory_position, self.inventory_width, self.inventory_height))

        # Draw 'Inventory' text
        self.screen.blit(self.inventory_text, (self.inventory_position[0] + 20, self.inventory_position[1] + 20))

        # Draw close button (rect and text 'X')
        self.close_button_rect = pygame.Rect(self.inventory_position[0] + self.inventory_width - 60, self.inventory_position[1] + 20, 30, 30)
        pygame.draw.rect(self.screen, (200, 0, 0), self.close_button_rect)  # Red button background
        pygame.draw.rect(self.screen, (255, 255, 255), self.close_button_rect, 2)  # White border
        close_text = self.font.render('X', True, (255, 255, 255))  # White 'X'
        self.screen.blit(close_text, (self.close_button_rect.x + 7, self.close_button_rect.y + 2))  # Positioning 'X' in the center

        # Draw inventory slots
        for i, (x, y) in enumerate(self.inventory_slots):
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, self.slot_size, self.slot_size), 2)

            # Draw the item image if available
            if i < len(self.item_images) and self.item_images[i] is not None:
                item_image = pygame.transform.scale(self.item_images[i], (self.slot_size, self.slot_size))
                self.screen.blit(item_image, (x, y))  # Draw item image first

            # Draw the animation on the selected slot (on top of item image)
            if self.selected_slot == i:  
                frame_index = (self.animation_index // self.animation_speed) % len(self.idle_frames)
                frame = self.idle_frames[frame_index]
                self.screen.blit(frame, (x, y))  # Draw animation on top of the item image if selected


        # Draw the left screen (item image) inside the inventory window
        left_screen_x = self.inventory_position[0] + self.padding
        left_screen_y = self.inventory_position[1] + self.inventory_height - self.screen_height - 2 * self.padding  # Adjust for padding
        left_screen_width = self.left_screen_width - 2 * self.padding  # Adjust for padding on both sides
        left_screen_rect = pygame.Rect(left_screen_x, left_screen_y, left_screen_width, self.screen_height)
        pygame.draw.rect(self.screen, (70, 70, 70), left_screen_rect)

        # Draw the right screen (item description) inside the inventory window
        right_screen_x = left_screen_x + left_screen_width + self.padding  # Positioned next to the left screen
        right_screen_y = left_screen_y
        right_screen_width = self.right_screen_width - 2 * self.padding  # Adjust for padding
        right_screen_rect = pygame.Rect(right_screen_x, right_screen_y, right_screen_width, self.screen_height)
        pygame.draw.rect(self.screen, (70, 70, 70), right_screen_rect)

        # Display selected item image on the left screen
        if self.selected_slot is not None:
            if self.selected_slot < len(self.item_images) and self.item_images[self.selected_slot] is not None:
                item_image = pygame.transform.scale(self.item_images[self.selected_slot], (left_screen_width - 20, self.screen_height - 20))
                self.screen.blit(item_image, (left_screen_rect.x + 10, left_screen_rect.y + 10))  # Add small padding inside

            # Retrieve description for the selected slot from the loaded file
            description_data = self.item_descriptions.get(str(self.selected_slot), {"name": "Unknown", "description": "No description available."})
            
            # Prepare the description text
            description_lines = [
                f"Item Name: {description_data['name']}",
                "Description:",
                description_data['description']
            ]

            # Display description on the right screen
            for i, line in enumerate(description_lines):
                description_text = self.description_font.render(line, True, (255, 255, 255))
                self.screen.blit(description_text, (right_screen_rect.x + 10, right_screen_rect.y + 10 + i * (self.description_font.get_height() + self.line_spacing)))
