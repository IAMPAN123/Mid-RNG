import pygame
import json
from spritesheet import SpriteSheet

class Inventory:
    def __init__(self, screen):
        self.screen = screen #inventory screens
        self.inventory_width = 400
        self.inventory_height = 560
        self.inventory_position = ((600 - self.inventory_width) // 2, (700 - self.inventory_height) // 3)
        self.font = pygame.font.SysFont(None, 36) #fonts, spacing
        self.description_font = pygame.font.SysFont(None, 18)
        self.line_spacing = 3
        self.inventory_text = self.font.render('Inventory', True, (255, 255, 255))
        self.slot_size = 50 #slots, spacing, idle animation
        self.padding = 10
        self.selected_slot = None
        self.animation_index = 0
        self.is_open = False #page navigation
        self.current_page = 1
        self.close_button_rect = None #inventory exit button
        self.left_screen_width_ratio = 0.3 #botton panels
        self.right_screen_width_ratio = 0.7
        self.locked_image = pygame.image.load('Images/locked.png')

        self.left_screen_width = int(self.inventory_width * self.left_screen_width_ratio) 
        self.right_screen_width = int(self.inventory_width * self.right_screen_width_ratio)
        self.screen_height = 100

        self.inventory_slots = self._create_slots()
        self.idle_frames = self.load_idle_frames()
        self.item_images = self.load_item_images()  # Load item images
        self.item_descriptions = self.load_item_descriptions()
        self.item_to_slot_count = self.load_item_to_slot()

        self.animation_speed = 40

        # Crafting slots
        self.item_to_slot_count_file = 'Game/item_to_slot_count.json'
        self.load_item_to_slot()
        self.crafting_recipes = {
            ('Common','Uncommon'): "Finger",  # item0 + item1 = equip0
            ('Mythic', 'Fraud'): "Baby Rattle",  # item2 + item3 = equip1
            ('Worm', 'Gambler'): "ISOH",  # item4 + item5 = equip2
            ('Cat', 'Freaky'): "Jail World",  # item6 + item7 = equip3
            ('Nah', 'Void'): "Sex() Eyes",  # item8 + item9 = equip4
            # Add more recipes as needed
        }
        self.selected_slot1 = None
        self.selected_slot2 = None
        
        self.merge_button_rect = None
        self.last_click_time = None
        self.is_clicking = False

        # Additional crafting slots
        self.crafting_slots = self._create_crafting_slots()

    def _create_slots(self):
        slots = []
        total_grid_width = (self.slot_size * 5) + (self.padding * 6)
        total_grid_height = (self.slot_size * 5) + (self.padding * 6)
        
        offset_x = (self.inventory_width - total_grid_width) // 2
        offset_y = (self.inventory_height - total_grid_height - self.screen_height - self.padding) // 2.4

        for row in range(5):
            for col in range(5):
                x = self.inventory_position[0] + offset_x + self.padding + col * (self.slot_size + self.padding)
                y = self.inventory_position[1] + offset_y + self.padding + row * (self.slot_size + self.padding)
                slots.append((x, y))
        return slots

    def _create_crafting_slots(self):
        crafting_slots = []
        crafting_slots.append((self.inventory_position[0] + 20, self.inventory_position[1] + self.inventory_height - self.screen_height - 2 * self.padding))
        crafting_slots.append((self.inventory_position[0] + self.inventory_width - 70, self.inventory_position[1] + self.inventory_height - self.screen_height - 2 * self.padding))
        crafting_slots.append((self.inventory_position[0] + self.inventory_width // 2 - self.slot_size // 2, self.inventory_position[1] + self.inventory_height - self.screen_height - 2 * self.padding + self.slot_size + 10))
        return crafting_slots

    def load_idle_frames(self):
        idle_spritesheet_image = pygame.image.load('Images/idle_spritesheet_new.png').convert_alpha()
        sprite_sheet = SpriteSheet(idle_spritesheet_image)
        idle_frames = [sprite_sheet.get_image(i, 50, 50, 1, (0, 0, 0)) for i in range(4)]
        for frame in idle_frames:
            frame.set_colorkey((255, 255, 255))
        return idle_frames

    def load_item_images(self):
        """Load item images from the folder."""
        item_images = [
            pygame.image.load('Images/commonitem.png').convert_alpha(),                    
            pygame.image.load('Images/uncommonitem.png').convert_alpha(),
            pygame.image.load('Images/rareitem.png').convert_alpha(),
            pygame.image.load('Images/epicitem.png').convert_alpha(),
            pygame.image.load('Images/legendaryitem.png').convert_alpha(),
            pygame.image.load('Images/mythicitem.png').convert_alpha(),
            pygame.image.load('Images/frauditem.png').convert_alpha(),
            pygame.image.load('Images/wormitem.png').convert_alpha(),
            pygame.image.load('Images/judgeitem.png').convert_alpha(),
            pygame.image.load('Images/gambleritem.png').convert_alpha(),
            pygame.image.load('Images/anti-womenitem.png').convert_alpha(),
            pygame.image.load('Images/comedianitem.png').convert_alpha(),
            pygame.image.load('Images/farmeritem.png').convert_alpha(),
            pygame.image.load('Images/catitem.png').convert_alpha(),
            pygame.image.load('Images/freakyitem.png').convert_alpha(),
            pygame.image.load('Images/cogitem.png').convert_alpha(),
            pygame.image.load('Images/specialzitem.png').convert_alpha(),
            pygame.image.load('Images/nahitem.png').convert_alpha(),
            pygame.image.load('Images/voiditem.png').convert_alpha(),
            pygame.image.load('Images/malevolentitem.png').convert_alpha(),
            pygame.image.load('Images/fingerequip.png').convert_alpha(),                    
            pygame.image.load('Images/babyrattleequip.png').convert_alpha(),
            pygame.image.load('Images/isohequip.png').convert_alpha(),
            pygame.image.load('Images/jailworldequip.png').convert_alpha(),
            pygame.image.load('Images/sex()eyesequip.png').convert_alpha(),
            # Add more as necessary for other slots
        ]

        # Resize images to fit into the slots if necessary
        for i, img in enumerate(item_images):
            if img is not None:
                item_images[i] = pygame.transform.scale(img, (self.slot_size, self.slot_size))
        return item_images

    def load_item_descriptions(self):
        """Load item descriptions from an external JSON file."""
        with open('Game/item_descriptions.json', 'r') as file:
            descriptions = json.load(file)
        return descriptions

    def load_item_to_slot(self):
        """Load the item-to-slot mapping from a JSON file."""
        with open('Game/item_to_slot_count.json', 'r') as file:
            item_names = json.load(file)
            return item_names

    def increment_counter(self, item_name):
        """Increment the counter for the given item."""
        if item_name in self.item_to_slot_count:
            self.item_to_slot_count[item_name] += 1
            print(f"Incrementing counter for {item_name}. Current count: {self.item_to_slot_count[item_name]}")
        else:
            self.item_to_slot_count[item_name] = 1
            print(f"Item {item_name} not found. Initializing counter to 1.")

    def update_item_counts(self, slot1_item, slot2_item, result_item):
        # Load the existing item counts from the JSON file
        with open('Game/item_to_slot_count.json', 'r') as f:
            item_counts = json.load(f)

        # Convert the items to the correct keys as strings
        item1_key = slot1_item
        item2_key = slot2_item
        result_key = result_item

        # Decrease counters for the selected items, ensuring they don't go below 0
        item_counts[item1_key] = max(0, item_counts.get(item1_key, 0) - 1)
        item_counts[item2_key] = max(0, item_counts.get(item2_key, 0) - 1)

        # Increase the counter for the resulting equipment item
        item_counts[result_key] = item_counts.get(result_key, 0) + 1

        # Save the updated counts back to the JSON file
        with open('Game/item_to_slot_count.json', 'w') as f:
            json.dump(item_counts, f, indent=4)

        # Print updated counts for debugging
        print(f"Updated counts: Slot 1 ({item_counts.get(item1_key, 0)}), Slot 2 ({item_counts.get(item2_key, 0)}), Result ({item_counts.get(result_key, 0)})")

        # Update inventory slots immediately after merge
        self.load_item_images()  # Reload images to reflect the new item counts
        self.draw()  # Redraw the slots using the existing method

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
            
            # Check if the event is a mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button_rect.collidepoint(mouse_x, mouse_y):
                    self.close()
                # Ensure merge_button_rect is initialized before checking
                elif hasattr(self, 'merge_button_rect') and self.merge_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Merge button clicked")
                    self.merge_items()
                else:
                    self._check_slot_click(mouse_x, mouse_y)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_clicking = False

    def _check_slot_click(self, mouse_x, mouse_y):
        for i, (x, y) in enumerate(self.inventory_slots):
            if x <= mouse_x <= x + self.slot_size and y <= mouse_y <= y + self.slot_size:
                if pygame.mouse.get_pressed()[0]:  # Left-click (normal click)
                    # Handle the normal slot selection (animation, etc.)
                    if not self.is_clicking:
                        self.is_clicking = True
                        self.selected_slot = i
                        self.animation_index = 0
                        print(f"Slot {i} selected (left-click).")
                    break

                elif pygame.mouse.get_pressed()[2]:  # Right-click (select for crafting)
                    # Deselect if the clicked slot is already selected
                    if self.selected_slot1 == i:
                        self.selected_slot1 = None
                        print(f"Deselected Slot 1 (right-click)")
                    elif self.selected_slot2 == i:
                        self.selected_slot2 = None
                        print(f"Deselected Slot 2 (right-click)")
                    
                    # Select for Slot 1 or Slot 2 if it's not already selected
                    elif self.selected_slot1 is None:
                        if self.selected_slot2 != i:  # Prevent selecting the same slot
                            self.selected_slot1 = i
                            print(f"Selected Slot 1: {i} (right-click)")
                    elif self.selected_slot2 is None:
                        if self.selected_slot1 != i:  # Prevent selecting the same slot
                            self.selected_slot2 = i
                            print(f"Selected Slot 2: {i} (right-click)")
                    else:
                        print(f"Both slots are already selected.")

                    break

    def check_merge_button_click(self, mouse_x, mouse_y):
        merge_button_pos = (self.inventory_position[0] + 280, self.inventory_position[1] + self.inventory_height - 176)
        button_width = 90
        button_height = 40

        # Check if the mouse click is within the merge button area
        if merge_button_pos[0] <= mouse_x <= merge_button_pos[0] + button_width and \
            merge_button_pos[1] <= mouse_y <= merge_button_pos[1] + button_height:
            print("Merge button clicked")

            # Check if both slots are selected
            if self.selected_slot1 is not None and self.selected_slot2 is not None:
                # Perform the merge logic (based on your specific merge rules)
                self.merge_items()
            else:
                print("Please select two items to merge.")

    def merge_items(self):
        # Define your item merge combinations
        combinations =  {
            ('Common', 'Uncommon'): "Finger",  # item0 + item1 = equip0
            ('Mythic', 'Fraud'): "Baby Rattle",  # item2 + item3 = equip1
            ('Worm', 'Gambler'): "ISOH",  # item4 + item5 = equip2
            ('Cat', 'Freaky'): "Jail World",  # item6 + item7 = equip3
            ('Nah', 'Void'): "Sex() Eyes",  # item8 + item9 = equip4
            # Add more recipes as needed
        }

        with open('Game/item_to_slot_count.json', 'r') as file:
            item_data = json.load(file)

        # Get the selected items
        if self.selected_slot1 is not None and self.selected_slot2 is not None:
            # Get the list of item names from the JSON keys
            item_names = list(item_data.keys())  # This will be ['Common', 'Uncommon', ...]
            slot1_item = item_names[self.selected_slot1]  # Use correct mapping to item name
            slot2_item = item_names[self.selected_slot2]

            # Ensure slots are different and valid
            if slot1_item != slot2_item and (slot1_item, slot2_item) in combinations:
                # Get the resulting equipment item from the combination
                result_item = combinations[(slot1_item, slot2_item)]

                # Update the counters in item_to_slot_count.json
                self.update_item_counts(slot1_item, slot2_item, result_item)
                print(f"Merge successful: Created {result_item}")

                #Update the inventory display after merging
                self.item_to_slot_count[slot1_item] -= 1
                self.item_to_slot_count[slot2_item] -= 1
                self.item_to_slot_count[result_item] += 1

                with open('Game/item_to_slot_count.json', 'w') as file:
                    json.dump(item_data, file, indent=4)

                # Update inventory slots immediately after merge
                self.draw()  # Redraw the slots using the existing method

                # Reset selected slots after merging
                self.selected_slot1 = None
                self.selected_slot2 = None

            else:
                print("Invalid combination or slots not selected.")
        else:
            print("Both slots must be selected for merging.")

    def update_animation(self):
        if self.selected_slot is not None:
            # Increment the animation index
            self.animation_index += 1
            
            # Ensure the index wraps around the number of frames to loop the animation
            if self.animation_index >= len(self.idle_frames) * self.animation_speed:
                self.animation_index = 0

    def draw_crafting_interface(self):
        # Modify the height by changing the y-coordinate
        offset_y = 186  # Change this value to adjust the height

        # Define the positions of the crafting slots and symbols relative to the inventory position
        selected_slot1_pos = (self.inventory_position[0] + 20, self.inventory_position[1] + self.inventory_height - offset_y)
        selected_slot2_pos = (self.inventory_position[0] + 120, self.inventory_position[1] + self.inventory_height - offset_y)
        product_slot_pos = (self.inventory_position[0] + 210, self.inventory_position[1] + self.inventory_height - offset_y)
        symbol_plus_pos = (self.inventory_position[0] + 90, self.inventory_position[1] + self.inventory_height - (offset_y - 10))
        symbol_equals_pos = (self.inventory_position[0] + 180, self.inventory_position[1] + self.inventory_height - (offset_y - 10))
        merge_button_pos = (self.inventory_position[0] + 280, self.inventory_position[1] + self.inventory_height - (offset_y - 10))  # To the right of product slot
        merge_button_size = (90, 40)  # Width 90, height 40

        # Draw the crafting slots
        pygame.draw.rect(self.screen, (255, 255, 255), (*selected_slot1_pos, self.slot_size, self.slot_size), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (*selected_slot2_pos, self.slot_size, self.slot_size), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (*product_slot_pos, self.slot_size, self.slot_size), 2)

        # Draw the plus and equals symbols
        plus_sign = self.font.render("+", True, (255, 255, 255))
        equals_sign = self.font.render("=", True, (255, 255, 255))
        self.screen.blit(plus_sign, symbol_plus_pos)
        self.screen.blit(equals_sign, symbol_equals_pos)

        # Draw the merge button
        merge_button_text = self.font.render("Merge", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 255, 0), (*merge_button_pos, 90, 40))  # Green button with width 90, height 40
        self.screen.blit(merge_button_text, (merge_button_pos[0] + 8, merge_button_pos[1] + 6))  # Position text within the button

        # Set merge_button_rect for collision detection
        self.merge_button_rect = pygame.Rect(merge_button_pos, merge_button_size)    

        # Check if there is a selected item for Slot 1 and Slot 2, and display the corresponding item images
        if self.selected_slot1 is not None:
            item_image = pygame.transform.scale(self.item_images[self.selected_slot1], (self.slot_size, self.slot_size))
            self.screen.blit(item_image, selected_slot1_pos)

        if self.selected_slot2 is not None:
            item_image = pygame.transform.scale(self.item_images[self.selected_slot2], (self.slot_size, self.slot_size))
            self.screen.blit(item_image, selected_slot2_pos)

        # Check if both selected items can create a product
        if self.selected_slot1 is not None and self.selected_slot2 is not None:
            slot1_item = list(self.item_to_slot_count.keys())[self.selected_slot1]
            slot2_item = list(self.item_to_slot_count.keys())[self.selected_slot2]

            # Define your combinations here (make sure this matches your existing recipe dictionary)
            combinations = {
                ('Common', 'Uncommon'): "Finger",
                ('Mythic', 'Fraud'): "Baby Rattle",
                ('Worm', 'Gambler'): "ISOH",
                ('Cat', 'Freaky'): "Jail World",
                ('Nah', 'Void'): "Sex() Eyes",
            }

            # Check if the selected items form a valid recipe
            if (slot1_item, slot2_item) in combinations:
                product_item = combinations[(slot1_item, slot2_item)]
                product_image_index = list(self.item_to_slot_count.keys()).index(product_item)

                # Draw the product image
                product_image = pygame.transform.scale(self.item_images[product_image_index], (self.slot_size, self.slot_size))
                product_slot_pos = (self.inventory_position[0] + 210, self.inventory_position[1] + self.inventory_height - 186)
                self.screen.blit(product_image, product_slot_pos)
                print(f"Displaying product image for: {product_item}")
                # Set a flag so that the product image is displayed only once
                self.product_displayed = True

        # Reset product_displayed if any slot is deselected
        if self.selected_slot1 is None or self.selected_slot2 is None:
                self.product_displayed = False

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

        # Load item data from JSON file (assuming it's named 'item_to_slot_count.json')
        with open('Game/item_to_slot_count.json', 'r') as json_file:
            item_data = json.load(json_file)

        # Extract item names from the JSON (the keys of the dictionary)
        item_names = list(item_data.keys())

        # Draw inventory slots
        for i, (x, y) in enumerate(self.inventory_slots):
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, self.slot_size, self.slot_size), 2)

            # Draw the item image if available
            if i < len(self.item_images) and self.item_images[i] is not None:
                item_image = pygame.transform.scale(self.item_images[i], (self.slot_size, self.slot_size))
                self.screen.blit(item_image, (x, y))  # Draw item image first

            # Retrieve the item name from the JSON keys
            item_name = item_names[i] if i < len(item_names) else None

            if item_name:
                # Fetch the counter value using the proper item name
                counter_value = self.item_to_slot_count.get(item_name, 0)

                # If the item is unlocked (counter > 0), draw the item image
                if counter_value > 0:
                    if i < len(self.item_images):  # Ensure index is within bounds of the item_images list
                        item_image = self.item_images[i]  # Access the image via index
                        item_image_scaled = pygame.transform.scale(item_image, (self.slot_size, self.slot_size))
                        self.screen.blit(item_image_scaled, (x, y))
                else:
                    # If the item is locked (counter == 0), draw the '???' image
                    locked_image = pygame.transform.scale(self.locked_image, (self.slot_size, self.slot_size))
                    self.screen.blit(locked_image, (x, y))

                counter_text = self.description_font.render(str(counter_value), True, (255, 255, 255))
                counter_position = (x + self.slot_size - 15, y + self.slot_size - 15)  # Adjust for positioning
                self.screen.blit(counter_text, counter_position)

                # Draw the animation on the selected slot (on top of item image)
                if self.selected_slot == i:  
                    frame_index = (self.animation_index // self.animation_speed) % len(self.idle_frames)
                    frame = self.idle_frames[frame_index]
                    self.screen.blit(frame, (x, y))  # Draw animation on top of the item image if selected

        # Draw crafting interface
        self.draw_crafting_interface()

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
                "Description:", description_data['description'],
            ]

            # Display description on the right screen
            for i, line in enumerate(description_lines):
                description_text = self.description_font.render(line, True, (255, 255, 255))
                self.screen.blit(description_text, (right_screen_rect.x + 10, right_screen_rect.y + 10 + i * (self.description_font.get_height() + self.line_spacing)))
