import pygame
import sys

import image_split
import block
import answer
import particles

screen_size = (800, 800)
pygame.init()

display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

block_size = 100
padding = pygame.math.Vector2(200, 200)
image_name = 'test-3.png'
image = pygame.image.load('test-3.png')

blocks, solved, puzzle_size = image_split.image_split(image_name, block_size, padding)

shuffle_amt = 800
block.Block.generate_shuffle(blocks, shuffle_amt, puzzle_size, block_size)

unknown_block = None

answer_image = answer.Answer(image, pygame.math.Vector2(screen_size[0]/2, 0 - image.get_height()/2), pygame.math.Vector2(screen_size[0]/2, screen_size[1]/2), screen_size, 100, 200)
can_use_mouse = True

test_success_partiles = particles.SuccessParticles(5, [(255, 0, 0)], 10, screen_size, 16, 10, 5, 5, 5, 5)

while True:
    display.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        answer_image.show_hide(event.type == pygame.KEYUP and event.key == pygame.K_SPACE)
    
    if unknown_block != None:
        unknown_block.draw(display)

    solved = True
    for index, b in enumerate(blocks):
        if type(b) == block.EmptyBlock and can_use_mouse:
            b.switch(blocks, block_size)
            
            unknown_block = b
        else:
            b.draw(display)
            
        if solved == True and b.current_index != b.start_index:
            solved = False
    
    if solved:
        unknown_block.image = unknown_block.solved_img

    can_use_mouse = bool(answer_image.draw(display) * (not solved))

    pygame.display.update()
    clock.tick(60)