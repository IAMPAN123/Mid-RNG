import pygame
import json

class Equipment:
    def __init__(self, screen):
        self.screen = screen
        self.equipment_width = 400
        self.equipment_height = 600
        self.equipment_position = ((600 - self.equipment_width) // 2, (700 - self.equipment_height) // 3)
        self.font = pygame.font.SysFont(None, 36)
        self.description_font = pygame.font.SysFont(None, 18)
        self.line_spacing = 3
        self.equipment_text = self.font.render('Equipment', True, (255, 255, 255))
        self.slot_size = 50
        self.padding = 10
        self.selected_slot = None
        self.animation_index = 0
        self.is_open = False
        self.current_page = 1
        self.close_button_rect = None
        self.screen_height = 100
        self.inventory_slots = self._create_slots()

        self.item_images = self.load_item_images()
        self.item_to_slot_count = self.load_item_to_slot()

    def _create_slots(self):
        slots = []
        total_grid_width = (self.slot_size * 5) + (self.padding * 6)
        total_grid_height = (self.slot_size * 5) + (self.padding * 6)
        
        offset_x = (self.equipment_width - total_grid_width) // 2
        offset_y = (self.equipment_height - total_grid_height - self.screen_height - self.padding) // 1
        
        # Move the slots further down by adding a fixed value (pixels)
        offset_y += 70

        for row in range(5):
            for col in range(5):
                x = self.equipment_position[0] + offset_x + self.padding + col * (self.slot_size + self.padding)
                y = self.equipment_position[1] + offset_y + self.padding + row * (self.slot_size + self.padding)
                slots.append((x, y))
        return slots


    def load_item_images(self):
        """Load item images from the folder."""
        item_images = [
            pygame.image.load('Images/item0.png').convert_alpha(),                    #1
            pygame.image.load('Images/item1.png').convert_alpha(),
            pygame.image.load('Images/item2.png').convert_alpha(),
            pygame.image.load('Images/item3.png').convert_alpha(),
            pygame.image.load('Images/item4.png').convert_alpha(),
            pygame.image.load('Images/item5.png').convert_alpha(),
            pygame.image.load('Images/item6.png').convert_alpha(),
            pygame.image.load('Images/item7.png').convert_alpha(),
            pygame.image.load('Images/item8.png').convert_alpha(),
            pygame.image.load('Images/item9.png').convert_alpha(),
            pygame.image.load('Images/item10.png').convert_alpha(),
            pygame.image.load('Images/item11.png').convert_alpha(),
            pygame.image.load('Images/item12.png').convert_alpha(),
            pygame.image.load('Images/item13.png').convert_alpha(),
            pygame.image.load('Images/item14.png').convert_alpha(),
            pygame.image.load('Images/item15.png').convert_alpha(),
            pygame.image.load('Images/item16.png').convert_alpha(),
            pygame.image.load('Images/item17.png').convert_alpha(),
            pygame.image.load('Images/item18.png').convert_alpha(),
            pygame.image.load('Images/item19.png').convert_alpha(),
            pygame.image.load('Images/item20.png').convert_alpha(),
            pygame.image.load('Images/item21.png').convert_alpha(),
            pygame.image.load('Images/item22.png').convert_alpha(),
            pygame.image.load('Images/item23.png').convert_alpha(),
            pygame.image.load('Images/item24.png').convert_alpha(),
            # Add more as necessary for other slots
        ]

        # Resize images to fit into the slots if necessary
        for i, img in enumerate(item_images):
            if img is not None:
                item_images[i] = pygame.transform.scale(img, (self.slot_size, self.slot_size))
        return item_images

    def load_item_to_slot(self):
        """Load the item-to-slot mapping from a JSON file."""
        with open('Game/item_to_slot_count.json', 'r') as file:
            return json.load(file)
        
    def save_item_counts(self):
        """Save item counts to a JSON file."""
        with open('Game/item_to_slot_count.json', 'w') as file:
            json.dump(self.item_to_slot_count, file)

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

    def draw(self):
        """Draw the equipment window, slots, text, close button, and additional screens."""
        # Reload the item counter data to ensure it's up to date
        self.item_to_slot_count = self.load_item_to_slot()

        # Draw equipment background
        pygame.draw.rect(self.screen, (50, 50, 50), (*self.equipment_position, self.equipment_width, self.equipment_height))

        # Draw 'Equipment' text
        self.screen.blit(self.equipment_text, (self.equipment_position[0] + 20, self.equipment_position[1] + 20))

        # Draw close button (rect and text 'X')
        self.close_button_rect = pygame.Rect(self.equipment_position[0] + self.equipment_width - 60, self.equipment_position[1] + 20, 30, 30)
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

            # Draw the counter at the bottom right of each slot
            counter_value = self.item_to_slot_count.get(f"item{i}", 0)
            counter_text = self.description_font.render(str(counter_value), True, (255, 255, 255))
            counter_position = (x + self.slot_size - 15, y + self.slot_size - 15)  # Adjust for positioning
            self.screen.blit(counter_text, counter_position)
