import pygame

class Animation:
    def __init__(self, frame_paths, frame_size, position):
        self.frames = [pygame.image.load(path).convert_alpha() for path in frame_paths]
        self.frames = [pygame.transform.scale(frame, frame_size) for frame in self.frames]
        self.frame_index = 0
        self.animation_speed = 5 
        self.animation_counter = 0
        self.position = position
        self.finished = False

    def update(self):
        if not self.finished:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.finished = True 

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.frame_index], self.position)

    def reset(self):
        #Reset animation to initial state.
        self.frame_index = 0
        self.animation_counter = 0
        self.finished = False