import random
from PIL import Image
import pygame
import os
import block

def image_split(name:str, tile_width:int, padding:pygame.math.Vector2):
    img = Image.open(name)

    blocks = []
    positions = []
    hidden_index = (random.choice((0, img.width//tile_width - 1)), random.choice((0, img.height//tile_width - 1)))

    for y in range(img.width//tile_width):
        for x in range(img.height//tile_width):
            crop = img.crop((x * tile_width, y * tile_width, (x * tile_width) + tile_width, (y * tile_width) + tile_width))
            crop_name = f'({str(x)}, {str(y)}).png'
            crop.save(crop_name)

            if (x, y) != hidden_index:
                blocks.append(block.Block(pygame.image.load(crop_name), pygame.math.Vector2(x * tile_width, y * tile_width) + padding, (x, y)))
            else:
                blocks.append(block.EmptyBlock(pygame.Surface((tile_width, tile_width)), (0, 0, 0), pygame.image.load(crop_name), pygame.math.Vector2(x * tile_width, y * tile_width) + padding, (x, y)))

            positions.append(pygame.math.Vector2(x * tile_width, y * tile_width))
            os.remove(crop_name)

    return blocks, positions, img.width