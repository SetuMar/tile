import math
import pygame
import random

class Particle:
    def __init__(self, position:pygame.math.Vector2, color:tuple, particle_size:float, center_offset_value:float, angle:int, gravity:float, speed:float, angle_change_amt:int) -> None:
        self.sprite = pygame.image.load('particle.png')
        self.sprite = pygame.transform.scale(self.sprite, (particle_size, particle_size))
        self.image = self.sprite
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = pygame.math.Vector2(math.cos(angle) * center_offset_value, math.sin(angle) * center_offset_value) * speed
        self.gravity = gravity
        self.angle = angle
        self.angle_change_amt = angle_change_amt
        
        self.is_faded = False
        
    def update(self):
        self.velocity.y += self.gravity
        self.rect.topleft += self.velocity
        self.angle += self.angle_change_amt
        
        save_pos = self.rect.center
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.center = save_pos
        
        self.opacity -= self.opacity_change_amt
        self.image.set_alpha(self.opacity)
        
    def draw(self, display:pygame.Surface):
        if self.image.get_alpha() > 0:
            display.blit(self.image, self.rect.topleft)
        else:
            self.is_faded = True
            
    @staticmethod
    def generate_particle_group(particle_jump:int, position:pygame.math.Vector2, color:tuple, particle_size:float, center_offset_value:float, gravity:float, speed:float, angle_change_amt:int, opacity_change_amt:int, opacity:int = 255):
        particles = []
        particle_spawn_number = int(360/particle_jump)
        for i in range(0, 361):
            if i % particle_spawn_number == 0:
                particles.append(Particle(position, color, particle_size, center_offset_value, i, gravity, speed, angle_change_amt, opacity_change_amt, opacity))
                
        return particles
    
    def particle_group_update_draw(particles:list, display:pygame.Surface):
        for p in particles:
            p.update()
            display.blit(p.image, p.rect.topleft)
            
            
class SuccessParticles:
    def __init__(max_amt:int, legal_rgb_values:list, particle_jump:int, screen_size:tuple, particle_size:float, center_offset_value:float, gravity:float, speed:float, angle_change_amt:int, opacity_change_amt:int, opacity:int = 255):
        
        for i in range(max_amt):
            print("A")
            # particle_group.append(Particle.generate_particle_group(particle_jump, (random.randrange(0, screen_size[0]), random.randrange(0, screen_size[1])), random.choice(legal_rgb_values), particle_size, center_offset_value, gravity, speed, angle_change_amt, opacity_change_amt, opacity))
            
            
#     create numerous groups of particles
#     generate particle groups during success (amount has to be less than max_amt), ensure color isn't illegal
# update
#     if particles are faded, then remove them from the group
#     update all particles
#     remove particle groups if they are faded
# draw
#     draw all particles
# remove_all
#     remove all particles