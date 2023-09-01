import pygame
import json
from player import Player
from camera import CameraGroup
from tiles import Tile
from level import Level

def load_settings(path):
    with open(path,'r') as file:
        return json.load(file)
        
def main():
    #Load all the constants from a json file
    SETTINGS = load_settings("settings.json")
    pygame.display.set_mode(SETTINGS["SCREEN_SIZE"])
    level1 = Level("assets/levels/level1.json")
    level1.run(SETTINGS)

if __name__ == '__main__':
    pygame.init()
    main()