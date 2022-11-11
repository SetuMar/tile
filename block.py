import pygame
import random
import math

class Block:
    previous_movements = []

    def __init__(self, image:pygame.Surface, position:pygame.math.Vector2, index:tuple) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.correct_pos = position
        self.rect.topleft = position
        self.start_index = index
        self.current_index = index
        self.draw_pos = self.rect.topleft

    def draw(self, display:pygame.Surface) -> None:
        self.draw_pos = pygame.math.Vector2(self.draw_pos).lerp(pygame.math.Vector2(self.rect.topleft), 0.5)
        
        if self.rect.x < self.draw_pos.x:
            self.draw_pos.x = math.floor(self.draw_pos.x)
        if self.rect.y < self.draw_pos.y:
            self.draw_pos.y = math.floor(self.draw_pos.y)

        if self.rect.x > self.draw_pos.x:
            self.draw_pos.x = math.ceil(self.draw_pos.x)
        if self.rect.y > self.draw_pos.y:
            self.draw_pos.y = math.ceil(self.draw_pos.y)

        display.blit(self.image, self.draw_pos)

    @staticmethod
    def shuffle(blocks:list, shuffle_positions:list):
        for index, b in enumerate(blocks):
            b.rect.topleft = shuffle_positions[index]

    @staticmethod
    def generate_shuffle(blocks, shuffle_amt, puzzle_size, block_size):
        for i in range(shuffle_amt):
            for b in blocks:
                if type(b) == EmptyBlock:
                    possibles = [
                    (b.current_index[0] + 1, b.current_index[1]),
                    (b.current_index[0] - 1, b.current_index[1]),
                    (b.current_index[0], b.current_index[1] + 1),
                    (b.current_index[0], b.current_index[1] - 1)
                ]

                    for p in possibles:
                        if p[0] < 0 or p[1] < 0 or p[0] > (puzzle_size / block_size) - 1 or p[1] > (puzzle_size / block_size) - 1 or p in Block.previous_movements:
                            possibles.remove(p)

                    random_index = random.choice(possibles)
                    Block.previous_movements = [(possibles[0], possibles[1])]

                    for b_inner in blocks:
                        if b_inner.current_index == random_index:
                            b.current_index, b_inner.current_index = b_inner.current_index, b.current_index
                            b.rect.topleft, b_inner.rect.topleft = b_inner.rect.topleft, b.rect.topleft

class EmptyBlock(Block):
    def __init__(self, unsolved_img:pygame.Surface, unsolved_color:tuple, solved_img:pygame.Surface, position:pygame.math.Vector2, index:tuple) -> None:
        Block.__init__(self, unsolved_img, position, index)
        self.image.fill(unsolved_color)
        self.solved_img = solved_img
        self.mouse_save = 0
    
    def switch(self, blocks, block_size):
        mouse = pygame.mouse.get_pressed()

        if mouse == (1, 0, 0):
            self.mouse_save += 1
        elif mouse == (0, 0, 0) and self.mouse_save > 0:
            poss = [
                self.rect.topleft + pygame.math.Vector2(block_size, 0),
                self.rect.topleft + pygame.math.Vector2(-block_size, 0),
                self.rect.topleft + pygame.math.Vector2(0, block_size),
                self.rect.topleft + pygame.math.Vector2(0, -block_size),
            ]

            for b in blocks:
                if b.rect.topleft in poss and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.rect.topleft, b.rect.topleft = b.rect.topleft, self.rect.topleft
                    self.current_index, b.current_index = b.current_index, self.current_index

            self.mouse_save = 0