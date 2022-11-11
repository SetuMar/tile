import math
import pygame

class Answer:
    def __init__(self, image:pygame.surface, hide_position:pygame.math.Vector2, show_position:pygame.math.Vector2, screen_size:tuple, background_opacity:int = 255, image_opacity:int = 255) -> None:
        self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.center = hide_position
        
        self.positions = [hide_position, show_position]
        self.hide_counter = 0
    
        self.background = pygame.Surface(screen_size)
        self.screen_size = screen_size
        self.background = pygame.transform.scale(self.background, (screen_size[0], 0))
        self.background_lerp = 0
        
        self.background.set_alpha(background_opacity)
        self.image.set_alpha(image_opacity)
    
    def show_hide(self, space_pressed):
        if space_pressed:
            self.hide_counter += 1
        
            if self.hide_counter > len(self.positions) - 1:
                self.hide_counter = 0
    
    def draw(self, display):
        self.background.fill((255, 0, 0))
        lerp_position = self.positions[self.hide_counter]
        self.rect.centery = self.lerp(self.rect.centery, lerp_position.y, 0.25, self.hide_counter != 0)
        
        self.background_lerp = self.lerp(self.background_lerp, self.hide_counter * self.screen_size[0], 0.25, self.hide_counter != 0)
        self.background = pygame.transform.scale(self.background, (self.screen_size[0], self.background_lerp))
        
        display.blit(self.background, (0, 0))
        display.blit(self.image, self.rect.topleft)
        
        if self.rect.bottom > self.screen_size[0]/2:
            return False
        
        return True
        
    def lerp(self, a, b, t, rising):
        if rising:
            return math.ceil(a + (b - a) * t)
        else:
            return math.floor(a + (b - a) * t)