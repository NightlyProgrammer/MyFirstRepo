import pygame
import json
from tiles import load_tile_spritesheet
from level import Level

def load_settings(path):
    with open(path,'r') as file:
        return json.load(file)
        
def main():
    #Load all the constants from a json file
    SETTINGS = load_settings("settings.json")
    pygame.display.set_mode(SETTINGS["SCREEN_SIZE"],pygame.DOUBLEBUF)
    tile_spritesheet =load_tile_spritesheet("assets/graphics/tiles_spritesheet.png",64,["backend","grass"],["topleft","topmiddle","topright","middleleft","center","middleright","bottomleft","bottommiddle","bottomright"])#load in the spritesheet
    print(tile_spritesheet)
    level1 = Level("assets/levels/level1.json",tile_spritesheet)
    level1.run(SETTINGS,tile_spritesheet)

if __name__ == '__main__':
    pygame.init()
    main()