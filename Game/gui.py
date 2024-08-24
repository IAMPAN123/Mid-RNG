import pygame

def draw_inventory(screen, inventory):
    # Draw inventory background
    pygame.draw.rect(screen, (50, 50, 50), (*inventory.inventory_position, inventory.inventory_width, inventory.inventory_height))

    # Draw 'Inventory' text
    screen.blit(inventory.inventory_text, (inventory.inventory_position[0] + 10, inventory.inventory_position[1] + 10))

    # Draw close button (rect and text 'X')
    inventory.close_button_rect = pygame.Rect(inventory.inventory_position[0] + inventory.inventory_width - 40, inventory.inventory_position[1] + 10, 30, 30)
    pygame.draw.rect(screen, (200, 0, 0), inventory.close_button_rect)  # Red button background
    pygame.draw.rect(screen, (255, 255, 255), inventory.close_button_rect, 2)  # White border
    close_text = inventory.font.render('X', True, (255, 255, 255))  # White 'X'
    screen.blit(close_text, (inventory.close_button_rect.x + 7, inventory.close_button_rect.y + 2))  # Positioning 'X' in the center

    # Draw inventory slots
    for i, (x, y) in enumerate(inventory.inventory_slots):
        pygame.draw.rect(screen, (100, 100, 100), (x, y, inventory.slot_size, inventory.slot_size))
        pygame.draw.rect(screen, (200, 200, 200), (x, y, inventory.slot_size, inventory.slot_size), 2)

        if inventory.selected_slot == i:  # Draw animation on the selected slot
            frame = inventory.idle_frames[inventory.animation_index // 10]
            screen.blit(frame, (x, y))
